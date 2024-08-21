# CoalMiner
This package is intended to help overcome limitation when estimating a model's evolutionary history. It takes user provided files and parameters, and creates several random topologies for the user to then test using [fastsimcoal28](https://cmpg.unibe.ch/software/fastsimcoal28/).

## Installation
1. Clone the *CoalMiner* repo onto your machine: `git clone https://github.com/raywray/CoalMiner.git`
2. Move into the *CoalMiner* directory: `cd CoalMiner`
2. Install all necessary conda packages and create a conda environment (will need to have [anaconda](https://docs.anaconda.com/anaconda/install/) or [miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/) installed prior) with the following command: `conda env create -f environment.yml`

3. Activate the conda environment: `conda activate coalminer_env`

## Use CoalMiner
### Input Files
*CoalMiner* requires only 2 types of input files: an SFS and a `.yml` with user parameters. 

#### SFS
Users can create their SFS's from `.vcf` files using several packages, including using the [PPP](https://ppp.readthedocs.io/en/latest/PPP_pages/Input_File_Generators/vcf_to_fastsimcoal.html) pipeline (this package is recommended)[^1]. These files **MUST** be placed directly in the *CoalMiner* directly and can be accomplished with the following command: `cp [prefix]_joint*.obs CoalMiner/`

#### User parameter `.yml`
This file must contain the follwing information
- `INPUT_PREFIX`: the output prefix the user would like to use 
- `NUM_POPS`: the number of populations being tested 
- `SAMPLE_SIZES`: as a bulleted list, the number of sampled individuals from each population 

Additionally, prior distributions, ranges and types must be provided for (under the `MODEL_PARAMS` section): 
- mutation rates: `mutation_rate_dist`
- effective population sizes: `effective_pop_size_dist`
- migration rates: `migration_dist`
- time in generations: `time_dist`
- and an optional value for the maximum number of generations between events (default=1000): `max_time_between_events` 

Optional Parameters:
- `OUTPUT_DIR`: (optional) Path for outupt
- `NUM_RANDOM_MODELS`: the number of random topologies to generate (defaulted to 100)


Example input `.yml` files can be found in the `example_input_files` directory.

### Running *CoalMiner*
After the input have been created, running *CoalMiner* is very simple and can be done with the following command: `python3 [path_to_coalminer.py] [path_to_user_input_yml]`

For example: `python3 /Users/foo/Projects/CoalMiner/coalminer.py /Users/foo/Projects/coalminer_input.yml`

### Output Files
CoalMiner generates random `.est` and `.tpl` files and saves them in directories titled `{prefix}_random_model_1`, `{prefix}_random_model_2`, etc., in the output directory. It also copies the provided SFS files into the respective model directories. 

### Example
Any example files can be found in the `example_input_files` directory. These files are used in the [**video tutorial**](https://youtu.be/XNAofUfulHw). Run the following commands to see how the example files work (assuming you have navigated into the *CoalMiner* directory):

`cp example_input_files/hom_sap_joint*.obs .`

`python3 coalminer.py example_input_files/hom_sap_3_pop_model.yml`


[^1]: *fastsimcoal* will only run with specific SFS suffix names. See the *OBSERVED SFS FILE NAMES* section of the [fastsimcoal manual](https://cmpg.unibe.ch/software/fastsimcoal28/man/fastsimcoal28.pdf).

