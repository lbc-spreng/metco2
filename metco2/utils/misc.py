import os
import glob


def create_subj_list(data_dir, selected=None):
    """
    # ['sub-1611058', 'sub-1611103', 'sub-1621107']
    """
    subject_list = glob.glob(os.path.join(data_dir, 'sub-*'))
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
    data_files = glob.glob(os.path.join(data_dir, subj, '*.nii.gz'))
    phys_files = glob.glob(os.path.join(data_dir, subj, '*.1D'))
    timings = glob.glob(os.path.join(data_dir, subj, '*.txt'))

    return data_files, phys_files, timings
