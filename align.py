"""
Align XRF tomography projections using tomoPy.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import sys
import tomopy
import numpy as np
import argparse
import shutil
import reader as dxr


def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="file name of xrf dxchange file: ./data.h5")
    parser.add_argument("--iters", nargs='?', type=int, default=10, help="number of iteration for alignment (default 10)")

    args = parser.parse_args()
    fname = args.fname
    iters = args.iters

    if os.path.isfile(fname):    
        # Add a trailing slash if missing
        top = os.path.join(fname, '')

        elements, ang, data = dxr.read_dx_xrf(fname)
        print ("Elements: ", elements)

        prj = np.sum(data, axis = 0)

        # Clean folder.
        try:
            shutil.rmtree('tmp/iters')
        except:
            pass

        prj = tomopy.remove_nan(prj, val=0.0)
        prj = tomopy.remove_neg(prj, val=0.0)
        prj[np.where(prj == np.inf)] = 0.0
        
        print (prj.min(), prj.max())

        prj, sx, sy, conv = tomopy.align_joint(prj, ang, iters=iters, pad=(0, 0),
                            blur=True, rin=0.8, rout=0.95, center=None,
                            algorithm='pml_hybrid',
                            upsample_factor=100,
                            save=True, debug=True)


if __name__ == "__main__":
    main(sys.argv[1:])
