from wikipedia import wikipedia, summary, DisambiguationError


class WikiAPI:
    def __init__(self):
        self.article = ''

    def search(self, query):
        try:
            self.article = wikipedia.page(title=query)

        except DisambiguationError as e:
            # list of articles returned by wikipedia when a search is too ambiguous
            titles = e.options
            # let's select the first one and return it
            self.article = wikipedia.page(titles[0])

        finally:
            title = self.article.title
            url = self.article.url
            article_summary = summary(title=title, sentences=3)

            return \
                {
                    'wikipedia':
                        {
                            'summary': article_summary,
                            'link': url
                        }
                }

# from wikipedia import *
#
#
# def search(query):
#     article = get_page(query)
#     title = article.title
#     url = article.url
#     article_summary = summary(title=title, sentences=3)
#
#     return {'results': {'link': url, 'summary': article_summary}}
#
#
# def get_page(query):
#     try:
#         result = wikipedia.page(title=query)
#         return result
#
#     # raise DisambiguationError(getattr(self, 'title', page['title']), may_refer_to)
#     except DisambiguationError as e:
#         titles = e.options
#         # for title in titles:
#         #     print(title)
#         result = wikipedia.page(titles[0])
#         # print(result.title)
#         return result
