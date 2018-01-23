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
    from ..info import __version__
    opts = get_parser().parse_args()

    output_dir = os.path.abspath(opts.output_dir)
    os.makedirs(output_dir, exist_ok=True)
    data_dir = os.path.abspath(opts.data_dir)

    subjects = create_subj_list(opts.data_dir,
                                selected=opts.participant_label)

    init_msg = """
    Running MEtCO2 version {version}:
      * BIDS dataset path: {data_dir}.
      * Output path: {output_dir}
      * Participant list: {participant_list}.
    """.format

    print(init_msg(version=__version__,
                   data_dir=data_dir,
                   output_dir=output_dir,
                   participant_list=subjects))

    for subj in subjects:
        images, physio, events = gather_inputs(data_dir, subj)
        for i, image in enumerate(images):
            run = image.split('.')[0].split('_')[1]  # some non-BIDS ugliness

            hr, resp = [convolve_ts(p) for p in physio[i]]
            confounds_fname = os.path.join(data_dir, subj,
                                           '{}_confounds_{}.txt'.format(subj,
                                                                        run))
            np.savetxt(confounds_fname, np.transpose([hr, resp]), fmt='%10.5f')

            workflow = init_metco2_wf(images[i], events[i], confounds_fname,
                                      subj, output_dir)
            # for debugging:
            # workflow.config['execution'] = {'remove_unnecessary_outputs': False,
            #                                 'keep_inputs': True,
            #                                 'try_hard_link_datasink': False}
            workflow.write_graph(graph2use='flat')
            workflow.run('MultiProc', plugin_args={'n_procs': 6})


if __name__ == "__main__":

    raise RuntimeError('metco2/cli/run.py should not be run directly.\n'
                       'Please `pip install` metco2 and run `metco2`')
