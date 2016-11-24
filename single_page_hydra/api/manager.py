from threading import Thread

from single_page_hydra.api.cache import DumbCache
from single_page_hydra.api.clients import (
    pixapi,
    WikiAPI,
    TwitterAPI,
)


class ApiManager:
    def __init__(self):
        self._cache = DumbCache()
        self._clients = [
            pixapi(),
            WikiAPI(),
            TwitterAPI(),
        ]

    def search(self, query):
        """
        Get the results from all of the APIs.

        :param query: Search string for the API queries.
        :type query: str
        :return: Dictionary of the results from the API clients.
        :rtype: dict
        """

        # Check the cache before sending out requests.
        cached_results = self._cache.get(query)
        if cached_results is not None:
            return cached_results

        # Fire up all of the worker threads.
        workers = [ApiClientWorker(client, query) for client in self._clients]
        for worker in workers:
            worker.start()

        # Gather the results from the workers when they are done.
        results = dict()
        while len(workers) > 0:
            for worker in workers:
                if worker.done:
                    results.update(worker.result)
                    workers.remove(worker)

        self._cache.put(query, results)

        return results


class ApiClientWorker(Thread):
    """ Thread worker for getting the result of a query from an API client. """

    def __init__(self, client, query):
        super().__init__(daemon=True)
        self.client = client
        self.query = query
        self.result = None
        self.done = False

    def run(self):
        self.result = self.client.search(self.query)
        self.done = True
