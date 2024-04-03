import scrapetube
import json
from os import listdir, remove, path, removedirs
import requests
from os import system, getcwd
import difPy
from collage_maker import make_collage
import threading

threads = []

def download_video_thumbnail(videos, channel_id, cur_path):
    for video in videos:
        files = listdir(path.join(cur_path, channel_id))
        if channel_id + "_" + video["videoId"] + ".jpg" in files:
            print(video["videoId"] + " Already Exists")
            continue

        url = video["thumbnail"]["thumbnails"][-1]["url"]
        video_id = video["videoId"]
        response = requests.get(url)
        file_name = path.join(cur_path, f"{channel_id}/{channel_id}_{video_id}.jpg")
        with open(file_name, "wb+") as file:
            file.write(response.content)
        print(f"stored {file_name}")

def main():
    # channel_id = 'UCIzzPhdRf8Olo3WjiexcZSw'
    channel_id = str(input("Enter Channel ID "))
    cur_path = getcwd()

    contents_types = ['videos', 'shorts', 'streams']
    for content_type in contents_types:
        print(f"Downloading {content_type}")
        videos = scrapetube.get_channel(channel_id, content_type=content_type)
        data = []
        for video in videos:
            data.append(video)
        print(f"Downloaded {content_type} size -> {len(data)}")

    if not path.exists(path.join(cur_path, channel_id)):
        system(f"mkdir {path.join(cur_path, channel_id)}")

    
    each_part = len(data) // 10
    for i in range(10):
        if i == 9:
            videos = data[each_part * i:]
        else:
            videos = data[each_part * i:each_part * (i + 1)]
        thread = threading.Thread(target=download_video_thumbnail, args=(videos, channel_id, cur_path))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    print("thumbnails downloaded")
    dif = difPy.build(channel_id)
    search = difPy.search(dif)
    search.delete(True)
    print("deleted duplicates")

    files = [fn for fn in listdir(path.join(cur_path, channel_id))]
    images = [
        path.join(cur_path, channel_id, file)
        for file in files
        if file.endswith(".jpg") and file.startswith(channel_id)
    ]
    print("attempting to make a collage now")

    width = 4500  # you can change this accordingly
    init_height = 200  # same
    make_collage(images, path.join(cur_path, f"{channel_id}.png"), width, init_height)

    system(path.join(cur_path, f"{channel_id}.png"))
    print("collage created")
    if input("Do you want to delete the images? (y/n) ").lower() == "y":
        for file in listdir(path.join(cur_path, channel_id)):
            remove(path.join(cur_path, channel_id, file))
        removedirs(path.join(cur_path, channel_id))
        print("images deleted")
if __name__ == "__main__":
    main()
