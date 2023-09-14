# -*- coding: utf-8 -*-

# (C) Copyright 2018- ECMWF.
# (C) Copyright 2022- ETH Zurich.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

from __future__ import annotations
import numpy as np
from os.path import dirname, join, normpath

from ifs_physics_common.framework.config import (
    DataTypes,
    FortranConfig,
    GT4PyConfig,
    IOConfig,
    PythonConfig,
)


config_files_dir = normpath(join(dirname(__file__), "../../../config-files"))
default_python_config = PythonConfig(
    num_cols=1,
    enable_validation=True,
    input_file=join(config_files_dir, "input.h5"),
    reference_file=join(config_files_dir, "reference.h5"),
    num_runs=15,
    precision="double",
    data_types=DataTypes(bool=bool, float=np.float64, int=np.int64),
    gt4py_config=GT4PyConfig(backend="numpy", rebuild=False, validate_args=True, verbose=True),
    sympl_enable_checks=True,
)

default_fortran_config = FortranConfig(
    build_dir=".",
    precision="double",
    variant="fortran",
    nproma=32,
    num_cols=1,
    num_runs=1,
    num_threads=1,
)

default_io_config = IOConfig(output_csv_file=None, host_name="")
