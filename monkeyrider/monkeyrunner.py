import sys
import os
import time
import simplejson as json
from utils import get_devices, run_emulator
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from com.android.monkeyrunner.easy import EasyMonkeyDevice, By


def main():
    apk = sys.argv[1]
    package = sys.argv[2]
    instructions_file = sys.argv[3]
    print(instructions_file)
    print('Checking adb devices')
    devices = get_devices()
    print('Devices found: '+str(devices))
    if not len(devices):
        print('No devices found, setting up emulator')
        run_emulator()
        print('Emulator boot completed.. proceding..')

    device = MonkeyRunner.waitForConnection()
    easy_device = EasyMonkeyDevice(device)
    print('Connected\nInstalling package..')
    device.installPackage(apk)
    print('Installed!')
    print('Checking all activities..\nThis may take a while..')
    f = open(instructions_file, 'r')
    instructions = json.load(f)
    for activity in instructions:
        print(activity)
        runComponent = package + '/' + activity
        for button in instructions[activity]:
            device.startActivity(component=runComponent)
            time.sleep(1)
            if easy_device.visible(By.id('id/'+button)):
                easy_device.touch(By.id('id/'+button), MonkeyDevice.DOWN_AND_UP)
                time.sleep(1)
            else:
                device.press("KEYCODE_BACK", MonkeyDevice.DOWN_AND_UP)
                time.sleep(1)
                if easy_device.visible(By.id('id/'+button)):
                    easy_device.touch(By.id('id/'+button), MonkeyDevice.DOWN_AND_UP)

        result = device.takeSnapshot()
        result_path = os.path.join(os.path.abspath('monkeyresult/'), package)
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        result.writeToFile(
            os.path.join(result_path, activity+'.png'),
            'png'
            )
    f.close()
    print('Saved some snapshots to\n'+result_path)


if __name__ == '__main__':
    main()
