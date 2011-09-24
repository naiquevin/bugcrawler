#!/usr/bin/env python

from sys import argv
import re
import urllib2
from urlparse import urlparse

PATTERN_LINKS = re.compile(r'<a\s*href=[\'"](.+?)[\'"].*?>')

PHP_ERRORS = ['Warning\s?:\s?Invalid argument\s?:\s?(.*)', 
              'Fatal Error\s?:\s?(.*)', 
              '<b>Notice</b>\s?:',
              '<b>Notice</b>\s?:\s?Undefined index:\s?(.*)']

PHP_ERROR_PATTERNS = [re.compile(x, re.I) for x in PHP_ERRORS]

class BugCrawler(object):
    def __init__(self, link):
        self.link = link
        self.app_base_url = '%s://%s' % (urlparse(link)[:2])
        print self.app_base_url
        self.links = set([self.link])
        self.crawled = set([])
        self.errors = []

    # main function that will do the work
    def crawl(self):    
        current = self.links.pop()
        print 'Crawling..'
        while current:
            print '->', current
            # content = urllib2.urlopen(current).read()
            content = self.scrap_content(current)
            errors = self.scrap_errors(content)
            if len(errors):
                print " " * 4, "|_", "::".join(errors)
                print "Bug found on %s" % (current)
                self.errors.append((current, errors))
                raw_input('press enter to continue..')
            # find other links on this page 
            scrapped_links = self.scrap_links(content, func=self.filter_links)
            # print scrapped_links
            self.links.update(scrapped_links)
            self.crawled.add(current)
            try:
                current = self.links.pop()
            except KeyError:
                current = None
        print 'Following are the errors'
        print self.errors

    def scrap_content(self, link):
        try:
            content = urllib2.urlopen(link).read()
        except ValueError:
            content = ''
        return content            

    def scrap_errors(self, content):
        err = []
        # todo use fp        
        def errors(p):
            e = p.search(content)
            if e is not None:                
                err.append(e.group(0))
                return True
            return False
        for i in PHP_ERROR_PATTERNS:
            errors(i)
        return err

    # find links by matching with regex
    def scrap_links(self, content, func=None):
        # print content, func
        result = PATTERN_LINKS.findall(content)
        if result is not None:
            if func is not None:
                return func(result)
            else: return result
        else: return []

    def filter_links(self, links):
        return [x for x in links if (self.is_valid(x) 
                                     and not self.is_external_link(x) 
                                     and not self.is_crawled(x))] 

    def is_valid(self, link):
        invalid = ['#','!#']
        return not link in invalid

    def is_external_link(self, link):
        return (not link.startswith(self.app_base_url)
                and (link.startswith('http://') or link.startswith('https://')))

    def is_crawled(self, link):
        possible = set([link])
        if not link.endswith('/'):
            possible.add(link+'/')
        else:
            possible.add(link[:-1])
        return len(self.crawled.intersection(possible))

if __name__ == '__main__':
    # site = 'http://vineetnaik.me/blog'
    script, site = argv
    # site = 'http://kodemall.com/demo/'
    crawler = BugCrawler(site)
    crawler.crawl()
    pass
