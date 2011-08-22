
class FeedUpdater (object):
    """Responsible for updating the metadata in a feed"""

    def update(self, feed):
        """Changes the last_updated of a legfiles feed to most recent intro
           date"""
        content = feed.get_content()
        latest = max(feed.get_last_updated(item) for item in content)
        feed.last_updated = latest
        feed.save()
    
    def update_all(self, feeds):
        """Updates all the feeds in a collection (yes, it's just a for loop)"""
        for feed in feeds:
            self.update(feed)
