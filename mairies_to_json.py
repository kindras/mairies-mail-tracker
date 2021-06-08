#!/usr/bin/env python3

import argparse
import os
import concurrent.futures
import json
import glob
import xml.etree.ElementTree as ET

COMMUNES_PATH = 'latest/all_20210607/communes'
ORGANISMES_PATH = 'latest/all_20210607/organismes'

def get_department_details(department: str):
    details = {}
    for commune in glob.glob(f'{COMMUNES_PATH}/{department}/*.xml'):
        try:
            tree = ET.parse(commune)
            root = tree.getroot()
            organisme_id = root.find('.//TypeOrganisme[@pivotLocal="mairie"]/Organisme').attrib['id']
            organisme_file = f'{ORGANISMES_PATH}/{department}/{organisme_id}.xml'
            tree = ET.parse(organisme_file)
            root = tree.getroot()
            commune_name = root.find('*/NomCommune').text
            commune_mail = root.find('*/Email').text
            details[commune_name] = (organisme_file, commune_mail)
        except:
            pass
    return (department, details)

def convert(fast: bool):
    if fast:
        departments = [ '03' ]
    else:
        departments = os.listdir(COMMUNES_PATH)
    details = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(get_department_details, department): department for department in departments}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                department, department_details = future.result()
                details[department] = department_details
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
    with open("mairies.json", "w") as outfile:
        outfile.write(json.dumps(details, ensure_ascii=False))
    print(details)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(__name__)
    parser.add_argument('-f', '--fast', action='store_true', help='Only take a single department')
    args = parser.parse_args()

    convert(args.fast)