import requests
import os
import urllib.request as ur
import zipfile
from bs4 import BeautifulSoup
import urllib.parse        #[新增]使用urllib.parse.quote

name = input("輸入")

# 下載 紳士 首頁內容
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}
r = requests.get('https://wnacg.org/download-index-aid-' + name + '.html', headers = headers)

# 確認是否下載成功
if r.status_code == requests.codes.ok:
  # 以 BeautifulSoup 解析 HTML 程式碼
    soup = BeautifulSoup(r.text, 'html.parser')

    nowpath = os.path.abspath('./本' + name)        #獲取當前路徑
  # 以 CSS 的 class 抓出各類頭條新聞
    if not os.path.isdir(nowpath):
        print("新增資料夾。")
        os.mkdir(nowpath)
    stories = soup.find('a', class_= "down_btn")
    imgurl = stories.get('href')
    imgurl = 'https:' + imgurl        #[新增]檔案連結的開頭是//z16.wzip.ru 所以把https:補上去
    imgurl = urllib.parse.quote(imgurl, safe = ':/?')        #[新增]某些作品名含有空格或日文等 需要用quote轉換 而其中':/?'代表不想被轉換的字元 參考自https://stackoverflow.com/a/47433617
    ur.urlretrieve(imgurl, os.path.join(nowpath, name + '.zip'), reporthook=None, data=None)
    print("下載完成")

    zip_name = nowpath + '/' + name + '.zip'#壓縮文件名
    file_dir = nowpath #解壓後的文件放在該目錄下
    with zipfile.ZipFile(zip_name, 'r') as myzip:
        for file in myzip.namelist():
            myzip.extract(file,file_dir)

    print("解壓縮完成")
    os.remove(zip_name)
    print("壓縮檔已刪除")
  
  