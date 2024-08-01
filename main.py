"""
This script generates 1 random model and runs it in fsc x number of times
"""
import os
import sys

from pipeline_modules import (
    generate_random_tpl,
    generate_random_est,
    determine_best_fit_model,
)
from utilities import get_user_params_from_yaml, use_fsc, run_model_in_fsc, generate_random_model # type: ignore


def execute_command(command):
    os.system(command)


def create_directory(dir_path):
    os.makedirs(dir_path, exist_ok=True)


def run_setup(cur_run, output_dir, project_path):    
    # make directory
    output_folder_name = f"{output_dir}/run_{cur_run}"
    create_directory(output_folder_name)


    # copy SFS into new dir
    os.system(f"cp {project_path}{user_params["FSC_INPUT_PREFIX"]}* {output_folder_name}")

    # move into new dir
    os.chdir(output_folder_name)

def generate_random_model(user_params): # TODO: can swap this out with the util 
    # Create filenames
    tpl_filename = f"{user_params["FSC_INPUT_PREFIX"]}.tpl"
    # tpl_filename = "hops.tpl"
    est_filename = f"{user_params["FSC_INPUT_PREFIX"]}.est"
    # est_filename = "hops.est"

    # Generate random tpl & est files
    generate_random_tpl.generate_random_params(
        tpl_filename, user_params["NUM_POPS"], user_params["SAMPLE_SIZES"]
    )
    generate_random_est.generate_random_params(
        tpl_filename,
        est_filename,
        **user_params["MODEL_PARAMS"]
    )
    return tpl_filename, est_filename


def run_simluations(user_params, num_of_sims, output_dir, project_path):
    # TODO: edit this function so that it generates 1 random tpl/est, and then runs fsc on that x number of times (ideally 1000)
    # run x number of fsc simulations
    for i in range(1, num_of_sims + 1):
        # prepare folder for run
        run_setup(i, output_dir, project_path)

        # Create filenames
        tpl_filename = f"{user_params["FSC_INPUT_PREFIX"]}.tpl"
        # tpl_filename = "cactus.tpl"
        est_filename = f"{user_params["FSC_INPUT_PREFIX"]}.est"
        # est_filename = "cactus.est"

        # Generate random tpl & est files
        generate_random_tpl.generate_random_params(
            tpl_filename, user_params["NUM_POPS"], user_params["SAMPLE_SIZES"]
        )
        generate_random_est.generate_random_params(
            tpl_filename,
            est_filename,
            **user_params["MODEL_PARAMS"]
        )

        # Run fsc TODO: change so it runs each model 100 times
        # TODO: get best l hoods from this, compare each best with each best
        # TODO: change 10000 to 1000

        run_model_in_fsc.send_model_to_fsc(tpl_filename=tpl_filename, est_filename=est_filename, sfs_type="d" if user_params["SFS_TYPE"] == "DAF" else "m")

        # command = f"fsc28 -t {tpl_filename} -e {est_filename} -{"d" if user_params["SFS_TYPE"] == "DAF" else "m"} -0 -C 10 -n 1000 -L 40 -s 0 -M"
        # print(command) 
        # execute_command(command)

        # go back to root directory
        os.chdir("../..")


def run(user_params, output_dir="output", project_path=""):
    # Create output directory
    create_directory(output_dir)

    num_of_fsc_runs = 1  # TODO: eventually 1000

    # generate random model
    tpl_filename, est_filename = generate_random_model(user_params)

    # add fsc exectuable to project path
    use_fsc.add_fsc_to_path(project_path)

    # run simulations
    run_simluations(user_params, num_of_fsc_runs, output_dir, project_path)

    # find the best fit run
    best_fit_run = determine_best_fit_model.get_best_lhoods(num_of_fsc_runs, user_params["FSC_INPUT_PREFIX"], output_dir)
    print("best fit run: run", best_fit_run)


if __name__ == "__main__":
    # get user params
    # example call: python3 main.py output_directory/ fscWrapper_project_path/
    if len(sys.argv) < 2:
        print("Usage: python script.py <parameter>")
        sys.exit(1)  
    user_input_yaml_filepath = sys.argv[1]
    output_dir = sys.argv[2]
    project_path = sys.argv[3]

    # parse yaml
    user_params = get_user_params_from_yaml.read_yaml_file(user_input_yaml_filepath)
    # run program
    run(user_params, output_dir, project_path)
