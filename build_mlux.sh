#!/bin/bash

srun --cpus-per-task=128 ./cloudsc-bundle build \
  --arch=arch/eurohpc/meluxina/nvhpc/22.7 \
  --build-dir=build/nvhpc/22.7/release/double \
  --build-type=release \
  --hdf5=ON \
  --with-cuda \
  --with-gpu \
  --with-loki \
  --with-serialbox \
  --without-loki-install
#  --clean

srun --cpus-per-task=128 ./cloudsc-bundle build \
  --arch=arch/eurohpc/meluxina/nvhpc/22.7 \
  --build-dir=build/nvhpc/22.7/release/single \
  --build-type=release \
  --hdf5=ON \
  --with-cuda \
  --with-gpu \
  --with-loki \
  --with-serialbox \
  --without-loki-install \
  --single-precision
#  --clean

srun --cpus-per-task=128 ./cloudsc-bundle build \
  --arch=arch/eurohpc/meluxina/nvhpc/22.7 \
  --build-dir=build/nvhpc/22.7/bit/double \
  --build-type=bit \
  --hdf5=ON \
  --with-cuda \
  --with-gpu \
  --with-loki \
  --with-serialbox \
  --without-loki-install
#  --clean

srun --cpus-per-task=128 ./cloudsc-bundle build \
  --arch=arch/eurohpc/meluxina/nvhpc/22.7 \
  --build-dir=build/nvhpc/22.7/bit/single \
  --build-type=bit \
  --hdf5=ON \
  --with-cuda \
  --with-gpu \
  --with-loki \
  --with-serialbox \
  --without-loki-install \
  --single-precision
#  --clean
