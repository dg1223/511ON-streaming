import requests
import json
import io
import asyncio

import aiohttp
from PIL import Image

def get_response(api):
    return requests.get(api).json()

def get_number_of_cameras(api):
    return get_response(api)["recordsTotal"]
    

def get_camera_ids(api):
    response = get_response(api)
    cameras = [camera for camera in response["data"]]
    camera_ids = [camera["id"] for camera in cameras]
    
    return camera_ids
    
async def fetch_images(session, url, camera_id):
    image_url = url + camera_id
    if image_url.startswith("https"):
        image_name = "511ON_image_" + camera_id + ".jpeg"
        async with session.get(image_url) as response:
            image_binary = await response.read()
            image = Image.open(io.BytesIO(image_binary))
            image.save(image_name)

async def get_images_from_cctv(url, camera_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_images(session, url, camera_id) for camera_id in camera_ids]
        await asyncio.gather(*tasks)
        

if __name__ == "__main__":
    url = "https://511on.ca/map/cctv/"
    
    '''
    TODO: images should be retrieved in batches
    '''
    start = 0
    length = 20
    
    api = f'https://511on.ca/List/GetData/Cameras?query={{"columns":[],"start":{start},"length":{length}}}'
    
    # camera_ids = get_camera_ids(api)
    
    # # Fetch images asynchronously
    # asyncio.run(get_images_from_cctv(url, camera_ids))
    
    print(get_number_of_cameras(api))
