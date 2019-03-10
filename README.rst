MIC TOOLS
#########

**Mic Tools** contains a list of python tools to interface X-ray Fluorescence (XRF) data collected at the Advanced Photon Source Microscopy beamlines 2-ID-E and the Bio Nano Probe with `tomoPy <https://tomopy.readthedocs.io/en/latest/>`_

Convert
=======

* Reads 2-ID-E and Bio Nano Probe data and converts in a stack of tiff or hdf files 
* The hdf files are tomographic data exchange formatted and directly loadable in tomopy with `rec.py <https://github.com/decarlof/util/tree/master/recon>`_
* Tested with `2-ID-E data <https://anl.box.com/s/qinted32vyrcnjyt7tzs3cx6kreeud3m>`_


Help::
    
    python convert.py -h


Usage::
    
    convert.py [-h] [--element [ELEMENT]]
                     [--output_fname [OUTPUT_FNAME]]
                     [--output_fformat [OUTPUT_FFORMAT]]
                     [--theta_index [THETA_INDEX]]
                     fname


positional arguments::

  fname                 directory containing multiple datasets or file name of
                        a single dataset: /data/ or /data/sample.h5

optional arguments::

  -h, --help            show this help message and exit
  --element [ELEMENT]   element selection (default Si)
  --output_fname [OUTPUT_FNAME]
                        output file path and prefix (default ./data)
  --output_fformat [OUTPUT_FFORMAT]
                        output file format: hdf or tiff (default hdf)
  --theta_index [THETA_INDEX]
                        theta_index: 2-ID-E: 663; 2-ID-E prior 2017: 657; BNP
                        8; (default 657)

Example::

    python convert.py mic_data/  (<= full path to the directory containing the datasets)
    python convert.py --element Ca --output_fformat hdf mic_data/

Using tomoPy::

    python rec.py(*) data.h5

(*) `rec.py <https://github.com/decarlof/util/tree/master/recon>`_
