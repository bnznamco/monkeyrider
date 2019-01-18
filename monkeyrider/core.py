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
        self.activity_with_paths()

    def __decompile(self):
        out = subprocess.Popen(
            [config.APKTOOL_PATH, 'd', self.apk_path],
            stdout=subprocess.PIPE
            )
        for c in iter(lambda: out.stdout.read(1), b''):
            sys.stdout.write(c.decode('utf-8'))
        self.base_dir = os.path.abspath(self.apk_path.replace('.apk', ''))
        self.instruction_file = os.path.abspath(
            self.apk_path.replace('.apk', '_instructions')
            )

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
                    if 'action' in i and 'category' in i:
                        act_check = False
                        cat_check = False
                        if isinstance(i['action'], list):
                            for action in i['action']:
                                if action['@android:name'] == 'android.intent.action.MAIN':
                                    act_check = True
                                    break
                        elif i['action']['@android:name'] == 'android.intent.action.MAIN':
                            act_check = True
                        if isinstance(i['category'], list):
                            for category in i['category']:
                                if category['@android:name'] == 'android.intent.category.LAUNCHER':
                                    cat_check = True
                                    break
                        elif i['category']['@android:name'] == 'android.intent.category.LAUNCHER':
                            cat_check = True
                        if cat_check and act_check:
                            return act['@android:name']

    def monkeyrunner(self):
        self.__build_monkey_instruction()
        out = subprocess.Popen(
            [config.MONKEYRUNNER_PATH, config.MONKEYSCRIPT_PATH, self.apk_path, self.package_name, self.instruction_file],
            stdout=subprocess.PIPE,
            )
        for c in iter(lambda: out.stdout.read(1), b''):
            sys.stdout.write(c.decode('utf-8'))

    # def activity_with_paths(self):
    #     activity_with_paths = []
    #     for activity in self.activity_list:
    #         smali_path = activity.split('.')
    #         smali_file = smali_path.pop() + '.smali'
    #         smali_path.append(smali_file)
    #         touple = (activity, os.path.join(self.base_dir, 'smali', *smali_path))
    #         activity_with_paths.append(touple)
    #     return activity_with_paths

    def activity_with_paths(self):
        smali_for_activity = {}
        for activity in self.activity_list:
            smali_for_activity[activity] = []
            smali_path = activity.split('.')
            activity_name = smali_path.pop()
            search_path = os.path.join(self.base_dir, 'smali', *smali_path)
            for root, dirs, files in os.walk(search_path, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    if activity_name in str(file_path):
                        smali_for_activity[activity].append(file_path)
        return smali_for_activity

    def __associate_layouts_codes_to_names(self):
        code_names = {}
        try:
            with open(os.path.join(self.base_dir, 'res', 'values', 'public.xml')) as m:
                self.public_schema = xmltodict.parse(m.read())
        except OSError:
            return code_names
        for element in self.public_schema['resources']['public']:
            if element['@type'] == 'layout':
                code_names[element['@id']] = element['@name']
        return code_names

    def __associate_layouts(self):
        activities_wln = []
        code_names = self.__associate_layouts_codes_to_names()
        activity_wp = self.activity_with_paths()
        for activity, paths in activity_wp.items():
            for path in paths:
                try:
                    with open(path) as f:
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
                                    if origin == 0 or i - origin > 10:
                                        break
                            if len(layout_code) and layout_code[0] in code_names:
                                activities_wln.append(
                                    (activity, code_names[layout_code[0]])
                                )
                                break
                except OSError:
                    pass
        return set(activities_wln)

    def __associate_elements_code_to_name(self):
        code_names = {}
        try:
            with open(os.path.join(self.base_dir, 'res', 'values', 'public.xml')) as m:
                self.public_schema = xmltodict.parse(m.read())
        except OSError:
            return code_names
        for element in self.public_schema['resources']['public']:
            if element['@type'] == 'id':
                code_names[element['@id']] = element['@name']
        return code_names

    def __naive_button_search(self):
        activities_we = []
        code_names = self.__associate_elements_code_to_name()
        activity_wp = self.activity_with_paths()
        for activity, paths in activity_wp.items():
            elements = []
            for path in paths:
                try:
                    with open(path) as f:
                        content = f.readlines()
                        content = [x.strip().replace('\n', '') for x in content]
                        for i in range(len(content)):
                            layout_code = []
                            if 'findViewById' in content[i]:
                                origin = i
                                while not len(layout_code):
                                    origin -= 1
                                    layout_code = re.findall(
                                        r'0x[0-9A-F]+',
                                        content[origin], re.I
                                        )
                                    if origin == 0 or i - origin > 5:
                                        break
                            if len(layout_code) and layout_code[0] in code_names:
                                elements.append(code_names[layout_code[0]])
                        if len(elements):
                            activities_we.append(
                                        (activity, elements)
                                    )
                except OSError:
                    pass
        return activities_we

    def __build_monkey_instruction(self):
        action_dict = dict()
        for element in self.__naive_button_search():
            action_dict[element[0]] = element[1]
        with open(self.instruction_file, 'w') as f:
            f.write(json.dumps(action_dict, indent=4))

    # TODO
    # Create a tree for navigation:
    #     - need to know which button start which activity
    #     - need to keep trace of the path we find
    #     - need to organize activity visit order
    #     - if possible find a whay to make monkey aware of current activity
