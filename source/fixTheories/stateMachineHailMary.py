"""
This is a hail mary approach based off my state machine idea
"""
from datetime import datetime
import json
import time
import os
import subprocess
from copy import deepcopy
import random
import string


class StateMachine:

    def __init__(self, global_config, log):
        self.isFirst = True
        log.write(str(global_config))
        self.log = log
        #TODO: Make versions of representation, fault, fix, operators, and search stratagy
        print(global_config)
        self.max_num_fix = global_config["MaxNumFix"]
        self.max_num_probe = global_config["MaxNumProbes"]
        self.num_tried = 0
        self.num_fixed = 0
        self.bad_input_cache = ['']

    def find_location_in_input(self, bad_input, error_message):
        """
        This function searches backwards and returns the index of the element that should be replaced
        TODO: Make it find all instances if possible?
        """
        
        stripped_error = error_message.strip()
        #stripped_error = stripped_errpr[stripped_error.find('Error:'):]
        last_element = stripped_error[-1]
        
        to_look_for = stripped_error[stripped_error.find(last_element)+1:-1]
        print(stripped_error)
        print('to look for: ' + str(to_look_for))
        print(len(to_look_for))

        for i, e in reversed(list(enumerate(bad_input))):
            if len(to_look_for) == 0 and len(e) == 0:
                return i, 0, 0

            element_index = e.rfind(to_look_for)
            if element_index >= 0:
                return (i, element_index, len(to_look_for))
        
        # If not found, do a random one
        rand_row = random.randint(0, len(bad_input) - 1)
        return rand_row, 0, len(bad_input[rand_row])

    def start_timer(self):
        #self.start_time = datetime.utcnow() 
        self.start_time = time.time()

    def end_timer(self):
        #self.end_time = datetime.utcnow()
        self.end_time = time.time()

    def scan_input_for_type(self, bad_input, type_t, findAll=False):
        """
        This function returns the last element in the bad input to have that type (or all if findAll is true)
        """
        pass

    def gen_random_string(self, length):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.digits + '--') for _ in range(length))

    def random_mutation(self, bad_input):
        """
        If this function is called, the bad input string is randomly mutated
        """
        #TODO: Modify so random token generator will generate tokens from the source code
        # First, figure out which broad one to do
        # First pick a line to operate on
        if len(bad_input) == 0:
            bad_input.append(self.gen_random_string(3))
            return bad_input
        
        operation_line = random.randint(0, len(bad_input) - 1)

        # Now, see if this line can be broken into tokens
        split_version = bad_input[operation_line].split()
        #TODO: MAKE THIS MORE EFFICIENT
        if len(split_version) <= 1:
            # Then here, we either add, delete, or swap
            operation_choice = random.randint(0, 5)
            if operation_choice == 0:
                bad_input = []
            elif operation_choice == 1:
                bad_input.pop(operation_line)
            elif operation_choice == 2:
                bad_input.insert(operation_line, random.choice(bad_input + self.input_history[0] + self.input_history[0] + self.input_history[0]))
            elif operation_choice == 3:
                bad_input.insert(operation_line, random.choice(self.bad_input_cache))
            elif operation_choice == 4:
                bad_input.insert(operation_line, self.gen_random_string(3))
            elif operation_choice == 5:
                bad_input[operation_line] = bad_input[operation_line] + ' ' + self.gen_random_string(3)
        else:
            operation_choice = random.randint(0, 4)
            if operation_choice == 0:
                bad_input[operation_line] = ''
            elif operation_choice == 1:
                bad_input.pop(operation_line)
                bad_input[operation_line:operation_line] = split_version
            elif operation_choice == 2:
                split_version[random.randint(0, len(split_version) - 1)] = random.choice(bad_input + self.input_history[0])
                bad_input[operation_line] = ' '.join(split_version)
            elif operation_choice == 3:
                split_version[random.randint(0, len(split_version) - 1)] = self.gen_random_string(3)
                bad_input[operation_line] = ' '.join(split_version)
            elif operation_choice == 4:
                split_version[random.randint(0, len(split_version) - 1)] = random.choice(self.bad_input_cache)
                bad_input[operation_line] = ' '.join(split_version)

        return bad_input

    def init_scenario(self, session_config):
        self.input_history = []
        self.num_tried += 1
        self.found_solution = False
        if len(session_config["BadInput"]) > 15:
            self.bad_input_cache.extend(session_config["BadInput"][:15])
        elif session_config["BadInput"][-1] == '':
            self.bad_input_cache.extend(session_config["BadInput"][-1])
        else:
            self.bad_input_cache.extend(session_config["BadInput"])
    
    def fix(self, session_config, scenario_folder_path, log):
        """
        This is the only method that should be called from outside this file
        It runs the overall fixer
        """
        self.init_scenario(session_config)
        
        # Convert the bad input into its modifiable datastructure form -> a list of lists
        print(session_config)
        bad_input = deepcopy(session_config["BadInput"])

        # Initialize the cache with the original bad, so we don't try the same result twice
        cache = {str(bad_input)}

        num_fixes_found = 0
        num_probes_made = 0
        last_error_type = session_config["ErrorType"]
        last_error_message = session_config["ErrorMessage"]
        last_error_message = last_error_message[last_error_message.find(last_error_type) + len(last_error_type):]
        print(last_error_message)

        self.log.write('ORIGINAL BAD INPUT: {}\n'.format(bad_input))
        self.log.write('ORIGINAL ERROR: {} :-:-: {}\n'.format(last_error_type, last_error_message))
        
        # Record the starting time
        self.start_timer()
        
        while num_fixes_found < self.max_num_fix and num_probes_made < self.max_num_probe:
            if last_error_type == "" or last_error_type == ":":
                num_probes_made = self.max_num_probe
                self.log.write('NOTE: PROGRAM HAS NO ERROR MESSAGE, SO BEING SKIPPED\n')
                return

            self.input_history.append(deepcopy(bad_input))
            
            # Take a look at the error message associated with this guy
            # TODO: Deal with making deep copies of the bad input
            if last_error_type  == "ValueError":
                
                #TODO: Don't have this fault location always be the last input line
                # First look for values to unpack
                if last_error_message.find('too many values to unpack') >= 0:
                    split_last = bad_input[-1].strip().split()
                    bad_input[-1] = ' '.join(split_last[:-1])

                elif last_error_message.find("not enough values to unpack") >= 0:
                    if len(bad_input) == 0: bad_input.append('')
                    split_last = bad_input[-1].strip().split()
                    if len(split_last) > 15:
                        bad_input = bad_input[:-1]
                    
                    else:
                        if len(split_last) > 0:
                            split_last.append(split_last[-1])
                        else:
                            split_last = [self.gen_random_string(3)]
                        bad_input[-1] = ' '.join(split_last)

                elif last_error_message.find("invalid literal for int()") >= 0:
                    if len(bad_input) == 0:
                        bad_input = [str(random.randint(-1, 15))]
                    else:
                        #TODO: DEAL WIITH TEMPLATE
                        line, i, l = self.find_location_in_input(bad_input, last_error_message)
                        bad_input[line] = bad_input[line][:i] + str(random.randint(0, 10)) + bad_input[line][i + l:]

                elif last_error_message.find("could not convert string to float") >= 0:
                    # First, localize the error
                    if len(bad_input) == 0:
                        bad_input = [str(random.randint(-1, 15)) + '.' + str(random.randint(0, 100))]
                    else:
                        #TODO: DEAL WIITH TEMPLATE
                        line, i, l = self.find_location_in_input(bad_input, last_error_message)
                        bad_input[line] = bad_input[line][:i] + str(random.randint(-1, 15)) + '.' + str(random.randint(0, 100))+ bad_input[line][i + l:]

            elif last_error_type == "EOFError":
                # In this case, repete the last line
                # TODO: Make this work better in the future
                if len(bad_input) > 0:
                    bad_input.append(random.choice(bad_input + self.input_history[0] + [self.gen_random_string(3)]))
                else:
                    bad_input.append(self.gen_random_string(3))
            
            # If the input is in the cache at this point or nothing was done before, we need to keep trying to modify it
            while str(bad_input) in cache:
                bad_input = self.random_mutation(bad_input)

            print(num_probes_made)
            print(scenario_folder_path)
            # Ok, now add the modified version back into the cache
            cache.add(str(bad_input))

            # Next, log what I am doing
            num_probes_made += 1
            self.log.write("Trying input num {}: Input is {}\n".format(num_probes_made, bad_input))

            # Next, test this input and see if it does better or worse
            #print(session_config)
            program_file_name = os.path.join(scenario_folder_path, session_config['UniqueId'] + '_code.py')
            last_error_type, last_error_message, full_error = self.try_program(program_file_name, bad_input)

            if last_error_type is None:
                self.log.write('SOLVED THE ERROR\n')
                num_fixes_found += 1
                print("SOLVED THE ERROR")
                self.found_solution = True
                self.final_input = bad_input
                self.minimized_input = self.minimize(program_file_name, deepcopy(bad_input))
                self.num_fixed += 1
            else:
                self.log.write('STILL HAS ERROR: {} :-:-: {}\n'.format(last_error_type, last_error_message))

        
        # At this point, we have finished all of our probes for this scenario. It's time for cleanup
        # Record the ending time
        self.end_timer()
        self.wrap_up_scenario_log(session_config, num_probes_made)
        
        print("Num tried: {}".format(self.num_tried))
        print("Num fixed: {}".format(self.num_fixed))

    def wrap_up_scenario_log(self, scenario_config, num_probes_made):
        self.log.write('\nSCENARIO {} WRAP_UP:\n'.format(scenario_config['UniqueId']))
        self.log.write('Student Ip: {}\n'.format(scenario_config['ip']))
        self.log.write('Found Solution: {}\n'.format(self.found_solution))
        self.log.write('Number of Probes made: {}\n'.format(num_probes_made))
        self.log.write('Start time: {}\n'.format(self.start_time))
        self.log.write('End time: {}\n'.format(self.end_time))
        self.log.write('Student bad input start time: {}\n'.format(scenario_config['TimeStamp']))
        print(self.end_time)
        # See if the student had a good input after the bad input
        for correct_input in scenario_config['CorrectInputs']:
            if correct_input[1] > scenario_config['TimeStamp']:
                self.log.write('Student next fix time: {}\n'.format(correct_input[1]))
                break
        self.log.write('Original bad input: {}\n'.format(scenario_config['BadInput']))
        self.log.write('Original Error Type: {}\n'.format(scenario_config["ErrorType"]))
        if self.found_solution:
            self.log.write('Final correct fix: \n{}\n'.format(json.dumps(self.final_input)))
            self.log.write('Final correct minimized fix: \n{}\n'.format(json.dumps(self.minimized_input)))
        self.log.write('Correct Student Inputs: \n{}'.format(json.dumps(scenario_config['CorrectInputs'])))
        self.log.write("\nNum scenario tried: {}\n".format(self.num_tried))
        self.log.write("Num scenario fixed: {}\n".format(self.num_fixed))
        self.log.write('\n\n\n')

    def try_program(self, program_file_name, program_input):
        """
        This function runs the program with the specidied input and sees if it errors out or not
        """
        inputs = '\n'.join(program_input) + '\n'
        
        print('Program Input: {}'.format(program_input))
        # Now run the program:
        run_result = None
        error_last_line = None
        full_error = None
        try:
            subprocess.run(['python3', program_file_name],
                    check=True,
                    timeout=5,
                    input=inputs,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True)
        except Exception as e:
            print(e.stderr)
            full_error = e.stderr
            important = e.stderr.strip().split('\n')[-1].strip()
            run_result = important[:important.find(':')]
            error_last_line = important[important.find(':'):]
        return run_result, error_last_line, full_error

    def minimize(self, program_file_name, program_input):
        """
        Assumes program_input is a working input
        """
        
        if (len(program_input)) == 0:
            return program_input

        result, _, _ = self.try_program(program_file_name, program_input[:-1])

        if result is not None:
            return program_input
        else:
            return self.minimize(program_file_name, program_input[:-1])
