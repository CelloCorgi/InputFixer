"""
This is a hail mary approach based off my state machine idea
"""
import datetime
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

    def find_location_in_input(self, bad_input, element_to_find):
        """
        This function searches backwards and returns the index of the element that should be replaced
        TODO: Make it find all instances if possible?
        """
        for i, e in reversed(list(enumerate(bad_input))):
            element_index = e.rfind(element_to_find)
            if element_index >= 0:
                return (i, element_index)

        return None

    def replace_element(self):
        pass

    def scan_input_for_type(self, bad_input, type_t, findAll=False):
        """
        This function returns the last element in the bad input to have that type (or all if findAll is true)
        """
        pass

    def random_mutation(self, bad_input):
        """
        If this function is called, the bad input string is randomly mutated
        """
        #TODO: Modify so random token generator will generate tokens from the source code
        # First, figure out which broad one to do
        # First pick a line to operate on
        if len(bad_input) == 0:
            bad_input.append(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)))
            return bad_input
        
        operation_line = random.randint(0, len(bad_input) - 1)

        # Now, see if this line can be broken into tokens
        split_version = bad_input[operation_line].split()

        if len(split_version) <= 1:
            # Then here, we either add, delete, or swap
            operation_choice = random.randint(0, 3)
            if operation_choice == 0:
                bad_input = []
            elif operation_choice == 1:
                bad_input.pop(operation_line)
            elif operation_choice == 2:
                bad_input.insert(operation_line, random.choice(bad_input + self.input_history[0]))
            elif operation_choice == 3:
                bad_input.insert(operation_line, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)))
  
        else:
            operation_choice = random.randint(0, 3)
            if operation_choice == 0:
                bad_input[operation_line] = ''
            elif operation_choice == 1:
                bad_input.pop(operation_line)
                bad_input[operation_line:operation_line] = split_version
            elif operation_choice == 2:
                split_version[random.randint(0, len(split_version) - 1)] = random.choice(bad_input + self.input_history[0])
                bad_input[operation_line] = ' '.join(split_version)
            elif operation_choice == 3:
                split_version[random.randint(0, len(split_version) - 1)] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
                bad_input[operation_line] = ' '.join(split_version)        
        return bad_input
    
    def fix(self, session_config, scenario_folder_path, log):
        """
        This is the only method that should be called from outside this file
        It runs the overall fixer
        """
        
        self.input_history = []
        self.num_tried += 1

        # Convert the bad input into its modifiable datastructure form -> a list of lists
        print(session_config)
        bad_input = deepcopy(session_config["BadInput"])

        # Initialize the cache with the original bad, so we don't try the same result twice
        cache = {str(bad_input)}

        # Record the starting time
        self.start_time = datetime.datetime.now()
        
        # Loop through and try to find fixes
        num_fixes_found = 0
        num_probes_made = 0
        last_error_type = session_config["ErrorType"]
        last_error_message = session_config["ErrorMessage"]
        last_error_message = last_error_message[last_error_message.find(last_error_type) + len(last_error_type):]
        print(last_error_message)
        self.log.write('The original bad input: {}\n'.format(bad_input))

        while num_fixes_found < self.max_num_fix and num_probes_made < self.max_num_probe:
            
            self.input_history.append(deepcopy(bad_input))
            # Take a look at the error message associated with this guy
            # TODO: Deal with making deep copies of the bad input
            if last_error_type  == "ValueError":
                print("I'm REALLY HERE")    
                # First look for values to unpack
                if last_error_message.find('too many values to unpack') >= 0:
                    
                    # First split the last guy into tokens
                    split_last = bad_input[-1].strip().split()
                    bad_input[-1] = ' '.join(split_last[:-1])

                elif last_error_message.find("not enough values to unpack") >= 0:
                    if len(bad_input) == 0: bad_input.append('')
                    split_last = bad_input[-1].strip().split()
                    print("SPLIT LAST {}".format(split_last))
                    if len(split_last) > 0:
                        split_last.append(split_last[-1])
                    else:
                        split_last = ['1']
                    bad_input[-1] = ' '.join(split_last)

                elif last_error_message.find("invalid literal for int()") >= 0:
                    if len(bad_input) > 0:
                        bad_input[-1] = '5'
                    else:
                        bad_input = ['5']

                elif last_error_message.find("could not convert string to float") >= 0:
                    # First, localize the error

                    # See if fits template

                    # If not, random generate
                    
                    if len(bad_input) > 0:
                        bad_input[-1] = '3.3'
                    else:
                        bad_input = ['3.3']

            elif last_error_type == "EOFError":
                
                # In this case, repete the last line
                # TODO: Make this work better in the future
                if len(bad_input) > 0:
                    bad_input.append(random.choice(bad_input))
                else:
                    bad_input.append(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)))

            
            elif last_error_type == "" or last_error_type == ":":
                num_probes_made += 1
                continue
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
                self.log.write('Sucsessfully fixed error\n')
                num_fixes_found += 1
                print("SOLVED THE ERROR")
                print(self.minimize(program_file_name, bad_input))
                self.num_fixed += 1
            else:
                self.log.write('ERROR: {} :-:-: {}\n'.format(last_error_type, last_error_message))

            # Finally, either change the bad inputs, modify weights, or nothing and try again
            print(bad_input)
            print(session_config)
        # Record the ending time
        elapsed_time = datetime.datetime.now() - self.start_time
        self.log.write("The time elapsed was {}".format(elapsed_time))
        
        print("Num tried: {}".format(self.num_tried))
        print("Num fixed: {}".format(self.num_fixed))

    def try_program(self, program_file_name, program_input):
        """
        This function runs the program with the specidied input and sees if it errors out or not
        """
        inputs = '\n'.join(program_input) + '\n'

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

        if result == None:
            return program_input[:-1]
        else:
            return self.minimize(program_file_name, program_input[:-1])
