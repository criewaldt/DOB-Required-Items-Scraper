import requests, json, csv
import os
import pprint

from config.settings import OPENDATA_APP_TOKEN

worktypes = [ 'plumbing', 'mechanical', 'boiler', 'fuel_burning', 'fuel_storage', 'standpipe', 'sprinkler', 'fire_alarm', 
             'equipment', 'fire_suppression', 'curb_cut', 'other', 'other_description' ]

class JobsByWorktype():
    def __init__(self,):
        pass

    def get_jobs(self, worktype):
        payload = {
            "$$app_token" : OPENDATA_APP_TOKEN,
            "$limit" : 100
            }

        for wk in worktypes:
            if wk == worktype:
                payload[worktype] = 'X'
            else:
                payload[wk] = None
        
        url = "https://data.cityofnewyork.us/resource/ic3t-wcy2.json"
        r = requests.get(url, params=payload)
        return r.json()

def write_to_csv(worktype, jobs_list):
    with open('output/{} jobs.csv'.format(worktype), mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        for job in jobs_list:
            writer.writerow([job])
    print('Successfully created jobs list for {}'.format(worktype))


import pprint
if __name__ == "__main__":
    ByWorkType = JobsByWorktype()
    for worktype in worktypes:
        print(worktype)
        jobs = ByWorkType.get_jobs(worktype)
        for j in jobs:
            #print(j['job__'])
            pprint.pprint(j)
            input()
