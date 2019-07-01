x_name_list = ['x','xs','xu','xsu']
y_name_list = ['y','ys','yu','ysu']
z_name_list = ['z','zs','zu','zsu']


class Atom():

    def __init__(self, coordinates =None, velocities=None, names=None, charge=None, number=None):
        if coordinates is None:
            self.coordinates = []
        else:
            self.coordinates = coordinates

        if velocities is None:
            self.velocities = []
        else:
            self.velocities = velocities

        if names is None:
            self.names = []
        else:
            self.names = names

        if charge is None:
            self.charge = 0.0
        else:
            self.charge = 0.0

        if number is not None:
            self.number = number


class Dump():

    def __init__(self,filename = None, pos_list = None):
        self.nframes = 0
        self.nlines = 0
        self.frame_start_lines = []
        self.pos_dict = {}
        self.natoms = 0
        
        if filename is not None:
            self.filename = filename

        if pos_list is None:
            self.pos_list = []
            self.pos_dict = {}
        else:
            self.pos_list = pos_list
            self.pos_dict = {}

    def find_number_of_frames(self):
        with open(self.filename,'r') as if1:
            for line in if1:
                self.nlines = self.nlines + 1
                line1 = line.split()
                if (len(line1) > 1):
                    if (line1[0] == "ITEM:" and line1[1] == "TIMESTEP"):
                        self.nframes = self.nframes + 1
                        self.frame_start_lines.append(self.nlines)


    def parse_dump_frame(self,data_lines,atom_dict,box_params,at_names):
        
        tstep_falg = 0
        noa_flag = 0
        atoms_flag = 0
        box_flag = 0

        for line in data_lines:
            line1 = line.split()
            if (line1[0] == "ITEM:" and line1[1] == "TIMESTEP"):
                tstep_flag = 1
                continue
            
            if (line1[0] == "ITEM:" and line1[1] == "NUMBER"):
                noa_flag = 1
                continue
            
            if (line1[0] == "ITEM:" and line1[1] == "BOX"):
                box_flag = 1
                box_count = 0
                lxyz = []
                continue
            
            if (line1[0] == "ITEM:" and line1[1] == "ATOMS"):
                atoms_flag = 1
                atom_count = 0
                for i1 in range(2,len(line1)):
                    if line1[i1] in x_name_list:
                        self.pos_dict['x'] = i1-2
                    elif line1[i1] in y_name_list:
                        self.pos_dict['y'] = i1-2
                    elif line1[i1] in z_name_list:
                        self.pos_dict['z'] = i1-2
                    else:
                        self.pos_dict[line1[i1]] = i1-2

                if 'type' not in self.pos_dict.keys():
                    print ('Cannot convert dump into xyz without atom type number')
                    sys.exit()
                if 'id' not in self.pos_dict.keys():
                    print ('Warning: Atom ids not present in provided dump structure')
                
                continue

            if (tstep_flag == 1):
                tstep_flag = 0
                self.tstep = int(line1[0])
                
            if(box_flag == 1):
                
                if (box_count == 0):
                    box_params['xlo'] = float(line1[0])
                    box_params['xhi'] = float(line1[1])
                    if (len(line1) == 3):
                        box_params['xy']= float(line1[2])
                    box_count = box_count + 1
                    
                elif (box_count == 1):
                    box_params['ylo'] = float(line1[0])
                    box_params['yhi'] = float(line1[1])
                    if (len(line1) == 3):
                        box_params['xz']= float(line1[2])
                    box_count = box_count + 1

                else:
                    box_params['zlo'] = float(line1[0])
                    box_params['zhi'] = float(line1[1])
                    if (len(line1) == 3):
                        box_params['yz']= float(line1[2])
                    box_count = box_count + 1
                
                if (box_count == 3):
                    box_flag = 0

            if (noa_flag == 1):
                noa_flag = 0
                self.natoms = int(line1[0])


            if (atoms_flag == 1):
                temp_list = []
                if 'id' in self.pos_dict.keys():
                    at_id = int(line1[self.pos_dict['id']])
                else:
                    at_id = count

                n1 = int(line1[self.pos_dict['type']])

                temp_list.append(float(line1[self.pos_dict['x']]))
                temp_list.append(float(line1[self.pos_dict['y']]))
                temp_list.append(float(line1[self.pos_dict['z']]))
                temp_list.append(int(line1[self.pos_dict['type']]))
                temp_list.append(at_names[n1-1])
                atom_dict[at_id] = Atom(coordinates =temp_list[0:3], names=temp_list[3:5], number=at_id)

                atom_count = atom_count + 1

                if (atom_count == self.natoms):
                    atoms_flag = 0
        
    def write_xyz(self,atom_dict,box_params,translate,fr_count):
        
        if (fr_count == 1):
            of1 = open('output.xyz','w')
        else:
            of1 = open('output.xyz','a')
        
        of1.write('%d\n'%(self.natoms))
        of1.write('%f %f '%(box_params['xlo'],box_params['xhi']))
        of1.write('%f %f '%(box_params['ylo'],box_params['yhi']))
        of1.write('%f %f '%(box_params['zlo'],box_params['zhi']))
        of1.write('90 90 90\n')

        for key in atom_dict:
            of1.write('%s '%(atom_dict[key].names[1]))
            of1.write('%f '%(atom_dict[key].coordinates[0]))
            of1.write('%f '%(atom_dict[key].coordinates[1]))
            of1.write('%f\n'%(atom_dict[key].coordinates[2]))

        of1.close()

    def translate(self,translate,atom_dict):

        #Following set of equations are valid only for orthogonal boxes
        #Needs to updated in the future to take into account non-orthogonality
        
        lx = box_params['xhi'] - box_params['xlo']
        ly = box_params['yhi'] - box_params['ylo']
        lz = box_params['zhi'] - box_params['zlo']

        
        #Check for mapping in x,y and z directions
        #For each direction, update atom coordinates first and then box parameters. 
        if (translate[0] == 1):
            for key in atom_dic:
                if (atom_dict[key].coordinates[0] > box_params['xlo']+lx/2.0):
                    atpm_dict[key].coordinates[0] = atom_dict[key].coordinates[0] + lx
            box_params['xlo'] = box_params['xlo'] + lx/2.0
            box_params['xhi'] = box_params['xhi'] + lx/2.0

        if (translate[1] == 1):
            for key in atom_dic:
                if (atom_dict[key].coordinates[1] > box_params['ylo']+ly/2.0):
                    atom_dict[key].coordinates[1] = atom_dict[key].coordinates[1] + ly
            box_params['ylo'] = box_params['ylo'] + ly/2.0
            box_params['yhi'] = box_params['yhi'] + ly/2.0

        if (translate[1] == 2):
            for key in atom_dic:
                if (atom_dict[key].coordinates[2] > box_params['zlo']+lz/2.0):
                    atom_dict[key].coordinates[2] = atom_dict[key].coordinates[2] + lz
            box_params['zlo'] = box_params['zlo'] + lz/2.0
            box_params['zhi'] = box_params['zhi'] + lz/2.0
        
        
