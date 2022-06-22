from dusk.script import *

lb, nudging, interior, halo, end = HorizontalDomains(0, 1000, 2000, 3000, 4000)

fac_bdydiff_v = Global("fac_bdydiff_v")


@stencil
def mo_nh_diffusion_stencil_06(
    z_nabla2_e: Field[Edge, K], area_edge: Field[Edge], vn: Field[Edge, K]
):
    with domain.upward.across[lb+4:nudging+1]:
        vn += z_nabla2_e * area_edge * fac_bdydiff_v
