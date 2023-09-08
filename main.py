import requests
from bs4 import BeautifulSoup
import html2text
import re
import toml

# TOMLファイルのパスを指定
config_file = 'config.toml'

# TOMLファイルを読み込む
config_data = toml.load(config_file)

base_url = "https://www.space.t.u-tokyo.ac.jp/"
section_name = "wiki/procedure/"
url =  base_url + section_name

# セッションを作成
session = requests.Session()
session.auth = (config_data["web_login_info"]["username"], config_data["web_login_info"]["password"])

response = session.get(url)

# ステータスコードが200以外の場合、エラーを出力して終了
if response.status_code != 200:
    print('最初の認証に失敗しました。')
    exit()

second_login_data = {
    'u': config_data["wiki_login_info"]["username"],
    'p': config_data["wiki_login_info"]["password"],
}

response = session.post(url, data=second_login_data)

try:
    # セッションを使用してページにアクセス
    response = session.get(url)

    if response.status_code != 200:
        print(f"エラーステータスコード: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"エラー: {e}")

# セカンドページのコンテンツを取得
soup = BeautifulSoup(response.text, 'html.parser')

elems = soup.body.find_all(href=re.compile(section_name), class_=re.compile("wikilink"))

links = [elem.attrs['href'] for elem in elems]
for link in links:
    file_name = link.replace("/", "-") + ".txt"
    if file_name.startswith("-wiki-"):
        file_name = file_name[len("-wiki-"):]
    print(file_name)

    link = base_url + link
    res = session.post(link, data=second_login_data)
    soup = BeautifulSoup(res.text, 'html.parser')
    elem = soup.find(class_="dw-content")
    new_soup = BeautifulSoup('<html></html>', 'html.parser')
    new_soup.html.append(elem)

    # markdown に変換して書き出し
    md = html2text.html2text(new_soup.prettify())
    md = md.replace("\n編集\n", "")
    with open("output/"+file_name, 'w', encoding='utf-8') as file:
        file.write(md)
