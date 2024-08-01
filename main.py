import os
import sys

from pipeline_modules import (
    generate_random_tpl,
    generate_random_est,
)
from utilities import get_user_params_from_yaml # type: ignore


def execute_command(command):
    os.system(command)


def create_directory(dir_path):
    os.makedirs(dir_path, exist_ok=True)


def random_model_setup(cur_run, output_dir):    
    # make directory
    output_folder_name = os.path.join(output_dir, f"random_model_{cur_run}")
    create_directory(output_folder_name)

    # copy SFS into new dir (assuming the sfs is right in the CoalMiner directory)
    os.system(f"cp {user_params['INPUT_PREFIX']}* {output_folder_name}")

    # move into new dir
    os.chdir(output_folder_name)

def generate_random_model(cur_model, output_dir):
    # set up the random model output directory
    random_model_setup(cur_model, output_dir)

    # create filenames
    tpl_filename = f"{user_params['INPUT_PREFIX']}.tpl"
    est_filename = f"{user_params['INPUT_PREFIX']}.est"

    # Generate random tpl & est files
    generate_random_tpl.generate_random_params(
    tpl_filename, user_params["NUM_POPS"], user_params["SAMPLE_SIZES"]
    )
    generate_random_est.generate_random_params(
        tpl_filename, est_filename, **user_params["MODEL_PARAMS"]
    )

    os.chdir("../..")

def generate_models(user_params):
    output_dir = user_params.get("OUTPUT_DIR", "output") # since output dir is an optional value
    num_random_models = user_params["NUM_RANDOM_MODELS"]

    # Create output directory
    create_directory(output_dir)
    
    for i in range(1, num_random_models + 1):
        # generate random model
        generate_random_model(cur_model=i, output_dir=output_dir)
        

if __name__ == "__main__":
    # get user params
    # example call: python3 main.py input.yml
    if len(sys.argv) < 2:
        print("Usage: python script.py <input.yml>")
        sys.exit(1)  
    user_input_yaml_filepath = sys.argv[1]

    # parse yaml
    user_params = get_user_params_from_yaml.read_yaml_file(user_input_yaml_filepath)
    
    # run program
    generate_models(user_params)
