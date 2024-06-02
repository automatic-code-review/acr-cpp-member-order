import json
import os
import re
import subprocess

import automatic_code_review_commons as commons


def review(config):
    path_source = config['path_source']
    ordered_type = config['orderList']

    comments = []

    for root, dirs, files in os.walk(path_source):
        for file in files:
            if not file.endswith(".h"):
                continue

            infos = []
            file_path = os.path.join(root, file)
            ignore_type = config["ignoreList"]

            for field in list(get_infos(file_path)):
                if not atende_os_regex(ignore_type, field['type']):
                    infos.append(field)

            ordered = get_ordered(infos, ordered_type)

            if infos != ordered:
                como_esta = ""
                for field in infos:
                    como_esta += field['type'] + " " + field['name'] + ";<br>"

                como_deve_ficar = ""
                for field in ordered:
                    como_deve_ficar += field['type'] + " " + field['name'] + ";<br>"

                path_relative = file_path.replace(path_source, "")[1:]

                comment_description = config['comment']
                comment_description = comment_description.replace("${ORDERED_ATTRS}", como_deve_ficar)
                comment_description = comment_description.replace("${PATH}", path_relative)

                comments.append(commons.comment_create(
                    comment_id=commons.comment_generate_id(comment_description),
                    comment_path=path_relative,
                    comment_description=comment_description,
                    comment_snipset=None,
                    comment_end_line=1,
                    comment_start_line=1,
                ))

    return comments


def atende_os_regex(regex_list, field_type):
    for regex in regex_list:
        if not re.match(regex, field_type):
            return False

    return True


def get_ordered(fields, ordered_type):
    objs = []

    if len(fields) <= 1:
        return fields

    ja_add = []

    for field_type in ordered_type:
        for field in fields:
            if atende_os_regex(field_type, field['type']) and field['name'] not in ja_add:
                objs.append(field)
                ja_add.append(field['name'])

    for field in fields:
        if field['name'] not in ja_add:
            objs.append(field)

    return objs


def get_infos(file_path):
    data = subprocess.run(
        'ctags --output-format=json -R --languages=c++ --c++-kinds=+p --fields=+iaSn --extras=+q ' + file_path,  # TODO USAR EXTENSAO DO CTAG
        shell=True,
        capture_output=True,
        text=True,
    ).stdout

    objs = []

    for data_obj in data.split('\n'):
        if data_obj == '':
            continue

        data_obj = json.loads(data_obj)

        if data_obj['kind'] != 'member' or data_obj['access'] != 'private' or '::' in data_obj['name']:
            continue

        objs.append({
            'name': data_obj['name'],
            'type': data_obj['typeref'].replace("typename:", ""),
            'line': data_obj['line'],
        })

    objs = sorted(objs, key=lambda x: x['line'])

    return objs
