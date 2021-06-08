#!/usr/bin/env python3

import json
import dns.resolver
import sys
import concurrent.futures
import requests
import os
from tqdm import tqdm

def validate_email(commune):
    #print(email)
    #ips_record = dns.resolver.resolve(email.split("@")[-1], "MX")
    #print(ips_record[0].exchange)

    api_key = os.environ("API_KEY")
    response = requests.get(
        "https://isitarealemail.com/api/email/validate",
        params = {'email': commune[1][1]},
        headers = {'Authorization': "Bearer " + api_key })
    j = response.json()
    if 'status' in j:
        return commune, j['status']
    return commune, j

def run(f, my_iter):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(tqdm(executor.map(f, my_iter), total=len(my_iter)))
    
    with open(f"out/mairies_out_{depart}.json", "w") as outfile:
        outfile.write(json.dumps(results, ensure_ascii=False))
    return results

with open("mairies.json") as infile:
    j = json.load(infile)
    
    for depart in j:
        exceptions = {}
        range_total = len(j[depart])
        #bar = tqdm(total=range_total)
        exceptions[depart] = {}
        res = run(validate_email, [commune for commune in j[depart].items()])
        #with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        #    future_to_url = {executor.submit(validate_email, commune): commune for commune in j[depart].items()}
        #    for future in concurrent.futures.as_completed(future_to_url):
        #        url = future_to_url[future]
        #        commune, status = future.result()
        #       if status != "valid":
        #          exceptions[commune[0]] = (commune[1][1], str(e))
        #bar.update(1)

                

