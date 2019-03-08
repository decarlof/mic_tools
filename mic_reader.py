
"""
Module for importing MIC HDF data files.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import os
import sys
import argparse
import dxchange

__author__ = "Francesco De Carlo"
__copyright__ = "Copyright (c) 2018, UChicago Argonne, LLC."
__version__ = "0.0.1"
__docformat__ = 'restructuredtext en'
__all__ = ['read_projection',
           'read_elements',
           'find_index']


def find_index(a_list, element):
    try:
        return a_list.tolist().index(element)
    except ValueError:
        return None

def read_elements(h5fname):
    return(dxchange.read_hdf5(h5fname, "MAPS/channel_names"))

def read_projection(fname, element, theta_index):
    """
    Reads a projection for a given element from an hdf file.

    Parameters
    ----------
    fname : str
        String defining the file name
    element : 
        String defining the element to select
    theta_index :
        index where theta is saved under in the hdf MAPS/extra_pvs_as_csv tag.
        For unknown reason 2-ID-E and the Bio Nano proble save this information 
        in different index location (663 and 657)

    Returns
    -------
    float
        projection angle
    ndarray
        projection
    """

    projections = dxchange.read_hdf5(fname, "MAPS/XRF_roi")
    theta = float(dxchange.read_hdf5(fname, "MAPS/extra_pvs_as_csv")[theta_index].split(b',')[1])
    elements = read_elements(fname)

    return projections[find_index(elements, element)], theta


# use test data at https://anl.box.com/s/qinted32vyrcnjyt7tzs3cx6kreeud3m

def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="Directory containing multiple datasets or file name of a single dataset: /data/ or /data/sample.h5")
    parser.add_argument("--start", nargs='?', type=float, default=0.0, help="Angle first projection (default 0.0)")
    parser.add_argument("--end", nargs='?', type=float, default=180.0, help="Angle last projection (default 180.0)")
    parser.add_argument("--element", nargs='?', type=str, default="Si", help="Select the element to recontruct (default Si)")

    args = parser.parse_args()

    # Set path to the micro-CT data to reconstruct.
    fname = args.fname
    angle_start = float(args.start)
    angle_end = float(args.end)
    element = args.element

    if os.path.isfile(fname):    

        elements = mr.read_elements(fname)

        for i, e in enumerate(elements):
            print ('%d:  %s' % (i, e))
        
        proj, theta = mr.read_projection(fname, element, 663)
        print ("theta:", theta)
#        print (theta.shape)
        print ("proj:", proj)
        print (proj.shape)

    elif os.path.isdir(fname):
        # Add a trailing slash if missing
        top = os.path.join(fname, '')

        h5_file_list = list(filter(lambda x: x.endswith(('.h5', '.hdf')), os.listdir(top)))

        for i, fname in enumerate(h5_file_list):
            proj, theta = mr.read_projection(top+fname, element, 657) ##BNP 8; 2-ID-E: 663; 2-ID-E prior 2017: 657
            # print(i, theta, fname)
            print(theta, fname)

    else:
        print("Directory or File Name does not exist: ", fname)

if __name__ == "__main__":
    main(sys.argv[1:])
