"""
This file analyzes the new log format where everything is a json output
"""
import sys
import json
import statistics

def analyze_base_inFix():
    pass

def analyze_best_coverage(results, num_runs):
    """
    This function examines the best coverage run out of num_runs for each scenario
    """
    num_solutions_found = [0] * num_runs
    coverage_of_machine_solutions = [[] for x in range(num_runs)]
    has_max_coverage = [0 for x in range(num_runs)]
    maximum_coverage = []
    total_scenarios_with_at_least_one_solution = 0
    total_scenarios = 0
    for result in results:
        meta_data = result[0]
        experiment_results = result[1]
        if meta_data["ErrorMessage"] == "" or meta_data["ErrorMessage"] == ":":
            continue
        total_scenarios += 1
        
        # If not all blank, loop and see which ones solved
        max_coverage = 0
        max_index = -1
        has_solution = False
        for i in range(num_runs):
            run = experiment_results[i]
            if len(run) == 0: continue
            
            # If this experiment found a solution
            if run["FoundSolution"]:
                num_solutions_found[i] += 1
                has_solution = True
                if run["FinalCoverage"] is not None:
                    cov_result = int(run["FinalCoverage"][4][:-1])
                    coverage_of_machine_solutions[i].append(cov_result)
                    if cov_result > max_coverage:
                        max_coverage = cov_result
                        max_index = i
        if max_index >= 0:
            has_max_coverage[max_index] += 1
            maximum_coverage.append(max_coverage)

        if has_solution:
            total_scenarios_with_at_least_one_solution += 1
    
    print(num_solutions_found)
    print(total_scenarios)
    print(total_scenarios_with_at_least_one_solution)
    print(has_max_coverage)

    print('Maximum Coverage: {} {} {}'.format(statistics.mean(maximum_coverage), statistics.median(maximum_coverage), statistics.stdev(maximum_coverage))) 
    print('\nIndividual ones:')
    for x in coverage_of_machine_solutions:
        print('{} {} {}'.format(statistics.mean(x), statistics.median(x), statistics.stdev(x)))

def read_json_log(log_file):
    """
    General function for loading a json based log
    """
    with open(log_file, 'r') as f:
        f = iter(f)
        to_return = []
        for line in f:
            if line.startswith('NEXT'):
                general_config = json.loads(next(f))
                experiment_results = json.loads(next(f))
                to_return.append([general_config, experiment_results])
        return to_return

if __name__ == "__main__":
    # First, deal with the command line file
    log_file = sys.argv[-1]

    # Now read in the log file
    results = read_json_log(log_file)

    # Now analyze for the specific global config
    analyze_best_coverage(results, 5)
