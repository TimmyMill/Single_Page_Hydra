import requests

from single_page_hydra.api import keys as KEY


class pixapi:
    def __init__(self):
        self.key = '?key=' + (KEY.PIX_KEY)
        self.base_url = 'https://pixabay.com/api/'
        self.q = '&q='
        self.image_type = '&image_type=all'
        self.safesearch = '&safesearch=true'

    def search_image(self, search_param):
        res = requests.get(self.base_url + self.key + self.q + search_param + self.image_type + self.safesearch)
        return res.json()

    def search_video(self, search_param):
        new_base_url = self.base_url + '/videos/'
        res = requests.get(new_base_url + self.key + self.q + search_param + self.image_type + self.safesearch)
        return res.json()  # ['hits'][0]['videos']['small']['url']

    def search(self, query):
        images_json = self.search_image(query)
        image_urls = [image['webformatURL'] for image in images_json['hits']]

        video_json = self.search_video(query)
        if video_json['total'] > 0:
            video_url = video_json['hits'][0]['videos']['small']['url']
        else:
            video_url = None

        return {
            'pixabay':
                {
                    'images': image_urls,
                    'video': video_url
                }
        }

