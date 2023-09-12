# `cloudsc4py`: GT4Py-based implementation of the CLOUDSC dwarf

This folder contains a Python implementation of the CLOUDSC microphysics scheme based on
[GT4Py](https://github.com/GridTools/gt4py.git). The code is bundled as an installable
package called `cloudsc4py`, whose source code is placed under `src/`.


## Installation

We strongly recommend installing the package in an isolated virtual environment:

```shell
# create virtual environment under `venv/`
$ python -m venv venv

# activate the virtual environment
$ . venv/bin/activate

# upgrade base packages
(venv) $ pip install --upgrade pip setuptools wheel
```

The package `cloudsc4py` can be installed using the Python package manager [pip](https://pip.pypa.io/en/stable/):

```shell
# install cloudsc4py along with the minimal set of requirements
(venv) $ pip install .

# create a fully reproducible development environment with an editable installation of cloudsc4py
(venv) $ pip install -r requirements-dev.txt
(venv) $ pip install -e .

# enable the GPU backends of GT4Py on an NVIDIA GPU using CUDA 11.x
(venv) $ pip install .[gpu-cuda11x]

# enable the GPU backends of GT4Py on an NVIDIA GPU using CUDA 12.x
(venv) $ pip install .[gpu-cuda12x]

# enable the GPU backends of GT4Py on an AMD GPU using ROCm/HIP
(venv) $ export CUPY_INSTALL_USE_HIP=1
(venv) $ export ROCM_HOME=<path to ROCm installation>
(venv) $ export HCC_AMDGPU_TARGET=<string denoting the Instruction Set Architecture (ISA) supported by the target GPU>
(venv) $ pip install .[gpu]
```

## Usage

The scheme comes in two forms: one where computations are carried out in a single stencil
(see `src/cloudsc4py/{physics,_stencils}/cloudsc.py`), and one where calculations are split into two
stencils (one computing tendencies on the main vertical levels, the other computing fluxes at the
interface levels; see `src/cloudsc4py/{physics,_stencils}/cloudsc_split.py`).

The easiest way to run the dwarf is through the driver scripts `drivers/run.py` and `drivers/run_split.py`.
Run the two scripts with the `--help` option to get the full list of command-line options.

For the sake of convenience, we provide the driver `drivers/run_fortran.py` to invoke one of the
FORTRAN variants of the dwarf from within Python.
