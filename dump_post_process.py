from classes import Atom
from classes import Dump

dump_file_name = 'dump.airebo_stretch'
at_names = ['C','H1','H']
pos_list = ['id','type','x','y','z']

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

            data_lines = []

        if (frame_count == d1.nframes and lines == d1.nlines):
            frame_count = frame_count + 1
            print ('Finished reading frame %d'%(frame_count))
            
            d1.parse_dump_frame(data_lines,atom_dict,box_param,at_names)
            data_lines = []

        
