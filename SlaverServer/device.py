# TODO 设备操作部分需要找一个稳定的操作库
import subprocess

base_cmd = ('adb',)


def exec_adb_cmd(command_list, device=None, shell=None):
    """
    exec adb command (simple example)

    :param command_list: command list after 'adb' or 'adb shell', ['adb', 'devices'] -> ['devices']
    :param device: str, '123456F'
    :param shell: start with 'adb shell' or 'adb'
    :return:
    """
    cur_cmd = list(base_cmd)
    if device:
        cur_cmd += ['-s', device]
    if shell:
        cur_cmd.append('shell')
    cur_cmd += command_list

    sp = subprocess.Popen(cur_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sp_std, _ = sp.communicate()
    return sp_std.decode()


__all__ = [
    'exec_adb_cmd',
]

if __name__ == '__main__':
    device_list = exec_adb_cmd(['devices'])
    getprop = exec_adb_cmd(['getprop'], shell=True)

    print(device_list)
    print(getprop)
