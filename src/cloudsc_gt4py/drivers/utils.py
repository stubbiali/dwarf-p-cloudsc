# -*- coding: utf-8 -*-

# (C) Copyright 2018- ECMWF.
# (C) Copyright 2022- ETH Zurich.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

from __future__ import annotations
import csv
import datetime
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Tuple


def to_csv(
    output_file: str,
    host_name: str,
    variant: str,
    num_cols: int,
    num_threads: int,
    nproma: int,
    num_runs: int,
    runtime_mean: float,
    runtime_stddev: float,
    mflops_mean: float,
    mflops_stddev: float,
) -> None:
    """Write performance statistics to a CSV file."""
    if not os.path.exists(output_file):
        with open(output_file, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(
                (
                    "date",
                    "host",
                    "variant",
                    "num_cols",
                    "num_threads",
                    "nproma",
                    "num_runs",
                    "runtime_mean",
                    "runtime_stddev",
                    "mflops_mean",
                    "mflops_stddev",
                )
            )
    with open(output_file, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(
            (
                datetime.date.today().strftime("%Y%m%d"),
                host_name,
                variant,
                num_cols,
                num_threads,
                nproma,
                num_runs,
                runtime_mean,
                runtime_stddev,
                mflops_mean,
                mflops_stddev,
            )
        )


def print_performance(
    num_cols: int, runtime_l: list[float], mflops_l: Optional[list[float]] = None
) -> Tuple[float, float, float, float]:
    """Print means and standard deviation of runtimes and MFLOPS."""
    n = len(runtime_l)
    print(f"Performance over {num_cols} columns and {n} runs:")

    runtime_mean = sum(runtime_l) / n
    runtime_stddev = (
        sum((runtime - runtime_mean) ** 2 for runtime in runtime_l) / (n - 1 if n > 1 else n)
    ) ** 0.5
    print(f"-  Runtime: {runtime_mean:.3f} \u00B1 {runtime_stddev:.3f} ms.")

    mflops_l = mflops_l or [0.12482329 * num_cols / (runtime / 1000) for runtime in runtime_l]
    mflops_mean = sum(mflops_l) / n
    mflops_stddev = (
        sum((mflops - mflops_mean) ** 2 for mflops in mflops_l) / (n - 1 if n > 1 else n)
    ) ** 0.5
    print(f"-  MFLOPS: {mflops_mean:.3f} \u00B1 {mflops_stddev:.3f}.")

    return runtime_mean, runtime_stddev, mflops_mean, mflops_stddev
