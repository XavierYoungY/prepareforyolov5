import json
import os

json_file = 'all.json'
with open(json_file) as f:
    data = json.load(f)
    imgs = data['images']

img_folder=''

img_paths=[]
for img in imgs:
    path = os.path.join(img_folder, img['file_name'])
    img_paths.append(path)

path = '\n'.join(img_paths)
with open('names.txt','w') as f:
    f.write(path)
pass
