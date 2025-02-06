import os
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import pandas as pd
from io import StringIO


def count_dir(folder, count = None):
    if count is None: count = [[], []]
    for file in os.listdir(folder):
        new_path = os.path.join(folder, file)
        if os.path.isdir(new_path):
            count[0].append(new_path)
            count_dir(new_path, count)
        elif not new_path.endswith(".DS_Store"):
            count[1].append(new_path)
    return count

def process_file(path):
    with open(path, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    tables = soup.find_all("table", attrs={"border": "1"})
    nb_tables = soup.find_all("table", attrs={"class": "nb"})
    assert len(tables) + len(nb_tables) == len(soup.find_all("table"))

    lines = []
    for element in soup.find("body").find_all(recursive=False):
        if element.name == "table" and "border" in element.attrs:
            table_element = element
            break

        temp = element.text.splitlines()
        for line in temp:
            text = "".join(line.split())
            if text != "":
                lines.append(text)

    assert not "colspan" in table_element.prettify() and not "rowspan" in table_element.prettify()
    df = pd.read_html(StringIO(table_element.prettify()))[0]
    return "\n".join(lines), df.to_csv(index=False)


if __name__ == "__main__":
    count = count_dir("Html_subsec")

    with Pool(cpu_count()) as p:
        results = list(tqdm(p.imap(process_file, count[1]), total=len(count[1])))

    temp = pd.DataFrame({
        "path": count[1],
        "lines": [r[0] for r in results],
        "table": [r[1] for r in results]
    })

    temp.to_csv("temp.csv", index=False)