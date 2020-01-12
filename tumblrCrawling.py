# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import os
import zipfile
import requests
import urllib.request
import asyncio
from bs4 import BeautifulSoup
import re
import nest_asyncio
nest_asyncio.apply()

# class zipfile.ZipFile(파일주소, Mode(Option))
# Mode :
# 'r' 존재하는 파일 읽기
# 'w' 파일이 존재하면 지우고 생성
# 'a' 존재하는 파일에 append 하기
# 'x' 파일이 존재하지 않으면 생성, 존재하면 FileExistsError 뱉음

# html = req.text # HTML 소스 가져오기
# header = req.headers # HTTP Header 가져오기
# status = req.status_code # HTTP Status 가져오기 (200: 정상)
# is_ok = req.ok # HTTP가 정상적으로 되었는지 (True/False)


# %%
async def download(img):
#     fullName = "./temp/" + str(filename).rjust(3, '0') + ".jpg"
    try:
        print("Downloading... "+ img["fileName"], end="\r", flush=True)
        await loop.run_in_executor(None, urllib.request.urlretrieve, img["URL"], img["fileName"])
    except Exception as e:
        print("=====",e,"=====")
        print(img)
        print()
        
    return(img["i"])
 
async def main(imgList):
    futures = [asyncio.ensure_future(download(img)) for img in imgList]
    result = await asyncio.gather(*futures)                # 결과를 한꺼번에 가져옴
    print("Downloading...  done", end="\r")


# %%
def removeAllFile(filePath):
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)
#             print(file.path)
        return 'Remove All File'
    else:
        return 'Directory Not Found'
    
    

def zipImages(src_path, dest_file):
    with zipfile.ZipFile(dest_file, 'w') as zf:
        rootpath = src_path
        for (path, dir, files) in os.walk(src_path):
            for file in files:
                fullpath = os.path.join(path, file)
                relpath = os.path.relpath(fullpath, rootpath)
                zf.write(fullpath, relpath, zipfile.ZIP_DEFLATED)
        zf.close()
    
def imageListing(imageDomList):
    imgList = []
    for i in range(0, len(imageDomList)):
        tempImgURL = imageDomList[i].get("data-orig-src")
        if tempImgURL == None:
            imgURL = imageDomList[i].get("src")
        else:
            imgURL = tempImgURL
        temp = {
            "URL": imgURL ,
            "fileName": "./temp/" + str(i).rjust(3, '0') + ".jpg",
            "i": i
        }
        imgList.append(temp)
    return imgList

def toSoup(URL):
    req = requests.get(URL)
    html = req.text
    return BeautifulSoup(html, 'html.parser')

def toArrURL(URL):
    return re.split("\/\/|\/|http:|https:", URL)[2:]


# %%
arrURL = toArrURL(input("텀블러 주소를 입력해 주세요 : "))
taglistPage = "https://"+ "/".join(arrURL)
while True:
    title = input("압축파일의 제목을 입력해 주세요 : ")
    if len(title.split(" ")) > 1:
        print("띄어쓰기(' ')는 입력할 수 없습니다.")
        continue
    else:
        break

postURLList = []
while True:
    soup = toSoup(taglistPage)
    print("on = " + taglistPage)
    imageDomList = soup.select("#posts > div > article.text.not-page > div > section.post > div > h2 > a")
    for i in range(0, len(imageDomList)):
        postURLList.append(imageDomList[i].get("href"))
    nextBtn = soup.find("a", class_="next")
    if nextBtn == None:
        break
    else:
        taglistPage = "https://"+arrURL[0]+nextBtn.get("href")

postURLList.reverse()
if False == os.path.isdir("./temp"):
    os.mkdir("./temp")
if False == os.path.isdir("./aircomix_docker_server/aircomix"):
    os.mkdir("./aircomix_docker_server/aircomix")
os.mkdir("./aircomix_docker_server/aircomix/"+title)
nnnn = 1
for postURL in postURLList:
    print("on = " + postURL)
    print("title = ", title, nnnn)
    soup = toSoup(postURL)
    imageDomList = soup.select("#posts > div > article > div > section.post > div > div > p > img")
    
    imgList = imageListing(imageDomList)
    
    loop = asyncio.get_event_loop()          # 이벤트 루프를 얻음
    loop.run_until_complete(main(imgList))   # main이 끝날 때까지 기다림
    
    zipImages(os.getcwd()+"/temp/", os.getcwd()+"/aircomix_docker_server/aircomix/"+title+"/"+title+"_"+str(nnnn)+".zip")
    removeAllFile("./temp")
    nnnn += 1

os.rmdir("./temp")

# %%
loop.close()                             # 이벤트 루프를 닫음


# %%


