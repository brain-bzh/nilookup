#!/usr/bin/env python
# coding: utf-8

from nilearn.image import coord_transform
import numpy as np 
from numpy.linalg import inv
from nilearn.image import load_img
import pandas as pd 
from nilearn.datasets import fetch_atlas_harvard_oxford,fetch_atlas_destrieux_2009,fetch_atlas_juelich

import argparse

oxford = fetch_atlas_harvard_oxford('cort-maxprob-thr0-2mm')
destrieux = fetch_atlas_destrieux_2009()
destrieux['labels'] = [(des[1]) for des in destrieux['labels']] ## removing the index
juelich = fetch_atlas_juelich('maxprob-thr0-2mm')

def inverse_lookup(coord,atlasmap,atlaslabels):
    ## coord is a MNI coordinate
    ## atlasmap is a path to a nii or nii.gz file of a labels atlas
    ## atlaslabels is a list of corresponding labels
    labelmap = load_img(atlasmap).get_fdata()
    voxelcoords = np.array(coord_transform(coord[0],coord[1],coord[2],inv(load_img(atlasmap).affine)),dtype=int)
    label_ind = int(labelmap[voxelcoords[0],voxelcoords[1],voxelcoords[2]])
    return atlaslabels[label_ind]                    


def coord_to_labels(my_coord,atlas_list = [oxford,destrieux,juelich],atlas_names = ['Harvard Oxford','Destrieux', 'Juelich']):

    labels_dict = dict()
    labels_dict['x_MNI'] = my_coord[0]
    labels_dict['y_MNI'] = my_coord[1]
    labels_dict['z_MNI'] = my_coord[2]
    
    for curatlas,curname in zip(atlas_list,atlas_names):
        maps,labels = curatlas['maps'],curatlas['labels']
        labels_dict[curname] = inverse_lookup(my_coord,maps,labels)
    return(labels_dict)

if __name__ == '__main__':
    

    parser = argparse.ArgumentParser()
    parser.add_argument("-x", type=int, help="X coordinate in MNI")
    parser.add_argument("-y", type=int, help="Y coordinate in MNI")
    parser.add_argument("-z", type=int, help="Z coordinate in MNI")
    parser.add_argument("-i",type=str,help="Path to a csv file in which each row is x,y,z,name",default='')
    parser.add_argument("-o",type=str,help="Write the output to a csv file",default='')
    args = parser.parse_args()
    
    if len(args.i)==0:
        listcoords = [[args.x,args.y,args.z]]
        listnames = ['noname']
    else:
        listcoords = pd.read_csv(args.i,header=0,usecols=[0,1,2],sep=',').to_numpy()
        listnames = pd.read_csv(args.i,header=0,usecols=[3],sep=',').to_numpy()
        

    Df = []
    for curcoord in listcoords:
        Df.append(coord_to_labels(curcoord))

    Df = pd.DataFrame(Df)
    Df['name'] = listnames

    print(Df)

    if len(args.o)>0:
        Df.to_csv(args.o,index=False)