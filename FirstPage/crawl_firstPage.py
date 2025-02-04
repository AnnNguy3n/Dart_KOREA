import pandas as pd
import requests
from io import StringIO
from tqdm import tqdm
import os
from bs4 import BeautifulSoup
import time
import sys
def get_firstPage_html(report_id, session_id):
    url = f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={report_id}"

    while True:
        try:
            r = requests.get(url, timeout=30)
            assert r.status_code == 200
            break
        except:
            print("Waiting for 30 seconds...")
            time.sleep(30)

    with open(f"FirstPage/{session_id}/{report_id}.html", "wb") as f:
        f.write(r.content)

if __name__ == "__main__":
    ### Get session_id from sys.argv
    session_id = int(sys.argv[1])
    print(f"Session ID: {session_id}")
    # raise

    os.makedirs(f"FirstPage/{session_id}", exist_ok=True)

    metadata_path = os.path.abspath(".").replace("FirstPage", "Metadata/filtered_2010_2023.csv")
    metadata = pd.read_csv(metadata_path)
    start_index = 7932 * session_id
    end_index = start_index + 7932
    print(metadata.shape, start_index, end_index)

    for report_id in tqdm(metadata["report_id"][start_index:end_index]):
        get_firstPage_html(report_id, session_id)
        time.sleep(0.05)
