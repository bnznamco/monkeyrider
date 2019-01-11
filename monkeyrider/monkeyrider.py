
import sys
from .core import MonkeyRider


def main():
    script = sys.argv[0]
    for filename in sys.argv[1:]:
        print('Analyzing the package.. '+filename)
        monkeydrive = MonkeyRider(filename)
        print('PACKAGEPATH')
        print(monkeydrive.apk_path)
        print('PACKAGENAME')
        print(monkeydrive.package_name)
        print('MAINACTIVITY')
        print(monkeydrive.main_activity)
        monkeydrive.monkeyrunner()


if __name__ == '__main__':
    main()
