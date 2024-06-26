import requests
import json
import os
import io

from PIL import Image


def get_camera_ids(url, headers, api):
    response = requests.get(api, headers=headers).json()
    cameras = [camera for camera in response["data"]]
    camera_ids = [camera["id"] for camera in cameras]
    
    return camera_ids
    
def get_images_from_cctv(url, camera_ids):
    for camera in camera_ids:
        image_url = url + camera
        if image_url.startswith("https"):
            image_name = "511ON_image_" + camera + ".jpeg"
            image_binary = requests.get(image_url).content        
            image = Image.open(io.BytesIO(image_binary))
            image.save(image_name)

if __name__ == "__main__":
    url = "https://511on.ca/map/Cctv/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
    }
    '''
    TODO:
    1. start and length should be parameters
    2. images should be retrieved in batches
    '''
    api = 'https://511on.ca/List/GetData/Cameras?query={"columns":[{"data":null,"name":""},{"name":"sortId","s":true},{"name":"cityName","s":true},{"name":"roadway","s":true},{"data":4,"name":""}],"order":[{"column":1,"dir":"asc"},{"column":3,"dir":"asc"}],"start":0,"length":20,"search":{"value":""}}&lang=en'
    
    camera_ids = get_camera_ids(url, headers, api)
    get_images_from_cctv(url, camera_ids)



        