import os

isMacbook = False
if isMacbook:
    base_path = "/Users/raya/Documents/School"
else:
    base_path = "/home/raya/Documents/Projects"

FSC_PROJECT_PATH = os.path.join(base_path, "fscWrapper")
UTILITIES_PATH = os.path.join(FSC_PROJECT_PATH, "utilities")


def run_script(script_command):
    result = os.system(script_command)
    if result != 0:
        print("SCRIPT FAILED TO EXECUTE********************")
    else:
        print("SCRIPT SUCCESSFULLY EXECUTED****************")


def model_comp_with_aic(path_to_best_max_est_run, prefix):
    # the folder in the path must have the .bestlhoods and the .est (might have to move the .est in manually)
    # output is saved as {prefix}.AIC
    """
    cd bestrun/
    calculateAIC.sh early_geneflow

    # Usage: calculateAIC.sh modelprefix
    # This script calculates AIC from fsc modeling results
    # Run in the folder with the highest likelihood
    """

    # move in est file to the /prefix dir
    est_file_path = os.path.join(path_to_best_max_est_run, f"{prefix}.est")
    best_run_prefix_folder = os.path.join(path_to_best_max_est_run, f"{prefix}")

    os.system(f"cp {est_file_path} {best_run_prefix_folder}")

    # run the aic
    aic_executable = os.path.join(UTILITIES_PATH, "calculateAIC.sh")

    os.chdir(best_run_prefix_folder)
    print("TRYING AIC CALCULATION**********************")
    run_script(f"{aic_executable} {prefix}")
    # the output will the in the working directory under {prefix}.AIC


def extract_number_of_samples(filename):
    with open(filename, "r") as file:
        for line in file:
            # Remove leading and trailing whitespace from each line
            line = line.strip()
            # Check if the line starts with "//Number of population samples"
            if line.startswith("//Number of population samples (demes)"):
                number_of_samples = next(file).strip()
                return int(number_of_samples)

    # Return None if the line is not found
    return None


def visualize_best_fit_model(path_to_best_run, prefix):
    # the .tpl has to be in this folder, as well as the .obs sfs's
    """
    SFStools.r -t print2D -i early_geneflow
    plotModel.r -p early_geneflow -l NyerMak,PundMak
    """
    # move tpl into folder
    tpl_file_path = os.path.join(path_to_best_run, f"{prefix}.tpl")
    best_run_prefix_folder = os.path.join(path_to_best_run, f"{prefix}")
    os.system(f"cp {tpl_file_path} {best_run_prefix_folder}")

    # move .obs to folder
    obs_file_path = os.path.join(path_to_best_run, f"{prefix}*.obs")
    os.system(f"cp {obs_file_path} {best_run_prefix_folder}")

    # define paths
    sfs_tools_executable = os.path.join(UTILITIES_PATH, "SFStools.r")
    plot_model_executable = os.path.join(UTILITIES_PATH, "plotModel.r")
    best_run_full_path = os.path.join(path_to_best_run, prefix)

    os.chdir(best_run_full_path)

    # run sfs tools: NOTE: this does not work, but idk how to fix it
    print("TRYING SFS TOOLS****************************")
    run_script(f"{sfs_tools_executable} -t print2D -i {prefix}") 

    # run plot model
    # need number of pops to plot
    num_pops = extract_number_of_samples(tpl_file_path)
    populations_list = []
    for i in range(num_pops):
        populations_list.append(f"pop{i}")
    populations = ",".join(populations_list)

    print("TRYING PLOT MODEL***************************")
    run_script(f"{plot_model_executable} -p {prefix} -l {populations}")

def recompute_likelihoods():
    # will need to send to cluster
    # run each of the top 10 models 100 more times -- see notes
    # see notes for further steps
    return


output_dir = "/home/raya/Documents/Projects/output/fsc_output"
prefix = "hops"
best_run_path = os.path.join(output_dir, "best_run")

# model_comp_with_aic(best_run_path, prefix)
# visualize_best_fit_model(best_run_path, prefix)
