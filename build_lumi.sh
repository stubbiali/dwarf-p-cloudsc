#!/bin/bash

./cloudsc-bundle build \
  --arch=arch/eurohpc/lumi/cray-gpu/14.0.2 \
  --build-dir=build/cray-gpu/14.0.2/release/double \
  --build-type=release \
  --hdf5=ON \
  --with-gpu \
  --with-loki \
  --without-loki-install \
  --clean

./cloudsc-bundle build \
  --arch=arch/eurohpc/lumi/cray-gpu/14.0.2 \
  --build-dir=build/cray-gpu/14.0.2/release/single \
  --build-type=release \
  --hdf5=ON \
  --with-gpu \
  --with-loki \
  --without-loki-install \
  --single-precision \
  --clean

./cloudsc-bundle build \
  --arch=arch/eurohpc/lumi/cray-gpu/14.0.2 \
  --build-dir=build/cray-gpu/14.0.2/bit/double \
  --build-type=bit \
  --hdf5=ON \
  --with-gpu \
  --with-loki \
  --without-loki-install \
  --clean

./cloudsc-bundle build \
  --arch=arch/eurohpc/lumi/cray-gpu/14.0.2 \
  --build-dir=build/cray-gpu/14.0.2/bit/single \
  --build-type=bit \
  --hdf5=ON \
  --with-gpu \
  --with-loki \
  --without-loki-install \
  --single-precision \
  --clean

./cloudsc-bundle build \
  --arch=arch/eurohpc/lumi/cray-gpu/15.0.1 \
  --build-dir=build/cray-gpu/15.0.1/release/double \
  --build-type=release \
  --hdf5=ON \
  --with-hip \
  --with-serialbox \
  --clean

./cloudsc-bundle build \
  --arch=arch/eurohpc/lumi/cray-gpu/15.0.1 \
  --build-dir=build/cray-gpu/15.0.1/release/single \
  --build-type=release \
  --hdf5=ON \
  --with-hip \
  --with-serialbox \
  --single-precision \
  --clean

./cloudsc-bundle build \
  --arch=arch/eurohpc/lumi/cray-gpu/15.0.1 \
  --build-dir=build/cray-gpu/15.0.1/bit/double \
  --build-type=bit \
  --hdf5=ON \
  --with-hip \
  --with-serialbox \
  --clean

./cloudsc-bundle build \
  --arch=arch/eurohpc/lumi/cray-gpu/15.0.1 \
  --build-dir=build/cray-gpu/15.0.1/bit/single \
  --build-type=bit \
  --hdf5=ON \
  --with-hip \
  --with-serialbox \
  --single-precision \
  --clean
