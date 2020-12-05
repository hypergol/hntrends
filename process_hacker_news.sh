export PYTHONPATH="${PWD}/..:${PWD}/../..:"

THREADS=15

# Disable multithreading in all numerical packages
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

FILE_PATTERN="/data/hn-full-20201129/hn-full-20201129-*"
DATA_DIRECTORY="/data/hn-full-20201129"

python3 \
    ./pipelines/process_hacker_news.py \
    --filePattern=${FILE_PATTERN} \
    --dataDirectory=${DATA_DIRECTORY} \
    --threads=${THREADS} \
    $1
