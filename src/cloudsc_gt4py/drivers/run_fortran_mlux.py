# -*- coding: utf-8 -*-

# (C) Copyright 2018- ECMWF.
# (C) Copyright 2022- ETH Zurich.

# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import os
from typing import Literal

from run_fortran import _main


# config: start
build_dir_parent: str = "/project/home/p200177/nasu/cloudsc/develop/build/nvhpc/22.7"
build_type_l: list[str] = ["release", "bit"]
precision_l: list[Literal["double", "single"]] = ["double", "single"]
host_alias: str = "mlux"
num_cols: int = 65536
num_runs: int = 50
output_dir_parent: str = "/project/home/p200177/nasu/cloudsc2/develop/data/nvhpc/22.7"
variants: dict[str, dict[str, int]] = {
    "fortran": {"num_threads": 16, "nproma": 32},
    # "c-cuda-k-caching": {"num_threads": 1, "nproma": 128},
    # "gpu-scc-k-caching": {"num_threads": 1, "nproma": 128},
    # "loki-scc-cuf-hoist": {"num_threads": 1, "nproma": 128},
}
# config: end


def main():
    for build_type in build_type_l:
        for precision in precision_l:
            build_dir = os.path.join(build_dir_parent, build_type, precision)
            output_dir = os.path.join(output_dir_parent, build_type)
            os.makedirs(output_dir, exist_ok=True)
            output_csv_file = os.path.join(output_dir, "performance.csv")
            for variant, options in variants.items():
                print(f"{variant=} {build_type=} {precision=}: start", flush=True)
                _main(
                    build_dir,
                    precision,
                    variant,
                    options["nproma"],
                    num_cols,
                    num_runs,
                    options["num_threads"],
                    host_alias,
                    output_csv_file,
                )
                print(f"{variant=} {build_type=} {precision=}: end", flush=True)


if __name__ == "__main__":
    main()
