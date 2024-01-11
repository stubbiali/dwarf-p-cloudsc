#!/usr/bin/bash

export EXTRA_COMPILE_ARGS="-fbracket-depth=4096"
export DEFAULT_BLOCK_SIZE="256,1,1"

CC=cc CXX=CC srun --ntasks=1 --cpus-per-task=56 python run.py \
  --backend=gt:cpu_kfirst --precision=double --num-cols=100 --num-runs=1
CC=cc CXX=CC srun --ntasks=1 --cpus-per-task=56 python run.py \
  --backend=gt:cpu_kfirst --precision=single --num-cols=100 --num-runs=1
CC=cc CXX=CC srun --ntasks=1 --cpus-per-task=56 python run.py \
  --backend=dace:gpu --precision=double --num-cols=100 --num-runs=1
CC=cc CXX=CC srun --ntasks=1 --cpus-per-task=56 python run.py \
  --backend=dace:gpu --precision=single --num-cols=100 --num-runs=1
