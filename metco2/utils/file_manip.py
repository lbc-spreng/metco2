import os
from operator import itemgetter


def split_dmat_txt(fname):
    '''
    Split PLS datamat text files into lists,
    retaining run information.
    '''
    runs_only = []
    fparts = []

    with open(fname, 'r') as f:
        fparts.extend(f.read().split("data_files"))

    for part in fparts[1:len(fparts)+1]:
        runs_only.append(part.strip().split("\n"))
        for sess in runs_only:
            match = ['run', 'block_onsets']
            sess[:] = [l for l in sess if any(list(m in l for m in match))]

    for sess in range(len(runs_only)):
        for s in range(len(runs_only[sess])):
            runs_only[sess][s] = runs_only[sess][s].split("\t")

    for sess in runs_only:
        for cond in sess:
            try:
                cond.remove('block_onsets')
            except ValueError:
                pass
    return runs_only


def sort_and_write(TR_in_S, runs_only, subj):
    '''
    Sort runs by chronological order, convert onsets
    to seconds, and pull conditions to text files for AFNI.
    '''
    TR = float(TR_in_S)
    runs_only.sort(key=itemgetter(0))

    for i, run in enumerate(runs_only):
        for cond in range(1, len(runs_only[i])):
            with open(os.path.join(subj,
                                   "{}_run_{}_condition_{}.txt".format(subj,
                                                                       i+1,
                                                                       cond)), "a+") as f:
                for onset in runs_only[i][cond]:
                    if onset is not '':
                        f.write(''.join(str(int(onset)*TR)) + '\t')
