#!/usr/bin/env python

from sys import argv
import re
import urllib2
from urlparse import urlparse

PATTERN_LINKS = re.compile(r'<a\s*href=[\'"](.+?)[\'"].*?>')

PHP_ERRORS = ['(<b>Warning</b>\s?:\s?.* on line <b>\d+</b>)', 
              '(<b>Fatal Error</b>\s?:\s?.* on line <b>\d+</b>)', 
              '(<b>Notice</b>\s?:\s?.* on line <b>\d+</b>)']

PHP_ERROR_PATTERNS = [re.compile(x, re.I) for x in PHP_ERRORS]

def scrap_bugs(content, log_inline=False):
    """
    Function to find PHP errors in the passed html content
    and in case of any errors display them in the terminal
    as per the log_inline flag
    """
    bugs = []
    for p in PHP_ERROR_PATTERNS:
        bugs.extend(match_bug_pattern(p, content))
    if len(bugs) and log_inline:
        log_bugs_inline(bugs)
    return bugs

def match_bug_pattern(pattern, content):
    """
    Function to search the content for an error pattern
    """
    m = pattern.search(content)
    return [] if m is None else m.groups()

def log_bugs_inline(bugs):
    """
    Function to log the bugs inline ie. as the crawling happens
    """
    indent = ' ' * 4
    delim = "\n" + indent + "|--"
    print indent, "|--", delim.join(bugs)
    # raw_input('press enter to continue..')

def scrap_links(content):
    """
    Function to scrap the html content and find all links
    by matching with the defined pattern PATTERN_LINKS
    """
    result = PATTERN_LINKS.findall(content)
    return [] if result is None else result

def generate_report(crawler):
    """
    Function to show the bug report after all the links have been crawled
    """
    print '-'*60
    print ' '*22, 'BugCrawler Report', ' '*22
    print '-'*60
    print 'Total links crawled: %d' % len(crawler.crawled)
    print 'Bugs found: %d' % len(crawler.bugs)
    if len(crawler.bugs) == 0:
        print 'Congrats!'
    else:
        for link, bugs in crawler.bugs:
            print link, ':'
            for b in bugs:
                print ' '*4, '|--', b
        print 'Oops! Might want get back to more bug fixing!'
    print '-'*60
        

class BugCrawler(object):
    """
    The main class for maintaining the state of scrapped links,
    found bugs and also doing the crawling
    """
    
    def __init__(self, link):
        self.link = link
        self.app_base_url = '%s://%s' % (urlparse(link)[:2])
        self.links = set([self.link])
        self.crawled = set([])
        self.bugs = []

    # main function that will do the work
    def crawl(self):
        """
        Function to crawl the urls starting with the user specified url
        and build a set of internal links from the crawled content and 
        looping over
        """

        def linkfltr(x):
            """
            Internal function to filter out urls that are invalid, external
            or already added, from getting added to the to-be-crawled list
            """
            return (self.is_valid(x) 
                    and not self.is_external_link(x) 
                    and not self.is_crawled(x)
                    and x not in [self.link])

        current = self.links.pop()
        print 'Crawling..'
        while current:
            # self.brute_force_debug(current)
            content = self.get_html_content(current)
            bugs = scrap_bugs(content, log_inline=True)
            if len(bugs):
                self.bugs.append((current, bugs))
            self.links.update(filter(linkfltr, scrap_links(content)))
            try:
                current = self.links.pop()
            except KeyError:
                current = None
        print 'Done..'
        generate_report(self)

    def get_html_content(self, link):
        """
        Function to get html response from the url passed as string
        """
        print '->', link
        try:
            req = urllib2.Request(link, headers={
                    'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
                    })
            content = urllib2.urlopen(req).read()
        except urllib2.HTTPError, e:
            # we will fetch html content of an error page too
            content = e.fp.read()
        except ValueError:
            content = ''
        self.crawled.add(link)
        return content

    def is_valid(self, link):
        """
        Check if the link is valid or not (
        in the context of this script only.)
        """
        invalid = ['#','!#']
        return (not link in invalid and not link.startswith('#'))

    def is_external_link(self, link):
        """
        Check whether the url points to an external site
        (To be discarded for the requirement of this script)
        """
        return (not link.startswith(self.app_base_url)
                and (link.startswith('http://') or link.startswith('https://')))

    def is_crawled(self, link):
        """
        Check if the url has already been crawled before
        """
        possible = set([link])
        if not link.endswith('/'):
            possible.add(link+'/')
        else:
            possible.add(link[:-1])
        return len(self.crawled.intersection(possible))

    def brute_force_debug(self, current):        
        print '----- ', current                
        print self.links
        print '----- '
        print self.crawled
        raw_input('>')

if __name__ == '__main__':
    script, site = argv
    crawler = BugCrawler(site)
    crawler.crawl()
    pass
