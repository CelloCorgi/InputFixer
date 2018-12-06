# This script just looks at the loog file stuff for time stamps

import sys

log_file = sys.argv[1]

lf = open(log_file, 'r')
# First read the logfile in
lf_lines = []
for line in lf:
    if line.startswith("SCENARIO") or line.startswith('Found Solution') or line.startswith('Number of Probes made') or line.startswith('Start time: ') or line.startswith('End time: ') or line.startswith('Student '):
           lf_lines.append(line)
lf.close()
lf_lines.extend(["1", "1", "1", "2"])
total_num_inputs = 0
total_num_solutions = 0
total_num_probes = 0
total_num_has_student_fix_time = 0

total_student_time_for_solved = 0
total_machine_time_for_solved = 0

total_student_time_for_unsolved = 0
total_machine_time_for_unsolved = 0

for i in range(len(lf_lines)):
    if lf_lines[i].startswith("SCENARIO") and lf_lines[i + 7].startswith("Student next fix "):
        
        total_num_inputs += 1
        machine_start_time = float(lf_lines[i + 4].strip().split(": ")[-1])
        machine_end_time = float(lf_lines[i + 5].strip().split(": ")[-1])
        machine_time = machine_end_time - machine_start_time

        student_start_time = int(lf_lines[i + 6].strip().split(": ")[-1])
        student_end_time = int(lf_lines[i + 7].strip().split(": ")[-1])
        student_time = student_end_time - student_start_time
        
        
        if lf_lines[i + 2].find("True") >= 0:
            total_num_solutions += 1
            total_num_probes += int(lf_lines[i + 3].strip().split(": ")[-1])
            total_student_time_for_solved += student_time
            total_machine_time_for_solved += machine_time

        else:
            total_student_time_for_unsolved += student_time
            total_machine_time_for_unsolved += machine_time

print("Total num inputs: {}".format(total_num_inputs))
print("Total num solutions: {}".format(total_num_solutions))
print("Total num probes for solved: {}".format(total_num_probes))
print("Total student time for solved: {}".format(total_student_time_for_solved))
print("Total machine time for solved: {}".format(total_machine_time_for_solved))
print("Total student time for unsolved: {}".format(total_student_time_for_unsolved))
print("Total machine time for unsolved: {}".format(total_machine_time_for_unsolved))
