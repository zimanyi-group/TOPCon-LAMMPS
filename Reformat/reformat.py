import ReadLAMMPS as rl
import atom
import sys, os
import pdb
import numpy as np


def scaledFileName(file,a):
    id=file.index('.data')
    outfile = file[:id] + "_"+str(int(a*100)) + file[id:]
    return outfile

def Replicate(sim, x,y,z):
    new_sim = rl.Simulation
    bx, by, bz = sim.box[0][1], sim.box[1][1], sim.box[2][1]
    temp = []
    count = sim.num + 1
    for at in sim.atoms:
        if(at.type == 1):
            at.type =3
        elif(at.type == 2):
            at.type = 1
        ax, ay, az = at.coords
        if((ax + bx) < x):
            temp.append(atom.ATOM([count, at.type, ax + bx, ay, az]))
            count +=1
        if((ay + by) < y):
            temp.append(atom.ATOM([count, at.type, ax, ay + by, az]))
            count +=1
        if((ax + bx) < x and (ay + by) < y):
            temp.append(atom.ATOM([count, at.type, ax + bx, ay + by, az]))
            count +=1
    sim.box = np.array([[0.0,x], [0.0,y], [0.0,bz]])
    atom.ATOM.set_box(sim.box)
    sim.num +=len(temp)
    sim.atoms = np.concatenate([sim.atoms,np.asarray(temp)])
    return

#What we want to do is read in multiple data files and take small slices and stack them on top of each other.
# 1) read in all data files and create an array of simulations.
# 2) create a container of atoms.
# 3) loop through each sim and add only atoms that have a z coord in a particular range.
# 4) write a datafile fro those atoms.
#
######## Stack samples Main()
# folderpath = "/home/agoga/topcon/data/aSiOxSlices15/"
#     Out_Dir = "/home/agoga/topcon/MD-Analyze/output/"
    
#     offsets=[0,0,0,0,0]
#     folders=[]


#     scale=.25
       
#     files=['a-SiOx_1-1.data','a-SiOx_1-3.data','a-SiOx_1-5.data','a-SiOx_1-6.data','a-SiOx_1-8.data']

#     for f in files:
#         #folders.append('output-farm/with-v-without-h-SiO_1-5/'+f)
#         #folders.append(scaledFileName(folderpath+f,scale))
#         folders.append(folderpath+f)
            
#     sim = Stack_Samples(folders,5)
    
#     #print(sim.atoms[0].q)
#     dirs= folderpath.split('/')
#     Fname = dirs[len(dirs) - 2]
#     rl.Write_Data_WQ(Out_Dir + Fname[:-3] + ".data", sim)
def Stack_Samples(arr_of_file_names, slice_width):
    sim_container = []
    
    for file in arr_of_file_names:
        sim_container.append(rl.Read_Data(file))
    curr_offset = 0.0
    count = 1
    at_list=[]
    for sim in sim_container:
        szl=sim.box[2,0]#the current sim's zlo/zhi
        szh=sim.box[2,1]
        for at in sim.atoms:
            zcoord=at.z-szl
            if (zcoord < slice_width):

                at_list.append(atom.ATOM([count, at.type,at.q, at.x, at.y, zcoord + curr_offset]))

                count +=1
        curr_offset += slice_width
    new_sim = rl.Simulation()
    
    #print(sim_container[1].box)
    new_sim.box=sim_container[0].box
    new_sim.box[2,0]=0
    new_sim.box[2,1]=curr_offset
    
    new_sim.timestep = 0
    new_sim.num = count -1
    new_sim.atoms=at_list

    return new_sim


def Slice_Dump(dump,ts,atom,outfile):
    sim=rl.Read_Dump(dump)
    sim.timestep=10000
    

def main():
    folderpath = "/home/agoga/topcon/data/aSiOxSlices15/"
    Out_Dir = "/home/agoga/topcon/MD-Analyze/output/"
    
    offsets=[0,0,0,0,0]
    folders=[]


    scale=.25
       
    files=['a-SiOx_1-1.data','a-SiOx_1-3.data','a-SiOx_1-5.data','a-SiOx_1-6.data','a-SiOx_1-8.data']

    for f in files:
        #folders.append('output-farm/with-v-without-h-SiO_1-5/'+f)
        #folders.append(scaledFileName(folderpath+f,scale))
        folders.append(folderpath+f)
            
    sim = Stack_Samples(folders,5)
    
    #print(sim.atoms[0].q)
    dirs= folderpath.split('/')
    Fname = dirs[len(dirs) - 2]
    rl.Write_Data_WQ(Out_Dir + Fname[:-3] + ".data", sim)



if __name__ == '__main__':
    main()