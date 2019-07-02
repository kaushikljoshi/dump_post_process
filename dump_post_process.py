from classes import Atom
from classes import Dump
import os.path
import sys

dump_file_name = 'dump.airebo_stretch'
at_names = ['C','H1','H']
pos_list = ['id','type','x','y','z']
translate = [1,1,1] #will translate/move the atoms across periodic boundaries by input numer
                    # 0 means no translation/movement

if not os.path.isfile(dump_file_name):
    print ('File not found')
    sys.exit()

d1 = Dump(filename = 'dump.airebo_stretch')
d1.find_number_of_frames()


data_lines = []
nlines = 0
frame_count = 0

with open(dump_file_name,'r') as if1:
    for line in if1:
        data_lines.append(line)
        nlines = nlines + 1

        if (frame_count < d1.nframes-1 and nlines == d1.frame_start_lines[frame_count+1]-1):
            frame_count = frame_count + 1
            print ('Finished reading frame %d'%(frame_count))

            atom_dict = {}
            box_param = {}

            d1.parse_dump_frame(data_lines,atom_dict,box_param,at_names)
            
            if (sum(translate) != 0):
                d1.translate(translate,atom_dict,box_param)
            
            d1.write_xyz(atom_dict,box_param,translate,frame_count)

            data_lines = []
            atom_dict = {}
            box_param = {}

        if (frame_count == d1.nframes and lines == d1.nlines):
            frame_count = frame_count + 1
            print ('Finished reading frame %d'%(frame_count))
            
            d1.parse_dump_frame(data_lines,atom_dict,box_param,at_names)

            if (sum(translate) != 0):
                d1.translate(translate,atom_dict,box_param)
            
            d1.write_xyz(atom_dict,box_param,translate,frame_count)
            
            data_lines = []
            atom_dict = {}
            box_param = {}

        
