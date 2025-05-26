# Using KSO on LUMI

## Steps for DTO-BioFlow project members

- Go to https://www.lumi.csc.fi/ and login
- Select Jupyter app ([direct link](https://www.lumi.csc.fi/pun/sys/dashboard/batch_connect/sys/ood-base-jupyter/session_contexts/new))
- Choose the following settings:
  - Project: project_465001460 (DTO-BioFlow project)
  - Partition: small-g
  - Number of CPU cores: 1 (Note: use values below 8 if using only a single GPU; see [billing](https://docs.lumi-supercomputer.eu/runjobs/lumi_env/billing/#gpu-billing))
  - Memory (GB): 30 (Note: this is CPU memory; use values below 64 GB if using only a single GPU; see [billing](https://docs.lumi-supercomputer.eu/runjobs/lumi_env/billing/#gpu-billing))
  - Number of GPUs (MI250 GCDs): 1
  - Time: 2:00:00 (Note: adjust as needed)
  - Working directory: /scratch/$PROJECT
  - Under 'Advanced'
    - Custom Python type: Script
    - Script or path to script: Copy-paste the following lines (you can omit the first line if you have notebooks already available on LUMI):

          git clone -b add-lumi https://github.com/ocean-data-factory-sweden/kso.git "/scratch/$PROJECT/$USER/kso"
          export SINGULARITY_BIND="/pfs,/scratch,/projappl,/project,/flash,/appl"
          export python="singularity exec /projappl/$PROJECT/containers/kso-lumi_0.1.0.sif python3"
          export PYTHONUSERBASE="/scratch/$PROJECT/$USER/venv"

- Click Launch
- Wait for the Jupyter session to be queued and launched
- Click 'Connect to Jupyter' once the button appears
- Navigate in Jupyter to the notebooks under **your working directory** (the directory named as your LUMI username)


## Steps for general users

The steps above work in general after the following changes:

- Initial preparation step: pull/transfer the singularity container image (the sif file) to LUMI as explained in the corresponding step [in these instructions](containers/lumi/README.md).
- Update the project code 'project_465001460' and the path to the sif file in the instructions above

