# Wrapper for juno typing pipeline

#----------------------------------------------#
# Create/update necessary environments
PATH_MAMBA_YAML="envs/mamba.yaml"
PATH_MASTER_YAML="envs/master_env.yaml"
MAMBA_NAME=$(head -n 1 ${PATH_MAMBA_YAML} | cut -f2 -d ' ')
MASTER_NAME=$(head -n 1 ${PATH_MASTER_YAML} | cut -f2 -d ' ')

envs_list=$(conda env list)

if ! $(echo $envs_list | grep -q mamba)
then
    echo -e "Installing ${MAMBA_NAME} environment..."
    conda env update -f "${PATH_MAMBA_YAML}"
fi

echo -e "Activating ${MAMBA_NAME} environment..."
source activate "${MAMBA_NAME}"

if ! $(echo $envs_list | grep -q "${MASTER_NAME}")
then
    echo -e "Installing ${MASTER_NAME} environment..."
    mamba env update -f "${PATH_MASTER_YAML}"
fi

echo -e "Activating ${MASTER_NAME} environment..."
source activate "${MASTER_NAME}"

#----------------------------------------------#
# Run the pipeline

if [ ! -z ${irods_runsheet_sys__runsheet__lsf_queue} ]; then
    QUEUE="${irods_runsheet_sys__runsheet__lsf_queue}"
else
    QUEUE="bio"
fi

echo -e "Running pipeline..."
python juno_blast.py --queue "${QUEUE}" ${@}