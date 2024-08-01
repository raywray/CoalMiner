from datetime import datetime

log_file_path = ""

def write_to_log(msg):

        now = datetime.now()
        day = now.strftime("%d/%m/%Y")
        time = now.strftime("%H:%M:%S")
        time_stamp_string = ",".join([day,time])
        log_line = time_stamp_string + ":\t" + msg + "\n"
        print(log_line)

        if len(log_file_path) == 0:
            return

        with open(log_file_path, 'a') as f:
           f.write(log_line)