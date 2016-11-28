from datetime import datetime, timedelta


class CachedContent:
    """ A class for storing content in a cache. """
    def __init__(self, content, max_age):
        self.content = content
        self.max_age = max_age
        self.timestamp = datetime.now()


class DumbCache:
    """
    A cache with the minimum amount of features needed to function.

    :type storage: dict[str, CachedContent]
    """
    def __init__(self):
        self.storage = dict()

    def get(self, key):
        """
        Return the thing from the cache or None if it expired or doesn't exist.

        :param key: The name of the thing to get from the cache.
        :type key: str
        :return: The thing that was stored in the cache.
        :rtype: object | None
        """

        # Check if the thing is in the cache.
        cached_content = self.storage.get(key, None)
        if cached_content is None:
            return

        # Check if the content is past it's expiry time.
        age = datetime.now() - cached_content.timestamp
        if age >= cached_content.max_age:
            del self.storage[key]

        return cached_content.content

    def put(self, key, content, max_age=(60 * 5)):
        """
        Store stuff in the cache.

        :param key: Name used to retrieve stuff out of the cache later.
        :type key: str
        :param content: Stuff to put in the cache.
        :type content: object
        :param max_age: Number of seconds the stuff should stay in the cache.
        :type max_age: timedelta
        """
        max_age = timedelta(seconds=max_age)
        self.storage[key] = CachedContent(content, max_age)
