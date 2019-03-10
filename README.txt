Reader/Data converter for 2-ID-E and Bio Nano Probe data

Reads 2-ID-E and Bio Nano Probe data and converts in a stack of tiff or hdf files. 
The hdf files are tomographic data exchange formatted and directly loadable in tomopy.

Example:

    python convert.py mic_data/  (<= full path to the directory containing the datasets)
    python convert.py --element Ca --output_fformat hdf mic_data/

Help:
    
    python convert.py -h


Usage: convert.py [-h] [--element [ELEMENT]]
                     [--output_fname [OUTPUT_FNAME]]
                     [--output_fformat [OUTPUT_FFORMAT]]
                     [--theta_index [THETA_INDEX]]
                     fname

positional arguments:
  fname                 directory containing multiple datasets or file name of
                        a single dataset: /data/ or /data/sample.h5

optional arguments:
  -h, --help            show this help message and exit
  --element [ELEMENT]   element selection (default Si)
  --output_fname [OUTPUT_FNAME]
                        output file path and prefix (default ./tmp/data)
  --output_fformat [OUTPUT_FFORMAT]
                        output file format: hdf or tiff (default hdf)
  --theta_index [THETA_INDEX]
                        theta_index: 2-ID-E: 663; 2-ID-E prior 2017: 657; BNP
                        8; (default 657)