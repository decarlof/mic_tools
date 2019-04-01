#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example to align the XRF tomography projections.
"""

from __future__ import print_function

import os
import sys
import tomopy
import dxchange as dx
import numpy as np
import argparse
import shutil


def read_xrf(fname):
    data = dx.read_hdf5(fname, dataset='/exchange/data').astype('float32').copy()
    b_elements = dx.read_hdf5(fname, dataset='/exchange/elements')
    elements = []
    for i, e in enumerate(b_elements):
        elements.append(e.decode('utf-8'))
    ang = dx.read_hdf5(fname, dataset='/exchange/theta').astype('float32').copy()
    ang *= np.pi / 180.

    return elements, ang, data


def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="directory containing multiple datasets or file name of a single dataset: /data/ or /data/sample.h5")
    parser.add_argument("--iters", nargs='?', type=int, default=10, help="number of iteration for alignment (default 7)")

    args = parser.parse_args()
    fname = args.fname
    iters = args.iters

    if os.path.isfile(fname):    
        # Add a trailing slash if missing
        top = os.path.join(fname, '')
        print("File Name:", fname)

        elements, ang, data = read_xrf(fname)
        print (elements)

        prj = np.sum(data, axis = 0)

        print (prj.shape)

        # Clean folder.
        try:
            shutil.rmtree('tmp/iters')
        except:
            pass

        prj = tomopy.remove_nan(prj, val=0.0)
        prj = tomopy.remove_neg(prj, val=0.0)
        prj[np.where(prj == np.inf)] = 0.0
        
        print (prj.min(), prj.max())

        prj, sx, sy, conv = tomopy.align_joint(prj, ang, iters=100, pad=(0, 0),
                            blur=True, rin=0.8, rout=0.95, center=None,
                            algorithm='pml_hybrid',
                            upsample_factor=100,
                            save=True, debug=True)




if __name__ == "__main__":
    main(sys.argv[1:])
