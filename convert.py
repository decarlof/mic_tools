
"""
Module for converting MIC multiple HDF data files in a sigle hdf file.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import os
import sys
import numpy as np
import argparse
import dxchange
from pylab import *
import dxfile.dxtomo as dx

from elements import ELEMENTS

__author__ = "Francesco De Carlo"
__copyright__ = "Copyright (c) 2019, UChicago Argonne, LLC."
__version__ = "0.0.1"
__docformat__ = 'restructuredtext en'
__all__ = ['read_projection',
           'read_channel_names',
           'read_xrf',
           'write_dxfile']


def find_index(a_list, element):
    try:
        return a_list.index(element)
    except ValueError:
        return None


def find_elements(channel_names):
    """
    Extract a sorted element list from a channel list.

    Parameters
    ----------
    channel_names : list
        List of channel names

    Returns
    -------
    elements : list
        Sorted list of elements
    
    """

    elements = []
    for i in range(1, 110, 1): 
         elements.append(str(ELEMENTS[i].symbol))

    elements = sorted(set(channel_names) & set(elements), key = channel_names.index)

    return elements


def read_channel_names(h5fname):
    b_channel_names = dxchange.read_hdf5(h5fname, "MAPS/channel_names")
    channel_names = []
    for i, e in enumerate(b_channel_names):
        channel_names.append(e.decode('utf-8'))
    return(channel_names)


def read_projection(fname, element, theta_index):
    """
    Reads a projection for a given element from a single xrf hdf file.

    Parameters
    ----------
    fname : str
        String defining the file name

    element : 
        String defining the element to select
    
    theta_index :
        Index where theta is saved under in the hdf MAPS/extra_pvs_as_csv tag.
        This is:
                2-ID-E:             663 
                2-ID-E prior 2017:  657 
                BNP:                  8

    Returns
    -------
    ndarray
        projection

    float
        projection angle
    
    """

    projections = dxchange.read_hdf5(fname, "MAPS/XRF_roi")
    theta = float(dxchange.read_hdf5(fname, "MAPS/extra_pvs_as_csv")[theta_index].split(b',')[1])
    elements = read_channel_names(fname)

    try:
        if find_index(elements, element) != None:
            return projections[find_index(elements, element),:, :], theta
        else:
            raise TypeError
    except TypeError:
        print("**** ERROR: Element %s does exist in the file: %s " % (element, fname))
        return None


def read_xrf(dname, theta_index):
    """
    Reads all xrf hdf files in a folder.

    Parameters
    ----------
    dname : str
        String defining the folder name

    theta_index : int
        Index where theta is saved under in the hdf MAPS/extra_pvs_as_csv tag.
        This is:
                2-ID-E:             663 
                2-ID-E prior 2017:  657 
                BNP:                  8

    Returns
    -------
    ndarray
        4D XRF tomographic data [element, theta, y, x]

    ndarray
        1D theta in degrees.

    string list
        elements 

    """
    # Add a trailing slash if missing
    top = os.path.join(dname, '')

    h5_file_list = list(filter(lambda x: x.endswith(('.h5', '.hdf')), os.listdir(top)))

    channel_names = read_channel_names(top+h5_file_list[0])
    print ("Channel Names:   ", channel_names)

    elements = find_elements(channel_names)
    print ("Sorted Elements: ", elements)

    # this is just the find proj.shape
    proj, theta = read_projection(top+h5_file_list[0], elements[0], theta_index) 

    data = zeros([len(elements), len(h5_file_list), proj.shape[0], proj.shape[1]])
    theta = zeros([len(h5_file_list)])

    for j, element in enumerate(elements):
        for i, dname in enumerate(h5_file_list):
            proj, theta_image = read_projection(top+dname, element, theta_index) 
            data[j, i, :, :] = proj
            theta[i] = theta_image
    
    return data, theta, elements


def write_dxfile(fname, proj, theta, elem):
    experimenter_affiliation="Argonne National Laboratory" 
    instrument_name="2-ID-E XRF"  
    sample_name = "test data set"

    # Open DataExchange file
    f = dx.File(fname, mode='w')
     
    # Write the Data Exchange HDF5 file.
    f.add_entry(dx.Entry.experimenter(affiliation={'value': experimenter_affiliation}))
    f.add_entry(dx.Entry.instrument(name={'value': instrument_name}))
    f.add_entry(dx.Entry.sample(name={'value': sample_name}))

    f.add_entry(dx.Entry.data(data={'value': proj, 'units':'ug/cm^2'}))
    f.add_entry(dx.Entry.data(theta={'value': theta, 'units':'degrees'}))

    elem = [x.encode('utf-8') for x in elem]
    f.add_entry(dx.Entry.data(elements={'value': elem, 'units':'ug/cm^2'}))

    f.close()


def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("dname", help="directory containing multiple datasets: /data/")
    parser.add_argument("--output_fname", nargs='?', type=str, default="./data", help="output file path and prefix (default ./data)")
    parser.add_argument("--theta_index", nargs='?', type=int, default=657, help="theta_index: 2-ID-E: 663; 2-ID-E prior 2017: 657; BNP 8; (default 657)")

    args = parser.parse_args()

    dname = args.dname
    out = args.output_fname
    theta_index = args.theta_index

    if os.path.isdir(dname):
        data, theta, elements = read_xrf(dname, theta_index)
        write_dxfile(out + ".h5", data, theta, elements)
    else:
        print("Directory does not exist: ", dname)


if __name__ == "__main__":
    main(sys.argv[1:])
