# BugCrawler Script

This script will crawl web application/sites written using PHP
looking for any PHP errors that might have been printed in the html
markup and gone unnoticed by the developer(s).

It will take an url as the input to start with and crawl it to find errors.
Also, while being at it, it will accumulate a set of other internal urls to 
crawl and loop over until the entire application is checked.

I know its a bit wierd but it works for me!

## Usage: 

python bugcrawler url

## Todos

Authentication - Crawling the app as a logged in user
