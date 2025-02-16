import requests
import os
import json

LICENSE_KEY = "1B5D194B-A12144E7-8058EBE0-998709E3"

dbn_eskom_url = "https://developer.sepush.co.za/business/2.0/area?test&id=ethekwini3-12a-cbdeast"

payload={}
headers = {
    'token': LICENSE_KEY,
}

dbn_response = requests.request("GET", dbn_eskom_url , headers=headers, data=payload)
dbn_response = dbn_response.json()

try:    
    stage = int(dbn_response["events"][0]["note"][6])
    dbn_affected_hours = dbn_response["schedule"]["days"][0]["stages"][stage - 1]
except:
    dbn_affected_hours = []
    


def all_affected_hours():
    """Return all affected hours between 6am and 6pm"""
    all_hours = []
    
    try:
        for n in dbn_affected_hours:
            if 6 <= int(n[0:2]) <= 18:
                all_hours.append(n)

        return all_hours
    except:
        return "Couldn't retrieve data."



if __name__ == "__main__": 
    print(all_affected_hours())    