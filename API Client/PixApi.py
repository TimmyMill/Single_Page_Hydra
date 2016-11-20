import requests
import key

class pixapi:
    def __init__(self):
        self.key = '?key='+(key.key)
        self.base_url = 'https://pixabay.com/api/'
        self.q='&q='
        self.image_type='&image_type='


    def search_image(self, search_param):
        self.image_type+='photo'


    def search_video(self, search_param):
        new_base_url=self.base_url+'/videos/'
        self.image_type+=''