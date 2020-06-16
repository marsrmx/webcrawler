import requests
from bs4 import BeautifulSoup
import pandas as pd
import mimetypes

url = "https://www.gob.mx/conagua/articulos/calidad-del-agua?idiom=es"

def handle_xlsb(file):
    df = pd.read_excel(file, engine='pyxlsb')
    return df

def main():
    print("hello")
    html = requests.get(url).content
    parse_html = BeautifulSoup(html, 'html.parser')
    body = parse_html.find_all("div", class_="article-body")
    a_list = body[0].find_all("a")
    for a in a_list:
        #link.attrs
        link = a.attrs["href"]

    file_response = requests.get("https://files.conagua.gob.mx/aguasnacionales/Léntico.xlsb")
    content_type = file_response.headers['content-type']
    print(content_type)
    extension = mimetypes.guess_extension(content_type)
    print(extension)
    file = file_response.content
    print(type(file))
    df = pd.read_excel(file, engine='pyxlsb')
    print(type(df))
    df.to_csv("output.csv")



if __name__ == "__main__":
    main()