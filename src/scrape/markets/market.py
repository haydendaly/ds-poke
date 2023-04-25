# Description: Base class for all markets
class Market:
    def __init__(self, name, url, language="en"):
        self.name = name
        self.url = url
        self.language = language

    def search(self, query, page=0):
        # search for items based on the query
        pass

    def get_item_details(self, item_id):
        # get details for a specific item
        pass
