from pprint import pprint

from single_page_hydra.api import ApiManager
from single_page_hydra.api.clients.PixApi import pixapi
import json

# pa = pixapi()
# res = pa.search_image('rabbit')
# for image in res['hits']:
#     print(image)
#
# video_json = pa.search_video('rabbit')
# print('Video json:\n' + json.dumps(video_json, sort_keys=True, indent=4))


api_manager = ApiManager()
results = api_manager.search('rabbit')
pprint(results)

#
# vid = pa.search_video('mountain')
# print(vid['hits'][0]['videos']['small']['url'])
# # for piece in vid:
#     print(json.dumps(vid, sort_keys = True, indent=4))