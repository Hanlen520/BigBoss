import subprocess
import threading


TASK_DICT = {
    # task id : process
}


def run_script(task_id, script_path):
    run_cmd = ['python', script_path]
    script_process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    TASK_DICT[task_id] = script_process

    if script_process.poll() is not None:
        result, _ = script_process.communicate()
        del TASK_DICT[task_id]
        print('delete task {}'.format(task_id))
        return result
    # is running
    return None


def check_task_dict():
    while True:
        need_remove = []
        for each_task_name, each_process in TASK_DICT.items():
            if each_process.poll() is not None:
                print(each_process.stdout.read())
                need_remove.append(each_task_name)
        for each_finished_task in need_remove:
            del TASK_DICT[each_finished_task]


threading.Thread(target=check_task_dict).start()


__all__ = [
    'run_script',
]
