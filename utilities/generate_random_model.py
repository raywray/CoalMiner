from pipeline_modules import generate_random_tpl, generate_random_est

from utilities import get_user_params_from_yaml


def get_tpl_est_files(user_params):
    # Create filenames
    tpl_filename = f'{user_params["FSC_INPUT_PREFIX"]}.tpl'
    # tpl_filename = "hops.tpl"
    est_filename = f'{user_params["FSC_INPUT_PREFIX"]}.est'
    # est_filename = "hops.est"

    # Generate random tpl & est files
    generate_random_tpl.generate_random_params(
        tpl_filename, user_params["NUM_POPS"], user_params["SAMPLE_SIZES"]
    )
    generate_random_est.generate_random_params(
        tpl_filename, est_filename, **user_params["MODEL_PARAMS"]
    )
    return tpl_filename, est_filename


def get_user_params(user_input_yaml_file):
    return get_user_params_from_yaml.read_yaml_file(user_input_yaml_file)


def generate_model(user_input_yaml_file):
    user_params = get_user_params(user_input_yaml_file)
    tpl_filename, est_filename = get_tpl_est_files(user_params)
    return tpl_filename, est_filename
