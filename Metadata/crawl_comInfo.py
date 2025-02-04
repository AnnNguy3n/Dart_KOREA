import requests
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
from tqdm import tqdm
import time


def get_company_info(popup_href):
    url = f"https://dart.fss.or.kr/dsae001/selectPopup.ax?selectKey={popup_href}"

    while True:
        try:
            r = requests.get(url, timeout=30)
            assert r.status_code == 200
            break
        except:
            print("Waiting for 30 seconds...")
            time.sleep(30)

    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("table")
    df = pd.read_html(StringIO(table.prettify()))[0]

    try:
        assert df.iloc[:,0].unique().size == df.shape[0]
        return dict(zip(df.iloc[:,0], df.iloc[:,1]))
    except:
        print(f"Error in {popup_href}")
        return {}


if __name__ == "__main__":
    with open("popup_hrefs.txt", "r") as f:
        popup_hrefs = f.read().splitlines()

    session_id = 0
    start_index = 1223 * session_id
    end_index = start_index + 1223
    print(len(popup_hrefs), start_index, end_index)

    list_data = []
    for popup_id in tqdm(popup_hrefs[start_index:end_index]):
        data = get_company_info(popup_id)
        list_data.append(data)
        time.sleep(0.1)

    df = pd.DataFrame(list_data)
    df["popup_id"] = popup_hrefs[start_index:end_index]
    df.to_csv(f"comInfo_{session_id}.csv", index=False)