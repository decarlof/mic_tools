
"""
Module for converting MIC multiple HDF data files in a sigle hdf file.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import os
import sys
import argparse

import reader as dxr
import writer as dxw
import dxfile.dxtomo as dx

__author__ = "Francesco De Carlo"
__copyright__ = "Copyright (c) 2019, UChicago Argonne, LLC."
__version__ = "0.0.1"
__docformat__ = 'restructuredtext en'


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
        data, theta, elements = dxr.read_mic_xrf(dname, theta_index)
        dxw.write_dxfile(out + ".h5", data, theta, elements)
        print("Created the xrf dxfile: ", out + ".h5")
    else:
        print("Directory does not exist: ", dname)


if __name__ == "__main__":
    main(sys.argv[1:])
