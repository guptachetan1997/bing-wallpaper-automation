import requests
import random
import os
import datetime
from bs4 import BeautifulSoup
import traceback
import shutil

home= os.path.expanduser("~")
directory = home + "/Pictures/bing_wallpapers"

user_agents = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0'
]

def modify_resolution(url):
    url = url[:len(url)-13] + "_1920x1080.jpg"
    return url

# get todays wallpaper
def request_wallpaper(url):
  try:
    headers = { "User-Agent": random.choice(user_agents)}
    r = requests.get(url, headers = headers)
    # r.raise_for_status()
    html = r.text.encode("utf8")
    soup = BeautifulSoup(html, "lxml")
    ex = soup.find('image')
    eex = ex.find('url')
    photo_text = ex.find('copyright')
    print (photo_text.text)
    photo_url =  "http://www.bing.com" + eex.text
    photo_url = modify_resolution(photo_url)
    res = requests.get(photo_url,headers = headers)
    date = str(datetime.date.today()) + ".jpg"
    imageFile = open(os.path.join(directory,date),'wb')
    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()
  except:
    print ("error fetching the wallpaper...")
    print (traceback.format_exc())


def save_wallpaper():
  # download the daily release of the bing wallpaper by microsoft
  url = "http://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=en-IN"
  if os.path.exists(directory) == False:
      os.makedirs(directory)
  request_wallpaper(url)

#change wallpaper
def change_wallpaper():
    save_wallpaper()
    path= directory + "/"
    date = str(datetime.date.today()) + ".jpg"
    try:
        settings= "gsettings set org.gnome.desktop.background picture-uri file://" + path
        os.system(settings + date)
    except:
        print ("there was some problem changing the wallpaper")
        print (traceback.format_exc())

# organise wallpaper directory on year basis to de-clutter. all files except for current year get their own folders
def archive():
    wallpaper_path= directory
    try:
        current_year= str(datetime.datetime.now().year)
        for file in os.listdir(wallpaper_path):     # list all files
            if os.path.isfile(os.path.join(wallpaper_path, file)): # check if it's a file
                file_year= file.split("-")[0]
                if current_year == file_year:
                    continue
                if os.path.exists(os.path.join(wallpaper_path,file_year)) == False:
                    os.makedirs(os.path.join(wallpaper_path,file_year))
                shutil.move(os.path.join(wallpaper_path, file), os.path.join(wallpaper_path,file_year))
    except:
        print ("there was some error moving the files")
        print (traceback.format_exc())

if __name__ == '__main__':
    change_wallpaper()
