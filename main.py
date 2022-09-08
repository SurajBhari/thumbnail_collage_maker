
import scrapetube
import json
from os import listdir, remove, path
import requests
from os import system, getcwd
from difPy import dif
from collage_maker import make_collage

#channel_id = 'UCIzzPhdRf8Olo3WjiexcZSw'
channel_id = str(input("Enter Channel ID "))
cur_path = getcwd()


if channel_id + ".json" not in listdir(cur_path):   
    videos = scrapetube.get_channel(channel_id)
    count =0
    x = {'data':[]}
    for video in videos:
        x['data'].append(video)

    with open(path.join(cur_path, f'{channel_id}.json'), 'w') as outfile:
        json.dump(x, outfile, indent=4)
        print("File Created")
else:
    print('File Already Exists')

data = json.load(open(path.join(cur_path,f'{channel_id}.json')))
files = listdir(path.join(cur_path, 'unique_thumbnails'))
for file in files:
    if not file.startswith(channel_id):
        remove(path.join(path.join(cur_path, 'unique_thumbnails', file)))
        files.remove(file)
for video in data['data']:
    if channel_id + "_" + video['videoId']+'.jpg' in files:
        print(video['videoId'] + " Already Exists")
        continue
    url = video['thumbnail']['thumbnails'][-1]['url']
    id = video['videoId']
    response = requests.get(url)
    open(path.join(cur_path, f"unique_thumbnails/{channel_id}_{id}.jpg"), "wb").write(response.content)

search = dif(path.join(cur_path, "unique_thumbnails/"))
for lower_quality in search.lower_quality:
    remove(lower_quality)

files = [fn for fn in listdir(path.join(cur_path, 'unique_thumbnails/'))]
images = [path.join(cur_path, "unique_thumbnails/", file) for file in files if file.endswith('.jpg') and file.startswith(channel_id)]
print('attempting to make a collage now')

width = 4500 # you can change this accordingly
init_height = 200 # same
make_collage(images, path.join(cur_path, f'{channel_id}.png'), width, init_height)

system(path.join(cur_path, f'{channel_id}.png'))