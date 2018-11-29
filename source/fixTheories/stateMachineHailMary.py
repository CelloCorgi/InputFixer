"""
This is a hail mary approach based off my state machine idea
"""
import datetime
import os
import subprocess

class StateMachine:

    def __init__(self, global_config, log):
        self.isFirst = True
        log.write(str(global_config))
        self.log = log
        #TODO: Make versions of representation, fault, fix, operators, and search stratagy
        print(global_config)
        self.max_num_fix = global_config["MaxNumFix"]
        self.max_num_probe = global_config["MaxNumProbes"]

    def fix(self, session_config, scenario_folder_path, log):
        """
        This is the only method that should be called from outside this file
        It runs the overall fixer
        """

        # Convert the bad input into its modifiable datastructure form -> a list of lists
        print(session_config)
        bad_input = session_config["BadInput"]

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

        while num_fixes_found < self.max_num_fix and num_probes_made < self.max_num_probe:
            
            # Take a look at the error message associated with this guy
            
            if last_error_type  == "ValueError":
                pass
            elif last_error_type == "EOFError":
                pass
            
            # If the input is in the cache at this point or nothing was done before, we need to keep trying to modify it
            """
            while str(bad_input) in cache:
                 # Do random mutations
                 continue
            """
            print(num_probes_made)
            print(scenario_folder_path)
            # Ok, now add the modified version back into the cache
            cache.add(str(bad_input))

            # Next, log what I am doing
            num_probes_made += 1
            self.log.write("Trying input num {}: Input is {}\n".format(num_probes_made, bad_input))

            # Next, test this input and see if it does better or worse
            print(session_config)
            program_file_name = os.path.join(scenario_folder_path, session_config['UniqueId'] + '_code.py')
            last_error_type, last_error_message = self.try_program(program_file_name, bad_input)

            if last_error_type is None:
                self.log.write('Sucsessfully fixed error\n')
                num_fixes_found += 1
            
            else:
                self.log.write('ERROR: {} :-:-: {}\n'.format(last_error_type, last_error_message))

            # Finally, either change the bad inputs, modify weights, or nothing and try again
        
        # Record the ending time
        elapsed_time = datetime.datetime.now() - self.start_time
        self.log.write("The time elapsed was {}".format(elapsed_time))

    def try_program(self, program_file_name, program_input):
        inputs = '\n'.join(program_input) + '\n'

        # Now run the program:
        run_result = None
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
            important = e.stderr.strip().split('\n')[-1].strip()
            run_result = important[:important.find(':')]
            full_error = important[important.find(':'):]
        return run_result, full_error
