import selenium
from selenium import webdriver
import time
import requests
import os
from PIL import Image
import io
import hashlib

# DRIVER_PATH = '/home/aditasyhari/Downloads/chromedriver_linux64/chromedriver'
DRIVER_PATH = './chromedriver'


def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    while image_count < max_links_to_fetch:

        actual_images = wd.find_elements_by_css_selector('img.Q4LuWd')

        for actual_image in actual_images:
            if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                image_urls.add(actual_image.get_attribute('src'))
                # image_urls.add(actual_image.get_attribute('src'))
                # print(image_urls.add(actual_image.get_attribute('src')))

        image_count = len(image_urls)
        # print(image_count)
        scroll_to_end(wd)

    imagelinks = []
    for a,i in enumerate(image_urls):
        if a >= max_links_to_fetch:
            break
        imagelinks.append(i)
        # print(i)

    print(len(imagelinks))

    return imagelinks
    # for a,i in enumerate(imagelinks):
    #     print(i)

def persist_image(folder_path:str,file_name:str,url:str):
    try:
        image_content = requests.get(url).content
        print(url)

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        folder_path = os.path.join(folder_path,file_name)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        else:
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=95)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

if __name__ == '__main__':
    wd = webdriver.Chrome(executable_path=DRIVER_PATH)
    queries = ["Cr7","Messi","Aguero"]
    for query in queries:
        links = fetch_image_urls(query,200,wd)
        images_path = '/home/aditasyhari/Project Python/images_scrapping'
        for i in links:
            persist_image(images_path,query,i)

    wd.quit()