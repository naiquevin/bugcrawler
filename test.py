import unittest
from bugcrawler import BugCrawler, scrap_bugs

class BugCrawlerTest(unittest.TestCase):
    
    def test_is_crawled(self):
        crawler = BugCrawler('http://kodemall.com/demo')
        crawler.crawled.update(['http://kodemall.com/demo/', 
                        'http://kodemall.com/demo/rohitbegwani123/index.php?', 
                        'http://kodemall.com/demo/rohitbegwani123/index.php?route=information/sitemap'])
        self.assertTrue(crawler.is_crawled('http://kodemall.com/demo/rohitbegwani123/index.php?route=information/sitemap'))

    def test_is_external_link(self):
        crawler = BugCrawler('http://184.106.134.49/gr8menus/')
        self.assertTrue(crawler.is_external_link('http://www.google.com'))
        self.assertTrue(crawler.is_external_link('https://www.google.com'))

    def test_scrap_bugs(self):
        html = """
        <b>%s</b>: Undefined index: information_id in <b>/var/www/gr8menus/catalog/controller/information/information.php</b> on line <b>57</b><?xml version="1.0" encoding="UTF-8"?> 
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en" xml:lang="en">
        <head>
        <meta http-equiv="X-UA-Compatible" content="IE=8" />
        <title>Information Page Not Found!</title>
        <base href="http://184.106.134.49/gr8menus/" />
        """
        bugs = scrap_bugs(html % ('Notice'))
        self.assertTrue(bugs)
        bugs = scrap_bugs(html % ('Fatal Error'))
        self.assertTrue(bugs)
        bugs = scrap_bugs(html % ('Warning'))
        self.assertTrue(bugs)
        bugs = scrap_bugs(html % ('No Error'))
        self.assertFalse(bugs)        

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    unittest.main(testRunner=runner)
