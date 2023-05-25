import trimesh
import pyvista as pv
from pyvista import examples
import numpy as np
import matplotlib.pyplot as plt
from pyscf import compute_spfs,normalize_sph,batch_sph2scf


mesh = trimesh.load('./examples/obj.obj')
mesh = mesh.apply_scale(1/mesh.scale)
points = mesh.bounding_sphere.to_mesh().bounding_box.sample_grid(4)

spfs,rays = compute_spfs(mesh,points,return_rays=True)
scfs = batch_sph2scf(spfs)
plt.imshow(scfs[:,:5].T)
plt.xlabel('points')
plt.ylabel('scf')
# plt.yticks([0,1,2,3,4])
plt.tight_layout()
plt.show()

pl = pv.Plotter(window_size=(500,500))
pl.add_mesh(mesh,opacity=0.5)
for i in range(len(points)):
    sp = rays[i][:,:3]+rays[i][:,3:]*0.05
    spf = spfs[i]
    spf_norm = normalize_sph(spf)
    pl.add_mesh(sp,scalars=spf_norm,opacity=0.5,show_scalar_bar=False)
pl.show(screenshot='./imgs/spf.png')