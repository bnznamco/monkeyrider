import subprocess
import config


def get_devices(adb_path=config.ADB_PATH):
    subprocess.check_call([adb_path, 'start-server'])
    out = subprocess.Popen(
        [adb_path, 'devices'],
        stdout=subprocess.PIPE
        ).communicate()[0].split('\n')
    devices = []
    for line in out[1:]:
        if not line:
            continue
        if 'offline' in line:
            continue
        print(line)
        device = line.split('\t')[0]
        devices.append(device)
    return devices


def get_emulator_images(emulator_path=config.EMULATOR_PATH):
    out = subprocess.Popen(
        [emulator_path, '-list-avds'],
        stdout=subprocess.PIPE
        ).communicate()[0].split('\n')
    images = []
    for line in out[0:]:
        if not line:
            continue
        images.append(line)
    print('Searching for emulator images..')
    print('found:\n'+str(images))
    return images[0]


def run_emulator(emulator_path=config.EMULATOR_PATH):
    subprocess.Popen([emulator_path, '-avd', get_emulator_images(emulator_path)])
