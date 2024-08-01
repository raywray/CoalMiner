import log
import subprocess
import time
import os

def send_cmd_to_cluster(
    remote_url,
    bash_profile_path,
    cmd_list,
    out_dir,
    excuse="Connection reset by peer",
    num_re_all=3,
    sleepy_time=10,
    retry=False,
):
    cmds_to_append = ["ssh", remote_url, f". {bash_profile_path};"]
    cmds_to_send = cmds_to_append + cmd_list
    print(" ".join(cmds_to_send))
    if retry:
        out_string, error_string = run_and_wait_with_retry(
            cmds_to_send, out_dir, excuse, num_re_all, sleepy_time
        )
    else:
        out_string, error_string = run_and_wait_on_process(cmds_to_send, out_dir)
    return out_string, error_string

def run_and_wait_on_process(cmd, folder):
    program = cmd[0]
    log.write_to_log(" ".join(cmd))
    print(" ".join(cmd))
    process_completed_result = subprocess.run(cmd, capture_output=True, cwd=folder)
    error_string = process_completed_result.stderr.decode()
    out_string = process_completed_result.stdout.decode()

    colored_error_string = "\033[93m" + "ERROR:  " + error_string + "\x1b[0m"

    if len(error_string) > 0:
        log.write_to_log(colored_error_string)

    with open(os.path.join(folder, program + "_stderr.txt"), "w") as f:
        f.writelines(error_string)
    with open(os.path.join(folder, program + "_stdout.txt"), "w") as f:
        f.writelines(out_string)

    return out_string, error_string

def run_and_wait_with_retry(cmd, folder, excuse, num_retries_allowed, sleepy_time):
    num_tries = 0

    while True:
        out_string, error_string = run_and_wait_on_process(cmd, folder)
        num_tries = num_tries + 1
        if num_tries > num_retries_allowed:
            break

        if excuse in error_string:
            log.write_to_log(
                "Got " + excuse + ". Retrying " + str(num_tries) + " time."
            )
            log.write_to_log("Wait for " + str(sleepy_time) + " secs.")
            time.sleep(sleepy_time)
        else:
            break
    return out_string, error_string

def write_sh_file(template_file, out_dir, new_file_name, replacements):
    lines_to_write = []
    new_sh_file = os.path.join(out_dir, new_file_name)

    with open(template_file, "r") as f:
        while True:
            line = f.readline()
            new_line = line

            for r_tuple in replacements:
                out_with_the_old = r_tuple[0]
                in_with_the_new = r_tuple[1]

                if out_with_the_old in line:
                    new_line = line.replace(out_with_the_old, in_with_the_new)
            lines_to_write.append(new_line)
            if not line:
                break
    with open(new_sh_file, "w") as f:
        for line in lines_to_write:
            f.writelines(line)
    return new_sh_file