import sys
import os
import time
from utils import get_devices, run_emulator
from com.android.monkeyrunner import MonkeyRunner


def main():
    apk = sys.argv[1]
    package = sys.argv[2]
    activities = sys.argv[3:]
    print('Checking adb devices')
    devices = get_devices()
    print('Devices found: '+str(devices))
    if not len(devices):
        print('No devices found, setting up emulator')
        run_emulator()

    device = MonkeyRunner.waitForConnection()
    print('Connected\nInstalling package..')
    device.installPackage(apk)
    print('Installed!')
    print('Checking all activities..\nThis may take a while..')
    for activity in activities:
        runComponent = package + '/' + activity
        device.startActivity(component=runComponent)
        time.sleep(5)
        result = device.takeSnapshot()
        result_path = os.path.join(os.path.abspath('monkeyresult/'), package)
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        result.writeToFile(
            os.path.join(result_path, activity+'.png'),
            'png'
            )
    print('Saved some snapshots to\n'+result_path)


if __name__ == '__main__':
    main()
