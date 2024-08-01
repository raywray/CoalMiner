import os

def find_lhoods(num_of_sims, prefix):
    results = []

    # iterate through each run
    for i in range(1, num_of_sims + 1):
        best_lhoods_filepath = f"output/run_{i}/{prefix}/{prefix}.bestlhoods"

        # check if file exists (it won't if the parameters are "bad")
        if os.path.exists(best_lhoods_filepath):
            # find best lhood & add to results
            with open(f"{best_lhoods_filepath}", "r") as best_lhoods_file:
                header = next(best_lhoods_file).split()
                max_est_index = header.index("MaxEstLhood")
                values = next(best_lhoods_file).split()
                max_est_lhood = values[max_est_index]
                results.append((i, max_est_lhood))
    
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    return sorted_results


def get_best_fit_model(results, output_dir):
    with open(f"{output_dir}/best_lhood_results.txt", "w") as results_file:
        for result in results:
            results_file.write(f"{result[0]} {result[1]}\n")
    if not results:
        best_fit_run = "NA"
    else:
        best_fit_run = results[0][0]
    return best_fit_run


def get_best_lhoods(num_of_sims, input_prefix, output_dir):
    best_lhood_resuls = find_lhoods(num_of_sims, input_prefix)
    best_fit_run = get_best_fit_model(best_lhood_resuls, output_dir)

    return best_fit_run
