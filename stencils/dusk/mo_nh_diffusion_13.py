from dusk.script import *

lb, nudging, interior, halo, end = HorizontalDomains(0, 1000, 2000, 3000, 4000)

@stencil
def mo_nh_diffusion_stencil_13(
    kh_smag_e: Field[Edge, K],
    inv_dual_edge_length: Field[Edge],
    theta_v: Field[Cell, K],
    z_nabla2_e: Field[Edge, K]
):
  with domain.upward.across[nudging:halo+1]:
    # compute kh_smag_e * grad(theta) (stored in z_nabla2_e for memory efficiency)
    z_nabla2_e = kh_smag_e * inv_dual_edge_length * \
        sum_over(Edge > Cell, theta_v, weights=[-1.0, 1.0])
