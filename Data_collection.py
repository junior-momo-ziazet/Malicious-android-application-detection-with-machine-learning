from tqdm import tqdm
import requests
import pandas as pd

APIKEY="5388ac33b211abffbfaf6e6e43f2feecd679d1bc243a4a2876e7b10d73f9b365"

dataset=pd.read_csv('examplaires.csv')

sha256list=list(dataset["sha256"])

for sha256 in sha256list:
    url="https://androzoo.uni.lu/api/download?apikey="+APIKEY+"&sha256="+sha256
    r=requests.get(url)
    file_name="data_downloaded/Sha256_"+sha256
    
    with open(file_name,'wb') as f:
        for data in tqdm(r.iter_content()):
            f.write(data)
    
