import requests
from tqdm import tqdm
import os
import time
import pandas as pd

def get_html(index, name, url):
    if os.path.exists(f"Html_subsec/{index}/{name}.html"):
        return

    while True:
        try:
            r = requests.get(url, timeout=30)
            assert r.status_code == 200
            break
        except:
            print("Waiting for 30 seconds")
            time.sleep(30)

    with open(f"Html_subsec/{index}/{name}.html", "wb") as f:
        f.write(r.content)

    time.sleep(0.3)

if __name__ == "__main__":
    df = pd.read_csv("df_consolidated_subsec.csv")
    total = df.count().sum() - df.shape[0]
    print(total)
    with tqdm(total=total) as pbar:
        for iii in range(len(df)):
            index = df.iloc[iii]["report_id"]
            os.makedirs(f"Html_subsec/{index}", exist_ok=True)
            for name in df.columns[1:]:
                url = df.iloc[iii][name]
                if not pd.isna(url):
                    get_html(index, name, url)
                    pbar.update(1)
