import requests
from bs4 import BeautifulSoup
import pandas as pd
import mimetypes
import sys
import os

url = "https://www.gob.mx/conagua/articulos/calidad-del-agua?idiom=es"

def handle_xlsb(file):
    df = pd.read_excel(file, engine='pyxlsb')
    return df

def handle_xlsx(file):
    df = pd.read_excel(file)
    return df

def save_csv(name, content):
    name = name + ".csv"
    content.to_csv(name)

def save_pdf(name, content):
    name = name + ".pdf"
    with open(name, "wb") as f:
        f.write(content)

def get_file(link):
    file_response = requests.get(link)
    return file_response.content

def main():
    html = requests.get(url).content
    parse_html = BeautifulSoup(html, 'html.parser')
    body = parse_html.find_all("div", class_="article-body")
    a_list = body[0].find_all("a")
    files = []
    for a in a_list:
        link = a.attrs["href"]
        split_link = link.split(".")
        try:
            file = get_file(link)
            split_name = split_link[-2].split("/")
            name = split_name[-1]
            if split_link[-1] == "xlsb":
                df = handle_xlsb(file)
                save_csv(name, df)
            elif split_link[-1] == "xlsx":
                df = handle_xlsx(file)
                save_csv(name, df)
            elif split_link[-1] == "pdf":
                save_pdf(name, file)

            files.append(link)
        except:
            print("Could not get ", link)
    print("Available files:")
    for file in files:
        print(file)

if __name__ == "__main__":
    main()