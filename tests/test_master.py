import requests

# 本机测试
base_master_url = 'http://127.0.0.1:9507'
base_slaver_ip = '127.0.0.1'


def test_ping():
    resp = requests.get(base_master_url)
    assert resp.ok


def test_single_device_status():
    target_url = base_master_url + '/api/device'
    resp = requests.get(target_url, {
        'target_ip': base_slaver_ip,
    })
    assert resp.ok


def test_all_device_status():
    target_url = base_master_url + '/api/device'
    resp = requests.get(target_url)
    assert resp.ok


def test_single_server_status():
    target_url = base_master_url + '/api/slaver'
    resp = requests.get(target_url, {
        'target_ip': base_slaver_ip,
    })
    assert resp.ok


def test_all_server_status():
    target_url = base_master_url + '/api/slaver'
    resp = requests.get(target_url)
    assert resp.ok


def test_exec_py():
    target_url = base_master_url + '/api/task'
    resp = requests.post(target_url, {
        'script_name': 'hello_for_10s.py',
        'target_ip': base_slaver_ip,
    })
    assert resp.ok
    assert 'running' in resp.text
