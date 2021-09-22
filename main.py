import os
import requests
import urllib
from bs4 import BeautifulSoup


GOOGLE_IMAGE = \
    'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

# usr_agent = {
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#     'Accept-Encoding': 'none',
#     'Accept-Language': 'en-US,en;q=0.8',
#     'Connection': 'keep-alive',
# }

SAVE_FOLDER = 'images_scrapping'

def main():
    if not os.path.exists('/home/aditasyhari/Project Python/'+SAVE_FOLDER):
        os.mkdir('/home/aditasyhari/Project Python/'+SAVE_FOLDER)
    download_images()
    
def download_images():
    data = input('Masukan keyword gambar : ')
    n_images = int(input('Berapa gambar yang di inginkan? '))
    data_lower = data.lower()

    print('Start searching...')
    
    keyword = urllib.parse.quote_plus(data_lower)
    # print(keyword)

    searchurl = GOOGLE_IMAGE + 'q=' + keyword
    print(searchurl)

    def getdata(url): 
        r = requests.get(url) 
        return r.text 
	
    htmldata = getdata(searchurl) 
    soup = BeautifulSoup(htmldata, 'html.parser')

    results = soup.find_all('img', limit=n_images+1)
    
    imagelinks = []
    for i, re in enumerate(results):
        if i == 0:
            continue

        imagelinks.append(re['src'])
        # print(re['src'])

    print(f'found {len(imagelinks)} images')
    print('Start downloading...')

    for a, imagelink in enumerate(imagelinks):

        print(imagelink)
        download = requests.get(imagelink)
        
        # imagename = SAVE_FOLDER + '/' + data_lower + str(a + 1) + '.jpg'
        # with open(imagename, 'wb') as file:
        #     file.write(download.content)

    print('Done')


if __name__ == '__main__':
    main()