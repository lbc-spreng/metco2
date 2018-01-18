import nipype.interfaces.io as nio
import nipype.pipeline.engine as pe
from niworkflows.nipype.interfaces import utility as niu
from nipype.interfaces.afni.model import (Deconvolve, Synthesize)


def init_metco2_wf(subject, task_id):
    """
    This workflow ... .

    .. workflow::
    :graph2use: orig
    :simple_form: yes

       from metco2.workflows.base import init_metco2_wf
       wf = init_metco2_wf(subject='fmripreptest')

    Inputs
    ------


    Outputs
    -------
    nipype workflow
    """
    metco2_wf = pe.Workflow(name='metco2_wf')

    # input node for gathering relevant files
    inputnode = pe.Node(niu.IdentityInterface(fields=['']),
                        name='inputnode')

    # run a GLM in AFNI using 3dDeconvolve
    deconvolve = pe.Node(Deconvolve(outputtype='NIFTI_GZ'),
                         name='deconvolve')
    deconvolve.inputs.in_files = []
    deconvolve.inputs.num_stimts = []
    deconvolve.inputs.stim_times = ('', '')
    deconvolve.inputs.args = '-stim_file {}'.format()
    deconvolve.inputs.x1D = ''
    deconvolve.inputs.cbucket = ''

    # use 3dSynthesize to remove the variance associated with
    # our physiological confounds
    synthesize = pe.Node(Synthesize(), name='synthesize')
    synthesize.inputs.select = ['']

    # save out the corrected data to a datasink
    datasink = pe.Node(nio.DataSink(), name='datasink')
    datasink.inputs.base_directory = ''
    datasink.inputs.container = ''

    metco2_wf.connect([
        (inputnode, deconvolve, [('', '')]),
        (deconvolve, synthesize, [('cbucket', 'cbucket'),
                                  ('x1D', 'matrix')])
        (synthesize, datasink, [('', '')])
    ])

    return metco2_wf
