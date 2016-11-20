from single_page_hydra.api.clients.PixApi import pixapi
import json
pa = pixapi()
#
# res = pa.search_image('rabbit')
# print(res)

vid = pa.search_video('mountain')
print(vid)
# for piece in vid:
#     print(json.dumps(vid, sort_keys = True, indent=4))