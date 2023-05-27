import os
import pickle
import trimesh
import numpy as np
from trimesh import creation
from tqdm import tqdm
import pyvista as pv
from pyscf import batch_compute_scfs

ndf_root = os.environ['NDF_SOURCE_DIR']
points_dir = f'{ndf_root}/src/ndf_robot/data/training_data'
mesh_dir = f'{ndf_root}/src/ndf_robot/descriptions/objects'
save_dir = f'{ndf_root}/src/ndf_robot/data/training_data/scfs'

for category in ['mug','bowl','bottle']:
    data_dict = pickle.load(open(f'{points_dir}/occ_shapenet_{category}.p','rb'))
    data_ids = list(data_dict.keys())
    os.makedirs(f'{save_dir}/{category}',exist_ok=True)
    for data_id in tqdm(data_ids):
        category_id, shapenet_id, _, _ = data_id.split('/')
        mesh_path = f'{mesh_dir}/{category}_centered_obj_normalized/{shapenet_id}/models/model_normalized.obj'
        mesh128_path = f'{mesh_dir}/{category}_centered_obj/{shapenet_id}/models/model_128_df.obj'
        if not os.path.exists(mesh128_path): continue
        
        # mesh = trimesh.load(f'{mesh_path}',process=False,maintain_order=True)
        mesh_128 = trimesh.load(mesh128_path,process=False)
        points = creation.box([1.1,1.1,1.1]).bounding_box.sample_grid(128)
        idx = np.random.permutation(128**3)[:100000]
        points = points[idx]

        # points,occ , _ = data_dict[data_id]
        # occ = occ.squeeze()
        scfs = batch_compute_scfs(mesh_128,points)[...,:5]

        data = np.concatenate([points,scfs],axis=-1)    
        np.save(f'{save_dir}/{category}/{shapenet_id}.npy',data)    
