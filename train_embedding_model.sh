export PYTHONPATH="${PWD}/..:${PWD}/../..:"

THREADS=31

# Disable multithreading in all numerical packages
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

DATA_DIRECTORY="/mnt/ds/temp"

python3 \
    ./pipelines/train_embedding_model.py \
    --dataDirectory=${DATA_DIRECTORY} \
    --threads=${THREADS} \
    $1
