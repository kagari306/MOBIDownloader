import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import sys
import os

PASSCODE = 6195
FORMAT = "MOBI" # MOBI/EPUB

def get_size(file_size):
    if file_size/1024 < 1:
        return f"{file_size} B"
    elif file_size/1024/1024 < 1:
        return f"{file_size/1024} KB"
    elif file_size/1024/1024/1024 < 1:
        return f"{file_size/1024/1024} MB"
    else:
        return f"{file_size/1024/1024/1024} GB"

def print_splitline(lenght):
    for _ in range(0,lenght):
        print('-',end='')
    print("Split Line",end='')
    for _ in range(0,lenght):
        print('-',end='')
    print()

def download_file(file_info):
    file_content = requests.get(file_info["downurl"], stream = True)
    file_size = int(file_content.headers['content-length'])
    with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, ascii=True, desc=file_info['file_name']) as bar:
        with open(file_info['file_name'],'wb') as fp:
            for chunk in file_content.iter_content(chunk_size=512):
                if chunk:
                    fp.write(chunk)
                    bar.update(len(chunk))

def ctfile_download(file_id):
    file_info = requests.get(f"https://webapi.ctfile.com/getfile.php?path=f&f={file_id}&passcode={PASSCODE}&token=0&r=&ref=").json()['file']
    params = {
        "uid": file_info['userid'],
        "fid": file_info['file_id'],
        "folder_id": 0,
        "file_chk": file_info['file_chk'],
        "mb": 0,
        "token": 0,
        "app": 0,
        "acheck": 1,
        "verifycode": ""
    }
    # Get file url
    download_url = requests.get("https://webapi.ctfile.com/get_file_url.php",params = params)
    while download_url.json()['code'] != 200: # CAPTCHA
        print("Get download url failed. retrying...")
        time.sleep(1)
        download_url = requests.get("https://webapi.ctfile.com/get_file_url.php",params = params)
        
    print(f"Downloading {download_url.json()['file_name']} Size: {get_size(download_url.json()['file_size'])}")
    download_file(download_url.json())

def process_files(files, deep=1):

    for file in files[1:]:
        if len(file.find_all('td')) > 2:
            file_id = file.find_all('td')[FORMAT].find('a')['href'].split('/')[4].split('?')[0]  
            ctfile_download(file_id)
        else:
            if deep > 1:
                for _ in range(deep-1):
                    os.chdir("..")
                deep = 1
            print(f"Enter dir {file.find_all('td')[0].contents[1].string}")
            try:
                os.makedirs(file.find_all('td')[0].contents[1].string)
            except FileExistsError:
                print(f"Folder {file.find_all('td')[0].contents[1].string} already exist.")
            os.chdir(file.find_all('td')[0].contents[1].string)
            deep += 1
    return deep

def get_details(url):
    global split_line_len
    page_content = requests.get(url).content
    page_data = BeautifulSoup(page_content, 'lxml')

    title = files = page_data.find('h1').string
    print(f"Title: {title}")

    files = page_data.find('table').find_all('tr')

    try:
        os.makedirs(title)
    except FileExistsError:
        print(f"Folder {title} already exist.")
    
    os.chdir(title)
    
    for table_name in files[0].find_all('span')[:2]:
        print(table_name.string,end='\t')
    print()

    split_line_len = 0
    for file in files[1:]:
        for book_name in file.find_all('span'):
            print(book_name.string,end='\t')
            if len(book_name.string) + 6 > split_line_len:
                split_line_len =len(book_name.string) + 6
        print()
    
    print_splitline(split_line_len)
    return files

def main():
    os.chdir("files")
    if len(sys.argv) > 1:
        files = get_details(sys.argv[1])
        deep = process_files(files)
    else:
        url_list = []
        with open('../lists.txt','r') as f:
            url_list = f.read().splitlines()
        for num in range(len(url_list)):
            files = get_details(url_list[num])
            deep = process_files(files)
            
            for _ in range(deep):
                os.chdir("..")
            with open("../lists.txt","w") as f:
                for i in url_list[num+1:]:
                    f.write(f"{i}\r\n")
            
            print_splitline(split_line_len)

if FORMAT == "MOBI":
    FORMAT = 2
elif FORMAT == "EPUB":
    FORMAT = 3
else:
    print("FORMAT must be MOBI or EPUB")
    exit(1)

if __name__ == "__main__":
    main()