# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING

from gt4py import gtscript

if TYPE_CHECKING:
    from typing import Any

    from gt4py import StencilObject

    from cloudsc4py.framework.config import GT4PyConfig


FUNCTION_COLLECTION = {}
STENCIL_COLLECTION = {}


def function_collection(name: str):
    if name in FUNCTION_COLLECTION:
        raise RuntimeError(f"Another function called `{name}` found.")

    def core(definition):
        FUNCTION_COLLECTION[name] = {"definition": definition}
        return definition

    return core


def stencil_collection(name: str):
    if name in STENCIL_COLLECTION:
        raise RuntimeError(f"Another stencil called `{name}` found.")

    def core(definition):
        STENCIL_COLLECTION[name] = {"definition": definition}
        return definition

    return core


def compile_stencil(
    name: str,
    gt4py_config: GT4PyConfig,
    externals: dict[str, Any] = None,
) -> StencilObject:
    stencil_info = STENCIL_COLLECTION.get(name, None)
    if stencil_info is None:
        raise RuntimeError(f"Unknown stencil `{name}`.")
    definition = stencil_info["definition"]

    dtypes = gt4py_config.dtypes.dict()
    externals = externals or {}

    kwargs = gt4py_config.backend_opts.copy()
    if gt4py_config.backend not in ("debug", "numpy", "gtc:numpy"):
        kwargs["verbose"] = gt4py_config.verbose

    return gtscript.stencil(
        gt4py_config.backend,
        definition,
        name=name,
        build_info=gt4py_config.build_info,
        dtypes=dtypes,
        externals=externals,
        rebuild=gt4py_config.rebuild,
        **kwargs,
    )
