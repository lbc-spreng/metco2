import os
import numpy as np
from argparse import (ArgumentParser, RawTextHelpFormatter)

from ..workflows import init_metco2_wf
from ..utils.physio import convolve_ts
from ..utils.misc import (create_subj_list, gather_inputs)


def get_parser():
    """
    Builds parser object.
    """
    from ..info import __version__

    verstr = 'metco2 v{}'.format(__version__)

    parser = ArgumentParser(description='MEtCO2',
                            formatter_class=RawTextHelpFormatter)

    # Arguments as specified by BIDS-Apps-- for eventual MEtCO2 BIDS App
    parser.add_argument('data_dir', action='store',
                        help='the root folder of the dataset.')
    parser.add_argument('output_dir', action='store',
                        help='the output directory for preprocessing.')
    parser.add_argument('analysis_level', choices=['participant'],
                        help='processing stage to be run, only "participant".')

    # optional arguments
    parser.add_argument('--version', action='version', version=verstr)

    g_data = parser.add_argument_group('Options for filtering dataset queries')
    g_data.add_argument('--participant_label', '--participant-label',
                        action='store', nargs='+',
                        help='one or more participant identifiers.')
    return parser


def main():
    """
    Entry point.
    """
    opts = get_parser().parse_args()

    output_dir = os.path.abspath(opts.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    subjects = create_subj_list(opts.data_dir,
                                selected=opts.participant_label)
    for s in subjects:
        images, events, physio = gather_inputs(opts.data_dir, s)
        confounds_fname = os.path.join(opts.data_dir, s + '_confounds.txt')
        np.savetxt(confounds_fname, [convolve_ts(p) for p in physio],
                   fmt='%10.5f')
        workflow = init_metco2_wf(images, events, confounds_fname,
                                  s, output_dir)
        workflow.run('MultiProc', plugin_args={'n_procs': 6})


if __name__ == "__main__":

    raise RuntimeError('metco2/cli/run.py should not be run directly.\n'
                       'Please `pip install` metco2 and run `metco2`')
