from single_page_hydra.api.clients.PixApi import pixapi
import json
pa = pixapi()
#
res = pa.search_image('rabbit')
for image in res['hits']:
    print(image)
#
# vid = pa.search_video('mountain')
# print(vid['hits'][0]['videos']['small']['url'])
# # for piece in vid:
#     print(json.dumps(vid, sort_keys = True, indent=4))