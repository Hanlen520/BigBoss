import subprocess
import threading
import requests
import os
from config import *


TASK_DICT = {
    # task id : process
}


def write_script(task_id, script_content):
    os.makedirs(GlobalConf.TEMP_DIR, exist_ok=True)
    target_temp_file = os.path.join(GlobalConf.TEMP_DIR, task_id + '.py')
    with open(target_temp_file, 'w+') as f:
        f.write(script_content)
        f.flush()
    return target_temp_file


def run_script(task_id, script_path):
    run_cmd = ['python', script_path]
    script_process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    TASK_DICT[task_id] = script_process

    if script_process.poll() is not None:
        result, _ = script_process.communicate()
        del TASK_DICT[task_id]
        return result.read().decode()
    # is running
    return None


def update_task(task_id, exec_result, status):
    master_url = 'http://{}:{}/api/private/task'.format(GlobalConf.MASTER_IP, GlobalConf.MASTER_PORT)
    requests.post(master_url, {
        'task_id': task_id,
        'exec_result': exec_result,
        'status': status,
    })


def check_task_dict():
    while True:
        need_remove = []
        for each_task_name, each_process in TASK_DICT.items():
            if each_process.poll() is not None:
                exec_result = each_process.stdout.read().decode()
                update_task(each_task_name, exec_result, 'done')
                need_remove.append(each_task_name)
        for each_finished_task in need_remove:
            del TASK_DICT[each_finished_task]


threading.Thread(target=check_task_dict).start()


__all__ = [
    'run_script',
    'write_script',
]
