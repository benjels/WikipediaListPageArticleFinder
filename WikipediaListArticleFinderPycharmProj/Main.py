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
import regex


nzRelatedArticlesIDs = []#list of wikipedia IDs of nz relevant articles that we find
visitedURLs = [] #complete list of all URLs that have been visited. We should never visit the same URL more than once. This should really be a set but whatever.
WIKIPEDIA_URL_ROOT_STRING = "https://en.wikipedia.org" #many of the urls linked in the html are incomplete
MAX_DEPTH_ALLOWED = 2 # we are not going deep atm




#gross main that starts the recursive searching with several calls to findLinksToMoreArticles()
#will tidy this up and just use a console provided list of root/top-level articles when it actually works.
#writes the found article ids to a file at the end
#TODO: make this just iterate over a list of URLs
def main():
    global nzRelatedArticlesIDs

    ###put URLs here that broke the program in the past to test that it handles them ok####
    examineArticle("https://en.wikipedia.org//pl.wikipedia.org/wiki/Kategoria:Nowozelandzcy_medali%C5%9Bci_olimpijscy", 0)
    examineArticle("https://en.wikipedia.org/wiki/List_of_villages_and_neighbourhoods_in_the_Cook_Islands", 0)

    #######################################################################################

    #start our searches for nz wikipedia articles at a few high level wikipedia list articles...

    examineArticle("https://en.wikipedia.org/wiki/List_of_towns_in_New_Zealand", 0)
    progressLogFile = open("C:\!2015SCHOLARSHIPSTUFF\wikipediaNZRelatedScrapeResults\serachingProgress.txt", "w")
    progressLogFile.write("finished search that started with : " + "https://en.wikipedia.org/wiki/List_of_towns_in_New_Zealand \n")
    progressLogFile.close()

    examineArticle("https://en.wikipedia.org/wiki/Lists_of_New_Zealanders", 0)
    progressLogFile = open("C:\!2015SCHOLARSHIPSTUFF\wikipediaNZRelatedScrapeResults\serachingProgress.txt", "w")
    progressLogFile.write("finished search that started with : " + "https://en.wikipedia.org/wiki/Lists_of_New_Zealanders \n")
    progressLogFile.close()


    examineArticle("https://en.wikipedia.org/wiki/Category:Lists_of_places_in_New_Zealand", 0)
    progressLogFile = open("C:\!2015SCHOLARSHIPSTUFF\wikipediaNZRelatedScrapeResults\serachingProgress.txt", "w")
    progressLogFile.write("finished search that started with : " + "https://en.wikipedia.org/wiki/Category:Lists_of_places_in_New_Zealand \n")
    progressLogFile.close()


    #we have gathered all of the article IDs, so let's write them to a file that our java program will use
    fileToSaveIDs = open("C:\!2015SCHOLARSHIPSTUFF\wikipediaNZRelatedScrapeResults\idsAll.txt", "w")
    for each in nzRelatedArticlesIDs:
        fileToSaveIDs.write(each + "\n")
    fileToSaveIDs.close()
    print("program finished naturally after collecting the following amount of wikipedia article IDs: " + str(len(nzRelatedArticlesIDs)))


