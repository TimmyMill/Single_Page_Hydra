import requests
import key

class pixapi:
    def __init__(self):
        self.key = '?key='+(key.key)
        self.base_url = 'https://pixabay.com/api/'
        self.q='&q='
        self.image_type='&image_type=all'
        self.safesearch='&safesearch=true'

    def search_image(self, search_param):
        res = requests.get(self.base_url+self.key+self.q+search_param+self.image_type+self.safesearch)
        return res.json()



    def search_video(self, search_param):
        new_base_url=self.base_url+'/videos/'
        res = requests.get(new_base_url + self.key + self.q + search_param + self.image_type + self.safesearch)
        return res.json()#['hits'][0]['videos']['small']['url']