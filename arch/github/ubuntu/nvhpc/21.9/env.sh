# (C) Copyright 1988- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

# Source me to get the correct configure/build/run environment

### Variables
export NVHPC_INSTALL_DIR=${GITHUB_WORKSPACE}/nvhpc-install
export NVHPC_VERSION=21.9
export CUDA_VERSION=11.4
export NVHPC_DIR=${NVHPC_INSTALL_DIR}/Linux_x86_64/${NVHPC_VERSION}

### Compilers
export PATH=${NVHPC_DIR}/compilers/bin:${PATH}
export NVHPC_LIBRARY_PATH=${NVHPC_DIR}/compilers/lib
export LD_LIBRARY_PATH=${NVHPC_LIBRARY_PATH}:${LD_LIBRARY_PATH}

### MPI
export MPI_HOME=${NVHPC_DIR}/comm_libs/mpi
export PATH=${MPI_HOME}/bin:${PATH}
export LD_LIBRARY_PATH=${NVHPC_DIR}/cuda/${CUDA_VERSION}/targets/x86_64-linux/lib/stubs:${LD_LIBRARY_PATH}

### HDF5
export HDF5_DIR=${GITHUB_WORKSPACE}/hdf5-install
export LD_LIBRARY_PATH=${HDF5_DIR}/lib:${LD_LIBRARY_PATH}
export PATH=${HDF5_DIR}/bin:${PATH}

### Compiler variables
export CC=pgcc
export CXX=pgc++
export FC=pgf90

export ECBUILD_TOOLCHAIN="./toolchain.cmake"

# Increase stack size to maximum
ulimit -S -s unlimited
