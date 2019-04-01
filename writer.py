"""
XRF data writer.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import dxfile.dxtomo as dx

__author__ = "Francesco De Carlo"
__copyright__ = "Copyright (c) 2019, UChicago Argonne, LLC."
__version__ = "0.0.1"
__docformat__ = 'restructuredtext en'
__all__ = ['write_dxfile']



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
