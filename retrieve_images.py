import requests
import json
import io
import os
import sys
import asyncio

import aiohttp
from PIL import Image

storage_path = "/home/shamir/Documents/GitHub/511ON-streaming/"

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
    print(f"Fetching image from camera: {camera_id}")
    image_url = url + camera_id
    if image_url.startswith("https"):
        image_name = "511ON_image_" + camera_id + ".jpeg"
        full_filepath = storage_path + image_name
        async with session.get(image_url) as response:
            image_binary = await response.read()
            try:
                image = Image.open(io.BytesIO(image_binary))
                image.save(full_filepath)
            except Exception as e:
                print(e)
                

async def get_images_from_cctv(url, camera_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_images(session, url, camera_id) for camera_id in camera_ids]
        await asyncio.gather(*tasks)
        

if __name__ == "__main__":
    url = "https://511on.ca/map/cctv/"
    
    if len(sys.argv) < 2:
        print("Usage: python script.py <command> [<start> <length>]")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "get_total_cameras":
        start = 0
        length = 1
        api = f'https://511on.ca/List/GetData/Cameras?\
            query={{"columns":[],"start":{start},"length":{length}}}'
            
        total_cameras = get_number_of_cameras(api)
        with open("total_cameras.txt", "w") as f:
            f.write(str(total_cameras))
        print(f"number of available cameras = {total_cameras}")
        
    elif command == "fetch_images":
        if len(sys.argv) != 4:
            print("Usage: python script.py fetch_images <start> <length>")
            sys.exit(1)
            
        start = int(sys.argv[2])
        length = int(sys.argv[3])
        
        api = f'https://511on.ca/List/GetData/Cameras?query={{"columns":[],"start":{start},"length":{length}}}'
      
        camera_ids = get_camera_ids(api)
        
        # Fetch images asynchronously                
        asyncio.run(get_images_from_cctv(url, camera_ids))
