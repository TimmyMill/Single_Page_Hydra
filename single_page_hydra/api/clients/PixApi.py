import os
import requests
from queue import Queue
from threading import Thread

from single_page_hydra.api.keys import PIX_KEY as KEY


class ProcessUrlWorker(Thread):
    def __init__(self, proccess_url_func, urls, filenames):
        super().__init__()
        self.func = proccess_url_func
        self.urls = urls
        self.filenames = filenames

    def run(self):
        while True:
            url = self.urls.get()
            filename = self.func(url)
            self.filenames.put(filename)
            self.urls.task_done()


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

        url_queue = Queue()
        filename_queue = Queue()

        # Fire up some worker threads.
        for _ in range(10):
            worker = ProcessUrlWorker(self._process_url, url_queue,
                                      filename_queue)
            worker.daemon = True
            worker.start()

        # Queue up some URLs to process.
        for url in urls:
            url_queue.put(url)

        # Wait for threads to finish.
        url_queue.join()

        return list(filename_queue.queue)

    def _process_url(self, url):
        filename = self._extract_filename(url)
        image_path = os.path.join(self.images_dir, filename)
        # Download the file if we don't have it.
        if not os.path.isfile(image_path):
            res = requests.get(url)
            with open(image_path, 'wb') as f:
                f.write(res.content)

        return filename

    @staticmethod
    def _extract_filename(url):
        filename = url.split('/')[-1]

        # Normalize the filename because the same image from Pixabay can have
        # different filenames.  I believe the first 10 characters of the
        # filename are the ones we are interested in.
        name, extension = filename.split('.')
        name = name[:10]

        return '{}.{}'.format(name, extension)


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
        image_urls =[image['webformatURL'] for image in images_json['hits']]
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
