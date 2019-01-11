import subprocess
import os
import xmltodict
import json
from . import config
import sys
import re


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
        self.activity_layouts = self.__associate_layouts()

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

    def activity_with_paths(self):
        activity_with_paths = []
        for activity in self.activity_list:
            smali_path = activity.split('.')
            smali_file = smali_path.pop() + '.smali'
            smali_path.append(smali_file)
            touple = (activity, os.path.join(self.base_dir, 'smali', *smali_path))
            activity_with_paths.append(touple)
        return activity_with_paths

    def __associate_layouts_codes_to_names(self):
            with open(os.path.join(self.base_dir, 'res', 'values', 'public.xml')) as m:
                self.public_schema = xmltodict.parse(m.read())
            code_names = {}
            for element in self.public_schema['resources']['public']:
                if element['@type'] == 'layout':
                    code_names[element['@id']] = element['@name']
            return code_names

    def __associate_layouts(self):
        activities_wln = []
        code_names = self.__associate_layouts_codes_to_names()
        for activity in self.activity_with_paths():
            with open(activity[1]) as f:
                content = f.readlines()
                content = [x.strip().replace('\n', '') for x in content] 
                for i in range(len(content)):
                    layout_code = []
                    if 'setContentView' in content[i]:
                        origin = i
                        while not len(layout_code):
                            origin -= 1
                            layout_code = re.findall(
                                r'0x[0-9A-F]+',
                                content[origin], re.I
                                )
                            if i - origin > 10:
                                break
                    if len(layout_code):
                        activities_wln.append(
                            (activity[0], code_names[layout_code[0]])
                        )
                        break
        return activities_wln




        #  TODO (almost done)
        #  we need to check smali activity path and figure out
        #  how to take the right path everytime and find activity files,
        #  for eache activity we need to find setContentView function and
        #  grab the ext constant associated with layout,
        #  then we can check for public.xml to associate hex with name!
