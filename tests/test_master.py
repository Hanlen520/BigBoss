import requests


base_url = 'http://127.0.0.1:9507'


def test_ping():
    resp = requests.get(base_url)
    assert resp.ok


def test_single_device_status():
    target_url = base_url + '/api/device'
    resp = requests.get(target_url, {
        'target_ip': '127.0.0.1',
    })
    assert resp.ok


def test_all_device_status():
    target_url = base_url + '/api/device'
    resp = requests.get(target_url)
    assert resp.ok


def test_single_server_status():
    target_url = base_url + '/api/slaver'
    resp = requests.get(target_url, {
        'target_ip': '127.0.0.1'
    })
    assert resp.ok


def test_all_server_status():
    target_url = base_url + '/api/slaver'
    resp = requests.get(target_url)
    assert resp.ok
