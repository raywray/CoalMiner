# CoalMiner
a wrapper to test hundreds of models and then run them through FSC to get the best fit evolutionary model

the user needs to have created an sfs already. Code written in my summary stats pipeline. These files need to be in the base directory of the directory where the code is being run (straight in CoalMiner)

<!-- To use fsc28, you need to add fsc28 to the path using `export PATH=$PATH:[path_to_current_working_dir]` -->

<!-- You may also need to change permissions. Do that by doing this: `chmod +x fsc28_linux64/fsc28` -->

how to install all packages: 
`conda env create -f environment.yml`
`conda activate coal_miner_env`