import os
import glob


data_dir = ''

if __name__ == "__main__":
    # first, define ATTA study-specific information.
    # since we sampled subjects at two different frequencies,
    # identify the anomalous subjects (sampled at 50Hz)

    # subjects = glob.glob('16*')  # 40 Hz subjects
    subjects = ['1611058', '1611103', '1621107']  # 50 Hz subjects

    for s in subjects:
        data_files = glob.glob(os.path.join(data_dir, s, '*.nii.gz'))
        phys_files = glob.glob(os.path.join(data_dir, s, '*.1D'))
        timings = glob.glob(os.path.join(data_dir, s, '*.txt'))
