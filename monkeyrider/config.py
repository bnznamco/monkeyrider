import os


BASE_DIR = os.path.dirname(__file__)

ANDROID_HOME = os.environ.get('ANDROID_HOME', '')

if ANDROID_HOME:
    ANDROID_PATH = os.path.abspath(ANDROID_HOME)
else:
    ANDROID_PATH = os.path.join(os.environ.get('HOME'), 'Android', 'Sdk')


ADB_PATH = os.path.join(ANDROID_PATH, 'platform-tools', 'adb')
EMULATOR_PATH = os.path.join(ANDROID_PATH, 'emulator', 'emulator')
MONKEYRUNNER_PATH = os.path.join(ANDROID_PATH, 'tools', 'bin', 'monkeyrunner')
APKTOOL_PATH = os.path.join(BASE_DIR, 'bin', 'apktool')
MONKEYSCRIPT_PATH = os.path.join(BASE_DIR, 'monkeyrunner.py')
EMULATORSCRIPT_PATH = os.path.join(BASE_DIR, 'bin', 'apktool')
