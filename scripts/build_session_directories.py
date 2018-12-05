input_data_json = "all_inputs_with_timestamp.json"

session_meta_directory_path = "/home/endremad/Projects/Python_Tutor_Input_Experiments/"

session_meta_directory_name = "PythonTutor_Input_Data_Sessions"

########## UNLESS INPUT FORMAT CHANGES, DON'T NEED TO MODIFY BELOW HERE ##########

import json
import sys
import os
import subprocess
import shutil
from collections import defaultdict
test_folder = session_meta_directory_path + session_meta_directory_name

# Load the input data
with open(input_data_json, 'r') as in_file:
    raw_data = json.loads(next(in_file))

print(raw_data[0])
ids = defaultdict(int)
for session_name_base, program, inputs in raw_data:
    session_name_base = session_name_base + '_'
    
    # First Make a list of all the fixes and errors
    correct_inputs = []
    bad_inputs = []
    for ip in inputs:
        if ip[1] == 'bad': bad_inputs.append(ip)
        else: correct_inputs.append((ip[0], ip[5]))
    
    # Then go through each bad and make a file for it
    for bad in bad_inputs:
        session_name = session_name_base + str(ids[session_name_base])
        ids[session_name_base] += 1
        session_folder = test_folder + '/' + session_name
        if os.path.exists(session_folder):
            #os.removedirs(session_folder)
            shutil.rmtree(session_folder)
        os.makedirs(session_folder)
        
        # Add all the files to each folder as needed
        with open(session_folder + '/' + session_name + '_code.py', 'w') as out:
            out.write(program)
        with open(session_folder + '/' + session_name + '_bad_input.txt', 'w') as out:
            out.write('\n'.join(bad[0]) + '\n')
        with open(session_folder + '/' + session_name + '_additional_info.json', 'w') as out:
            out.write(json.dumps(
                {'CorrectInputs': correct_inputs,
                 'BadInput': bad[0],
                 'ErrorType' : bad[2],
                 'ErrorMessage' : bad[3],
                 'ip' : bad[4],
                 'TimeStamp' : bad[5],
                 'UniqueId' : session_name,
                 'LastIsEmpty': (bad[0][-1] == "")}))
