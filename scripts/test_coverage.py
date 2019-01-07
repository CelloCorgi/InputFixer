"""
This file will compare the coverage of the student fix and the generated fix for all scenarios 
for which a solution was found by InFixPy
"""
import sys
import coverage
import subprocess
import json
import os

def load_repair_log(log_file_path):
    """
    Loads Repiar log into a list where each sub part looks like:
        Id, Ip, foundSolution, numProbes, machineTime, studentStartTime, studentEndTime, OriginalBadInput, OriginalErrorType, FinalCorrectFix, FinalMinimized Fix, CorrectStudentInputs
    """
    log_file = open(log_file_path, 'r')
    
    tryReading = False
    to_return = []
    log_file = iter(log_file)
    for line in log_file:
        if line.startswith('SCENARIO'):
            to_return.append({})
            to_return[-1]['Id'] = line.split()[1] # Make it so it's just the file 
            tryReading = True
        elif line.startswith('File num'):
            tryReading = False
        elif tryReading:
            if line.startswith('Student Ip'):
                to_return[-1]['Ip'] = line.strip().split(": ")[-1]
            if line.startswith("Found Solution:"):
                to_return[-1]["FoundSolution"] = bool(line.strip().split(": ")[-1])
            if line.startswith("Final correct fix:"):
                to_return[-1]["MachineFix"] = json.loads(next(log_file))
            if line.startswith("Final minimized fix:"):
                to_return[-1]["MinimizedMachineFix"] = json.loads(next(log_file))
            if line.startswith("Correct Student Inputs:"):
                to_return[-1]["StudentFixes"] = json.loads(next(log_file))

        # Here, I just load all the lines so I have it -> not coverage specific in this function

    log_file.close()
    return to_return

def erase_coverage():
    try:
        subprocess.run(['coverage', 'erase'], check=True, timeout=30)
    except Exception as e:
        pass

def report_coverage():
    try:
        report = subprocess.check_output(['coverage', 'report', '-m'])
    except Exception as e:
        return None

    # Here, go through the things
    print(report)

def run_program_with_coverage(program_file_name, program_input):
    """
    This function runs coverage on the program with the given input
    """
    inputs = '\n'.join(program_input) + '\n'
    
    # now run the program
    try:
        subprocess.run(['coverage', 'run', '--include=*_code.py', '--branch',  program_file_name],
                check=True,
                timeout=60,
                input=inputs,                                   
                stdout=subprocess.PIPE,
                universal_newlines=True)
    except Exception as e:
        pass


def compare_coverage(result_info, useMinimizedFix=True):
    """
    This function sees which program -> the student or the machine gets better coverage
    Returns None if there is no student correct answer or if there was no machine correct answer
    """
    if not "MachineFix" in result_info: return None
    if not "StudentFixes" in result_info: return None
    if len(result_info["StudentFixes"]) == 0: return None 
    # If we get here, there was both a machine and a student fix
    file_name = os.path.join('/home/endremad/Projects/Python_Tutor_Input_Experiments/PythonTutor_Input_Data_Sessions', result_info['Id'], result_info['Id'] + '_code.py') 
    
    
    print(result_info)
    
    # Here, we get the coverage from the student fix
    print('Student')
    run_program_with_coverage(file_name, result_info["StudentFixes"][0][0])
    
    # And we analyze that coverage
    report_coverage()
    # And erase the coverage record
    erase_coverage()

    # Now we get the coverage from the machine fix
    print('Machine')
    run_program_with_coverage(file_name, result_info["MachineFix"])
    
    # And we analyze that coverage
    report_coverage()

    # And erase the coverage record
    erase_coverage()

    x = open(file_name, 'r')
    y = ''
    for line in x:
        y+= line

    print(y)
    print()
    print()
    print()
    return None

if __name__ == "__main__":

    # First, load the log information
    scenario_results = load_repair_log(sys.argv[-1])
    #print(scenario_results)

    # Then calculate the coverage information
    coverages = [compare_coverage(i, True) for i in scenario_results]

    # Then analyize the coverage information
    print(coverages)

