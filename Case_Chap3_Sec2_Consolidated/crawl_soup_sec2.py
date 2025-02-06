import requests
from tqdm import tqdm
import os
import time
import pandas as pd

def get_html(index, url):
    if os.path.exists(f"Html_sec2/{index}.html"):
        return

    while True:
        try:
            r = requests.get(url, timeout=30)
            assert r.status_code == 200
            break
        except:
            print("Waiting for 30 seconds")
            time.sleep(30)

    with open(f"Html_sec2/{index}.html", "wb") as f:
        f.write(r.content)

    time.sleep(0.3)

if __name__ == "__main__":
    os.makedirs("Html_sec2", exist_ok=True)
    df = pd.read_csv("df_consolidated_sec2.csv")
    for iii in tqdm(range(len(df))):
        index = df.iloc[iii]["report_id"]
        url = df.iloc[iii]["url"]
        get_html(index, url)