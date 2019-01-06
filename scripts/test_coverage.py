"""
This file will compare the coverage of the student fix and the generated fix for all scenarios 
for which a solution was found by InFixPy
"""
import sys
import coverage
import subprocess
import json


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


if __name__ == "__main__":

    # First, load the log information
    scenario_results = load_repair_log(sys.argv[-1])
    print(scenario_results)
    # Then calculate the coverage information

    # Then analyize the coverage information
