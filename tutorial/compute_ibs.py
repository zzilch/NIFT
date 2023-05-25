import trimesh
import pyibs
import pyvista as pv
pv.rcParams['transparent_background'] = True
    
mesh0 = trimesh.load('./examples/hand.obj')
mesh1 = trimesh.load('./examples/obj.obj')
ibs = pyibs.IBS(mesh0.sample(5000), mesh1.sample(5000))

pl = pv.Plotter()
pl.add_mesh(mesh0,'w')
pl.add_mesh(mesh1,[.4,.7,1.])
pl.add_mesh(ibs.mesh,'purple',opacity=.5)
pl.background_color = [1.,1.,1.]
pl.show(screenshot='./imgs/ibs.png')