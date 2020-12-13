export PYTHONPATH="${PWD}/..:${PWD}/../..:"

THREADS=31

# Disable multithreading in all numerical packages
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

SOURCE_DATA_DIRECTORY="/home/sragner/full-hn-20201129"
MODEL_DIRECTORY="/mnt/ds/temp"
LOAD_MODEL_FILE="/mnt/ds/doc2vec/doc2vec_007.model"

python3 \
    ./pipelines/create_embedding_model.py \
    --sourceDataDirectory=${SOURCE_DATA_DIRECTORY} \
    --modelDirectory=${MODEL_DIRECTORY} \
    --loadModelFile=${LOAD_MODEL_FILE} \
    --threads=${THREADS} \
    $1