#Gets the content of the address provided as an arg and if the strings "list" and "new zealand" are in
#the title of that article, makes recursive calls for each URL found on that page. Passing each of those URLs as args.
#If the article is not identified as a list of other articles, then we send it to the determineNzArticleOrNot() function
#and if the string "new zealand" (or some differently cased variation) is found, then we save that article's id.
#depth is an int value that keeps track of how deep this recursive call is. e.g. as we keep recursively going deeper and deeper
#into list articles, this depth value increases. It is to stop us going on overly deep tangents.
#pathThroughArticlesSoFar is just used to keep of what path we have taken through wikipedia articles.
def examineArticle(wikipediaArticleURL, depthValue, pathThroughArticlesSoFar = ""):
    global visitedURLs

    #check that we haven't gone too deep into wikipedia...
    if depthValue == MAX_DEPTH_ALLOWED:
        print("%%%%%%%%%decay value got too high and we are not pursuing this branch any more. the path to this article was: " + pathThroughArticlesSoFar + " and the URL is: " + wikipediaArticleURL)
        print(pathThroughArticlesSoFar)
        return None

    #mark this URL as visited, so that we do not come here again
    assert wikipediaArticleURL not in visitedURLs, "this URL is already in visited collection. shouldnt have reached it again: " + wikipediaArticleURL
    visitedURLs.append(wikipediaArticleURL.lower()) #note that I'm using lower case for these URLs because they are never actually used for requests. Just used for reference of what's visited and what's not. Some articles' urls have variations in casing in wikipedia articles so some standardisation is required.
    print("just added the following URL to list of those visited:" + wikipediaArticleURL)

    #get the content at the wikipediaArticleURL and turn it into soup
    print("About to make a request to get the content at the URL: " + wikipediaArticleURL)
    try:
        articleToExamineResponse = requests.get(wikipediaArticleURL)
    except ConnectionError:
        print("connection error exception raised when requesting the url: " + wikipediaArticleURL + " just going to stop pursuing this branch.")
        progressLogFile = open("C:\!2015SCHOLARSHIPSTUFF\wikipediaNZRelatedScrapeResults\serachingProgress.txt", "w")
        progressLogFile.write("CONNECTION ERROR GETTING THIS URL: " + wikipediaArticleURL + "\n")
        progressLogFile.close()
        return None
    articleSoup = BeautifulSoup(articleToExamineResponse.text, 'html.parser')

    #if this article has "list" and "new zealand" in the title, then make recursive calls with the URLS
    #that it contains. Else, it is a "leaf" article and we should check whether we want to save its ID as an nz related article.
    lowerCaseArticleTitle = articleSoup.title.text.lower()
    if "list" in lowerCaseArticleTitle:
        if "new zealand" in lowerCaseArticleTitle:
            print("------FOUND NEW NZ LIST. the title : " + lowerCaseArticleTitle + " has the substring " + " \"list\" in it  as well as \"new zealand\" so making recursive calls to any article links we find on this nz articles list is: " + wikipediaArticleURL)
            print("------ ------  so the current list warticle is from the path: " + pathThroughArticlesSoFar)

            #find URLS on this page
            URLsOnThisPage = []
            for eachLink in articleSoup.find_all('a'):
                eachURLOnPageString = str(eachLink.get('href'))
                #filter out some things that are obviously not wikipedia article URLS
                if "/wiki/" in eachURLOnPageString:
                    #if the link is only a partial url, we need to attach the prefix
                    if "http" in eachURLOnPageString:
                        URLsOnThisPage.append(eachURLOnPageString)
                    else:
                        URLsOnThisPage.append(WIKIPEDIA_URL_ROOT_STRING + eachURLOnPageString)
            #make recursive call of this function for each URL we just found
            for eachURL in URLsOnThisPage:
                #check if it is an unvisited URL and if it is, visit it
                if eachURL.lower() not in visitedURLs:
                    print("making a recursive call to this URL because it is univisited we are currently in a list page:" + eachURL)
                    examineArticle(eachURL, depthValue + 1, pathThroughArticlesSoFar + " || " + wikipediaArticleURL)
                else:
                    print("----- not going to revisit this URL: " + eachURL)
        else:
            print("we encountered another list while parsing the html of this list, but the title doesnt have 'new zealand' in it, so we ignore it: " + wikipediaArticleURL)
    else:
        print("leaf article found. Passing it on to determine nzness: " + wikipediaArticleURL)
        determineNZArticleOrNot(wikipediaArticleURL)





#checks for the string "new zealand" or some differently cased
#variant within the body of this article. If it is present, this article is
#added to the master list of articles. Else, do nothing.
def determineNZArticleOrNot(wikipediaArticleURL):

    articleToExamineResponse = requests.get(wikipediaArticleURL)
    articleSoup = BeautifulSoup(articleToExamineResponse.text, 'html.parser')

    if "new zealand" in articleSoup.get_text().lower():
        print("found an nz related leaf article: " + articleSoup.title.text)
        articleSoupText = articleSoup.get_text()
        #NOTE: this is a gross bit of regular expression black magic that finds the unique
        #ID of the page which is a javascript var (i think...).
        regexIDMatch = regex.search("wgArticleId\":...........", articleSoupText)
        if regexIDMatch:
            matchFound = regexIDMatch.group(0)
            foundID = regex.sub("[^0-9]", "", matchFound)
            nzRelatedArticlesIDs.append(foundID)





if __name__ == '__main__':
    main()
