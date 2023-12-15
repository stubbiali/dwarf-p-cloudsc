# -*- coding: utf-8 -*-
from __future__ import annotations
import click
from typing import TYPE_CHECKING

from cloudsc4py.physics.cloudsc import Cloudsc
from cloudsc4py.initialization.reference import get_reference_tendencies, get_reference_diagnostics
from cloudsc4py.initialization.state import get_state
from cloudsc4py.utils.iox import HDF5Reader
from ifs_physics_common.framework.grid import ComputationalGrid
from ifs_physics_common.utils.output import (
    print_performance,
    write_performance_to_csv,
    write_stencils_performance_to_csv,
)
from ifs_physics_common.utils.timing import timing
from ifs_physics_common.utils.validation import validate

if TYPE_CHECKING:
    from typing import Literal, Optional, Type

    from ifs_physics_common.framework.config import IOConfig, PythonConfig

    from .config import default_python_config, default_io_config
else:
    from config import default_python_config, default_io_config


def core(config: PythonConfig, io_config: IOConfig, cloudsc_cls: Type) -> None:
    hdf5_reader = HDF5Reader(config.input_file, config.data_types)

    nx = config.num_cols or hdf5_reader.get_nlon()
    nz = hdf5_reader.get_nlev()
    computational_grid = ComputationalGrid(nx, 1, nz)

    state = get_state(computational_grid, hdf5_reader, gt4py_config=config.gt4py_config)
    dt = hdf5_reader.get_timestep()

    yoecldp_paramaters = hdf5_reader.get_yoecldp_parameters()
    yoethf_parameters = hdf5_reader.get_yoethf_parameters()
    yomcst_parameters = hdf5_reader.get_yomcst_parameters()
    yrecldp_parameters = hdf5_reader.get_yrecldp_parameters()

    cloudsc = cloudsc_cls(
        computational_grid,
        yoecldp_paramaters,
        yoethf_parameters,
        yomcst_parameters,
        yrecldp_parameters,
        enable_checks=config.sympl_enable_checks,
        gt4py_config=config.gt4py_config,
    )
    tends, diags = cloudsc(state, dt)

    config.gt4py_config.reset_exec_info()

    runtime_l = []
    for i in range(config.num_runs):
        with timing(f"run_{i}") as timer:
            cloudsc(state, dt, out_tendencies=tends, out_diagnostics=diags)
        runtime_l.append(timer.get_time(f"run_{i}"))

    runtime_mean, runtime_stddev, mflops_mean, mflops_stddev = print_performance(nx, runtime_l)

    if io_config.output_csv_file is not None:
        write_performance_to_csv(
            io_config.output_csv_file,
            io_config.host_name,
            config.precision,
            config.gt4py_config.backend,
            nx,
            config.num_threads,
            1,
            config.num_runs,
            runtime_mean,
            runtime_stddev,
            mflops_mean,
            mflops_stddev,
        )

    if config.enable_validation:
        hdf5_reader_ref = HDF5Reader(config.reference_file, config.data_types)
        tends_ref = get_reference_tendencies(
            computational_grid, hdf5_reader_ref, gt4py_config=config.gt4py_config
        )
        diags_ref = get_reference_diagnostics(
            computational_grid, hdf5_reader_ref, gt4py_config=config.gt4py_config
        )

        tends_fail = validate(tends, tends_ref)
        if len(tends_fail) == 0:
            print("Results: All tendencies have been successfully validated. HOORAY!")
        else:
            print(
                f"Results: Validation failed for {len(tends_fail)}/{len(tends_ref) - 1} "
                f"tendencies: {', '.join(tends_fail)}."
            )

        diags_fail = validate(diags, diags_ref)
        if len(diags_fail) == 0:
            print("Results: All diagnostics have been successfully validated. HOORAY!")
        else:
            print(
                f"Results: Validation failed for {len(diags_fail)}/{len(diags_ref) - 1} "
                f"diagnostics: {', '.join(diags_fail)}."
            )


@click.command()
@click.option(
    "--backend",
    type=str,
    default="numpy",
    help="GT4Py backend (options: cuda, dace:cpu, dace:gpu, gt:cpu_ifirst, gt:cpu_kfirst, gt:gpu, "
    "numpy; default: numpy).",
)
@click.option(
    "--enable-checks/--disable-checks",
    is_flag=True,
    type=bool,
    default=False,
    help="Enable/disable sanity checks performed by Sympl and GT4Py (default: enabled).",
)
@click.option(
    "--enable-validation/--disable-validation",
    is_flag=True,
    type=bool,
    default=True,
    help="Enable/disable data validation (default: enabled).",
)
@click.option("--num-cols", type=int, default=1, help="Number of domain columns (default: 1).")
@click.option("--num-runs", type=int, default=1, help="Number of executions (default: 1).")
@click.option(
    "--precision",
    type=str,
    default="double",
    help="Select either `double` (default) or `single` precision.",
)
@click.option("--host-alias", type=str, default=None, help="Name of the host machine (optional).")
@click.option(
    "--output-csv-file",
    type=str,
    default=None,
    help="Path to the CSV file where writing performance counters (optional).",
)
@click.option(
    "--output-csv-file-stencils",
    type=str,
    default=None,
    help="Path to the CSV file where writing performance counters for each stencil (optional).",
)
def main(
    backend: str,
    enable_checks: bool,
    enable_validation: bool,
    num_cols: int,
    num_runs: int,
    precision: Literal["double", "single"],
    host_alias: Optional[str],
    output_csv_file: Optional[str],
    output_csv_file_stencils: Optional[str],
) -> None:
    """
    Driver for the GT4Py-based implementation of CLOUDSC.

    Computations are carried out in a single stencil.
    """
    config = (
        default_python_config.with_backend(backend)
        .with_checks(enable_checks)
        .with_validation(enable_validation)
        .with_num_cols(num_cols)
        .with_num_runs(num_runs)
        .with_precision(precision)
    )
    io_config = default_io_config.with_output_csv_file(output_csv_file).with_host_name(host_alias)
    core(config, io_config, cloudsc_cls=Cloudsc)

    if output_csv_file_stencils is not None:
        write_stencils_performance_to_csv(
            output_csv_file_stencils,
            io_config.host_name,
            config.precision,
            config.gt4py_config.backend,
            config.num_cols,
            config.num_threads,
            config.num_runs,
            config.gt4py_config.exec_info,
            key_patterns=["cloudsc"],
        )


if __name__ == "__main__":
    main()