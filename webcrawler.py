import requests
from bs4 import BeautifulSoup
import pandas as pd
import mimetypes
import sys
import os

url = "https://www.gob.mx/conagua/articulos/calidad-del-agua?idiom=es"

def handle_xlsb(file):
    xlsx = pd.ExcelFile(file, engine='pyxlsb')
    df_map = {}
    for sheet_name in xlsx.sheet_names:
        df_map[sheet_name] = xlsx.parse(sheet_name)
    return df_map

def handle_xlsx(file):
    xlsx = pd.ExcelFile(file)
    df_map = {}
    for sheet_name in xlsx.sheet_names:
        df_map[sheet_name] = xlsx.parse(sheet_name)
    return df_map

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
                df_map = handle_xlsb(file)
                for df_key in df_map:
                    save_csv(name + "_" + df_key, df_map[df_key])
                
            elif split_link[-1] == "xlsx":
                df_map = handle_xlsx(file)
                for df_key in df_map:
                    save_csv(name + "_" + df_key, df_map[df_key])

            elif split_link[-1] == "pdf":
                save_pdf(name, file)

            files.append(link)
        except:
            print("Could not get ", link)
    print("Available files:")
    for file in files:
        print(file)

def one_file():
    file = get_file("https://files.conagua.gob.mx/aguasnacionales/Costero.xlsb")
    df = handle_xlsb(file)
    print(df)
    for sheet in df:
        save_csv("Costero_" + sheet, df[sheet])

if __name__ == "__main__":
    main()
    #one_file()