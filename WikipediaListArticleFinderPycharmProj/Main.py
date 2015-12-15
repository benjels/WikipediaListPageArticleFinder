__author__ = 'user'
# unfortunately, the way that lists of articles are done in wikipedia is not standardised and as
# it is not completely trivial to write code that can collect articles from lists that works for
# every article.
#
# what the algorithm will basically do is take some wikipedia pages as recursion start points
# and then recursively visit each page referenced in the body of the current page until it reaches a page that doesn't
# have the string "list of" or "lists of". When that happens, we have probably reached an article that might be about something
# to do with NZ. These are exactly the articles we want. It might also not be related to NZ. e.g. the article for "List of New
# Zealand architects" links to the wikipedia article "New Zealand". Towards the end of only collecting NZ related articles,
# We will only add articles to our master list of "goodArticles" if we find the string "new zealand" (or some differently cased variation)
# somewhere in that article.
#
# THINGS TO BE CAUTIOUS OF:
# 1) should exclude articles that have "list" or "lists" in the title from the final article master lsit
# 2) we are going to be getting articles from 2015 wikipedia and then trying to get the corresponding articles
# from a 2011 version of wikipedia (for now at least). So need to check that the articles actually existed back then
# when creating our collection of Topic (or whatever type is needed) objects from our master-list of articles.

from bs4 import BeautifulSoup
import requests

