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
        xdebug_html = """
	<br />
	<font size='1'><table class='xdebug-error' dir='ltr' border='1'
	cellspacing='0' cellpadding='1'>
	<tr><th align='left' bgcolor='#f57900' colspan="5"><span
	style='background-color: #cc0000; color: #fce94f; font-size:
	x-large;'>( ! )</span> Notice: Undefined index: type in /home/vineet/public_html/projects.kp/cat/application/controllers/AccountController.php on line <i>9</i></th></tr>
	<tr><th align='left' bgcolor='#e9b96e' colspan='5'>Call Stack</th></tr>
	<tr><th align='center' bgcolor='#eeeeec'>#</th><th align='left'
	bgcolor='#eeeeec'>Time</th><th align='left'
	bgcolor='#eeeeec'>Memory</th><th align='left'
	bgcolor='#eeeeec'>Function</th><th align='left'
	bgcolor='#eeeeec'>Location</th></tr>
	<tr><td bgcolor='#eeeeec' align='center'>1</td><td bgcolor='#eeeeec'
	align='center'>0.0024</td><td bgcolor='#eeeeec'
	align='right'>339312</td><td bgcolor='#eeeeec'>{main}(  )</td><td
	title='/home/vineet/public_html/projects.kp/cat/index.php'
	bgcolor='#eeeeec'>../index.php<b>:</b>0</td></tr>
        """
        bugs = scrap_bugs(xdebug_html)
        self.assertTrue(bugs);

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    unittest.main(testRunner=runner)
