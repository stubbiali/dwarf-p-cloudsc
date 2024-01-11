#!/usr/bin/bash

#export EXTRA_COMPILE_ARGS="-fbracket-depth=4096"
export DEFAULT_BLOCK_SIZE="128,1,1"

CC=gcc CXX=g++ srun --pty --ntasks=1 --cpus-per-task=128 python run.py \
  --backend=gt:cpu_kfirst --precision=double --num-cols=100 --num-runs=1
CC=gcc CXX=g++ srun --ntasks=1 --cpus-per-task=128 python run.py \
  --backend=gt:cpu_kfirst --precision=single --num-cols=100 --num-runs=1
CC=gcc CXX=g++ CUDA_HOST_CXX=g++ srun --ntasks=1 --cpus-per-task=128 python run.py \
  --backend=dace:gpu --precision=double --num-cols=100 --num-runs=1
CC=gcc CXX=g++ CUDA_HOST_CXX=g++ srun --ntasks=1 --cpus-per-task=128 python run.py \
  --backend=dace:gpu --precision=single --num-cols=100 --num-runs=1
