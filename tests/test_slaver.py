import requests


base_url = 'http://127.0.0.1:9410'


def test_ping():
    resp = requests.get(base_url)
    assert resp.ok


def test_device_status():
    target_url = base_url + '/api/device/status'
    resp = requests.get(target_url)
    assert resp.ok


def test_device_command():
    target_url = base_url + '/api/device/command'
    resp = requests.get(target_url, {
        'adb_cmd': 'devices'
    })
    assert resp.ok
