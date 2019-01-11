import subprocess
import os
import xmltodict
import json
import config
import sys


# TODO choose name for the project maybe monkeyride?


class MonkeyRider(object):
    def __init__(self, apk_path):
        self.apk_path = os.path.abspath(apk_path)
        self.__decompile()
        self.__load_structure()

    def __decompile(self):
        out = subprocess.Popen(
            [config.APKTOOL_PATH, 'd', self.apk_path],
            stdout=subprocess.PIPE
            )
        for c in iter(lambda: out.stdout.read(1), b''):
            sys.stdout.write(c.decode('utf-8'))
        self.base_dir = os.path.abspath(self.apk_path.replace('.apk', ''))

    def __load_structure(self):
        with open(os.path.join(self.base_dir, 'AndroidManifest.xml')) as m:
            self.AndroidManifest = xmltodict.parse(m.read())
        with open('AndroidManifestJSON_for_debug', 'w') as f:
            f.write(json.dumps(self.AndroidManifest, indent=4))
        self.package_name = self.AndroidManifest['manifest']['@package']
        self.activity_list = [act['@android:name'] for act in self.AndroidManifest['manifest']['application']['activity']] 
        self.main_activity = self.__get_main_activity()

    def __get_main_activity(self):
        for act in self.AndroidManifest['manifest']['application']['activity']:
            if 'intent-filter' in act:
                for i in act['intent-filter']:
                    if ('action' in i and 'category' in i and
                        i['action']['@android:name'] == 'android.intent.action.MAIN' and
                        i['category']['@android:name'] == 'android.intent.category.LAUNCHER'):
                        return act['@android:name']

    def monkeyrunner(self):
        out = subprocess.Popen(
            [config.MONKEYRUNNER_PATH, config.MONKEYSCRIPT_PATH, self.apk_path, self.package_name]+self.activity_list,
            stdout=subprocess.PIPE,
            )
        for c in iter(lambda: out.stdout.read(1), b''):
            sys.stdout.write(c.decode('utf-8'))

    def __associate_layouts(self):
        pass
        #  TODO
        #  we need to check smali activity path and figure out
        #  how to take the right path everytime and find activity files,
        #  for eache activity we need to find setContentView function and
        #  grab the ext constant associated with layout,
        #  then we can check for public.xml to associate hex with name!
