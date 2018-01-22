import os
import glob
from itertools import groupby


def group_phys(phys_files):
    """
    """
    def _get_run_num(x):
        return x.split('_')[-1]

    phys_files = [list(v) for k, v in groupby(sorted(phys_files,
                                                     key=_get_run_num),
                                              key=_get_run_num)]
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
    timings = sorted(glob.glob(os.path.join(data_dir, subj, '*condition*.txt')))
    return data_files, phys_files, timings
