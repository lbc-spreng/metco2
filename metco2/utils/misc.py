import os
import glob
from itertools import groupby
from utils.file_manip import (split_dmat_txt, sort_and_write)


def group_phys(phys_files):
    """
    """
    def _group_phys(x):
        return x.split('_')[-1]

    phys_files = [list(v) for k, v in groupby(sorted(phys_files,
                                                     key=_group_phys),
                                              key=_group_phys)]
    return phys_files


def group_timings(timing_files):
    """
    """
    def _group_timings(x):
        return x.split('_')[2]

    phys_files = [list(v) for k, v in groupby(sorted(timing_files,
                                                     key=_group_timings),
                                              key=_group_timings)]
    return phys_files


def create_subj_list(data_dir, selected=None):
    """
    # ['sub-1611058', 'sub-1611103', 'sub-1621107']
    """
    subject_list = glob.glob(os.path.join(data_dir, 'sub-*'))
    subject_list = [os.path.basename(s) for s in subject_list]
    if selected is not None:
        if all([s in subject_list for s in selected]):
            subject_list = selected
        else:
            print('Selected subjects not in data directory!')
            exit()
    return subject_list


def gather_inputs(data_dir, subj):
    """
    """

    data_files = sorted(glob.glob(os.path.join(data_dir, subj, '*.nii.gz')))
    phys_files = glob.glob(os.path.join(data_dir, subj, '*.1D'))
    phys_files = group_phys(phys_files)

    # some non-BIDS ugliness... works only for ATTA
    dmat = (glob.glob(os.path.join(data_dir, subj, '*dmat.txt')))[0]
    run_timings = split_dmat_txt(dmat)
    sort_and_write(2, run_timings, subj)
    timing_files = glob.glob(os.path.join(data_dir, subj, '*condition*.txt'))
    timings = group_timings(timing_files)

    return data_files, phys_files, timings
