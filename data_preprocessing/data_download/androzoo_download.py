from tqdm import tqdm
import requests
import pandas as pd

'''
Run this script to download the data from Androzoo

Step 1 - Get an API Key from: https://androzoo.uni.lu/
Step 2 - Insert your API Key in the APIKEY variable below
Step 3 - Run the Script

'''

APIKEY = "ENTER API KEY"

dataset = pd.read_csv('examplaires.csv')

sha256list = list(dataset["sha256"])

for sha256 in sha256list:
    url = "https://androzoo.uni.lu/api/download?apikey="+APIKEY+"&sha256="+sha256
    r = requests.get(url)
    file_name = "../../data/Benign_APK/Sha256_"+sha256

    with open(file_name, 'wb') as f:
        for data in tqdm(r.iter_content()):
            f.write(data)
