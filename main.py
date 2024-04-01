import scrapetube
import json
from os import listdir, remove, path
import requests
from os import system, getcwd
import difPy
from collage_maker import make_collage

def main():
    # channel_id = 'UCIzzPhdRf8Olo3WjiexcZSw'
    channel_id = str(input("Enter Channel ID "))
    cur_path = getcwd()

    videos = scrapetube.get_channel(channel_id)
    data = []
    for video in videos:
        data.append(video)

    if not path.exists(path.join(cur_path, channel_id)):
        system(f"mkdir {path.join(cur_path, channel_id)}")

    files = listdir(path.join(cur_path, channel_id))

    for file in files:
        if not file.startswith(channel_id):
            remove(path.join(path.join(cur_path, channel_id, file)))
            files.remove(file)
    for video in data:
        if channel_id + "_" + video["videoId"] + ".jpg" in files:
            print(video["videoId"] + " Already Exists")
            continue
        url = video["thumbnail"]["thumbnails"][-1]["url"]
        id = video["videoId"]
        response = requests.get(url)
        file_name = path.join(cur_path, f"{channel_id}/{channel_id}_{id}.jpg")
        open(file_name, "wb+").write(
            response.content
        )
        print(f"stored {file_name}")

    print("thumbnails downloaded")
    dif = difPy.build(channel_id)
    print("created difUCZy7vibLOxrNyngoHJByZfw")
    search = difPy.search(dif)
    search.delete(search)
    print("deleted duplicates")


    files = [fn for fn in listdir(path.join(cur_path, "/"))]
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

if __name__ == "__main__":
    main()
