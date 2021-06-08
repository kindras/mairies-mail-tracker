#!/usr/bin/env python3

import json
import sys
import concurrent.futures
import requests
import os
from tqdm import tqdm

def validate_email(commune):
    api_key = os.environ("API_KEY")
    resp = requests.get(
        "https://isitarealemail.com/api/email/validate",
        params = {'email': commune[1][1]},
        headers = {'Authorization': "Bearer " + api_key })
    response = resp.json()
    if 'status' in response:
        return commune, response['status']
    return commune, response

def run(function_to_start, department, commune):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(tqdm(executor.map(function_to_start, commune), total=len(commune)))
    
    with open(f"out/mairies_out_{department}.json", "w") as outfile:
        outfile.write(json.dumps(results, ensure_ascii=False))
    return results

def check_mails(departments):
    with open("mairies.json") as infile:
        mairies = json.load(infile)

        for depart in mairies:
            if not departments or depart in departments:
                run(validate_email, depart, [commune for commune in mairies[depart].items()])

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("departments", nargs="*")
    args = parser.parse_args()

    check_mails(args.departments)

