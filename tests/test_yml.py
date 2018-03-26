import unittest
import yaml
import feedparser


class TestConfigs(unittest.TestCase):

    def setUp(self):
        with open('headlines/config.yml') as file:
            cfg = yaml.load(file)
        self.config = cfg

    def test_default_publication(self):
        default = self.config['DEFAULT']['publication']
        test_city = 'London, UK'
        test_currency_to = 'USD'
        test_currency_from = 'GBP'
        self.assertEqual(default['bbc']['city'], test_city)
        self.assertEqual(default['currency_to'], test_currency_to)
        self.assertEqual(default['currency_from'], test_currency_from)

    def test_feeds_configs(self):
        feeds = self.config['RSS_FEEDS']
        bbc = 'http://feeds.bbci.co.uk/news/rss.xml'
        cnn = 'http://rss.cnn.com/rss/edition.rss'
        fox = 'http://feeds.foxnews.com/foxnews/latest'
        self.assertEqual(feeds['bbc'], bbc)
        self.assertEqual(feeds['cnn'], cnn)
        self.assertEqual(feeds['fox'], fox)

    def test_feeds_active(self):
        feeds = self.config['RSS_FEEDS']
        list_of_feeds = ['bbc', 'cnn', 'fox', 'iol', 'fivethirtyeight']
        for publication in list_of_feeds:
            feed = feedparser.parse(feeds[publication])
            self.assertEqual(feed['status'], 200)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
