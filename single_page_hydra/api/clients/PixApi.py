import os
import requests

from single_page_hydra.api.keys import PIX_KEY as KEY


class ImageDownloader:
    """ Downloads images from pixabay to avoid hot linking."""
    def __init__(self):
        import single_page_hydra
        base_path = os.path.dirname(single_page_hydra.__file__)
        self.images_dir = os.path.join(base_path, 'static', 'images', 'pixabay')
        os.makedirs(self.images_dir, exist_ok=True)

    def get_filenames(self, urls):
        """
        Return a list of filenames for pixabay images.  This will also
        download the images if we do not have a local copy.

        :param urls: List of URLs to pixabay images.
        :type urls: list[str]
        :return: List of filenames.
        :rtype: list[str]
        """

        # TODO: This needs some threading for the download.
        filenames = list()
        for url in urls:
            filename = url.split('/')[-1]
            filenames.append(filename)
            image_path = os.path.join(self.images_dir, filename)

            # Download the file if we don't have it.
            if not os.path.isfile(image_path):
                res = requests.get(url)
                with open(image_path, 'wb') as f:
                    f.write(res.content)

        return filenames


class pixapi:
    def __init__(self):
        self.key = '?key=' + KEY
        self.base_url = 'https://pixabay.com/api/'
        self.q = '&q='
        self.image_type = '&image_type=all'
        self.safesearch = '&safesearch=true'
        self.downloader = ImageDownloader()

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
        images = self.downloader.get_filenames(image_urls)

        video_json = self.search_video(query)
        if video_json['total'] > 0:
            video_url = video_json['hits'][0]['videos']['small']['url']
        else:
            video_url = None

        return \
            {
                'pixabay':
                    {
                        'images': images,
                        'video': video_url
                    }
            }

