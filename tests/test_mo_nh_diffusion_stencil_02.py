# ICON4Py - ICON inspired code in Python and GT4Py
#
# Copyright (c) 2022, ETH Zurich and MeteoSwiss
# All rights reserved.
#
# This file is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or any later
# version. See the LICENSE.txt file at the top-level directory of this
# distribution for a copy of the license or check <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import numpy as np

from src.gt4py.mo_nh_diffusion_stencil_02 import (
    mo_nh_diffusion_stencil_02,
)
from src.gt4py.dimension import C2EDim, CellDim, EdgeDim, KDim
from simple_mesh import SimpleMesh
from utils import random_field, zero_field


def mo_nh_diffusion_stencil_02_div_numpy(
    c2e: np.array,
    vn: np.array,
    geofac_div: np.array,
) -> np.array:
    geofac_div = np.expand_dims(geofac_div, axis=-1)
    vn_geofac = vn[c2e] * geofac_div
    div = np.sum(vn_geofac, axis=1)  # sum along edge dimension
    return div


def mo_nh_diffusion_stencil_02_khc_numpy(
    c2e: np.array,
    kh_smag_ec: np.array,
    e_bln_c_s: np.array,
    diff_multfac_smag: np.array,
) -> np.array:
    e_bln_c_s = np.expand_dims(e_bln_c_s, axis=-1)
    diff_multfac_smag = np.expand_dims(diff_multfac_smag, axis=-1)
    mul = kh_smag_ec[c2e] * e_bln_c_s
    summed = np.sum(mul, axis=1)  # sum along edge dimension
    kh_c = summed / diff_multfac_smag
    return kh_c


def mo_nh_diffusion_stencil_02_numpy(
    c2e: np.array,
    kh_smag_ec: np.array,
    vn: np.array,
    e_bln_c_s: np.array,
    geofac_div: np.array,
    diff_multfac_smag: np.array,
):
    kh_c = mo_nh_diffusion_stencil_02_khc_numpy(
        c2e, kh_smag_ec, e_bln_c_s, diff_multfac_smag
    )
    div = mo_nh_diffusion_stencil_02_div_numpy(c2e, vn, geofac_div)
    return div, kh_c


def test_mo_nh_diffusion_stencil_02():
    mesh = SimpleMesh()

    vn = random_field(mesh, EdgeDim, KDim)
    geofac_div = random_field(mesh, CellDim, C2EDim)
    kh_smag_ec = random_field(mesh, EdgeDim, KDim)
    e_bln_c_s = random_field(mesh, CellDim, C2EDim)
    diff_multfac_smag = random_field(mesh, CellDim)

    kh_c = zero_field(mesh, CellDim, KDim)
    div = zero_field(mesh, CellDim, KDim)

    div_ref, kh_c_ref = mo_nh_diffusion_stencil_02_numpy(
        mesh.c2e,
        np.asarray(kh_smag_ec),
        np.asarray(vn),
        np.asarray(e_bln_c_s),
        np.asarray(geofac_div),
        np.asarray(diff_multfac_smag),
    )

    mo_nh_diffusion_stencil_02(
        kh_smag_ec,
        vn,
        e_bln_c_s,
        geofac_div,
        diff_multfac_smag,
        kh_c,
        div,
        offset_provider={
            "C2E": mesh.get_c2e_offset_provider(),
        },
    )
    assert np.allclose(kh_c, kh_c_ref)
    assert np.allclose(div, div_ref)
