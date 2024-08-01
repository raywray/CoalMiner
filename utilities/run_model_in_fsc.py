import os

def add_permissions(tpl, est):
    add_permissions_tpl = [
        "chmod a+rwx", tpl
    ]
    add_permissions_est = [
        "chmod a+rwx", est
    ]
    execute_command(add_permissions_tpl)
    execute_command(add_permissions_est)
    

def execute_command(command_list):
    command = (" ".join(command_list))
    print(command)
    result = os.system(command)
    if result != 0:
        print(f"Command failed with exit code {result}")
    else:
        print("Command executed successfully")



def send_model_to_fsc(tpl_filename, est_filename, sfs_type):
    add_permissions(tpl_filename, est_filename)

    fsc_executable = "fsc28"    
    fsc_command = [
        fsc_executable,
        "-t", # add tpl file 
        tpl_filename,
        "-e", # add est file 
        est_filename,
        f"-{sfs_type}",
        "-0", # removeZeroSFS
        "-C", # minSFSCount
        "10",
        "-n", # numsims
        "1000",
        "-L", # numloops
        "40",
        "-s", # dnaToSnp 
        "0", # this outputs all SNP's in DNA sequence(s)
        "-M", # maxlhood
    ]
    execute_command(fsc_command)
    print("Finished running fsc28")