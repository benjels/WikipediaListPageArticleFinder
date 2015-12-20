__author__ = 'user'

from bs4 import BeautifulSoup
import requests
import regex
import yaml
from pprint import pprint



def main2():
    print("easfs")
    harvester = Harvester(3, "rules.yml")
    print(harvester.get("New_Zealand"))

#an instance of the Harvester class can be used to find a lot of interesting URLs given an appropriate yml file
class Harvester(object):

    def __init__(self, maxDepth, ruleset, verbose = False):
        self.maxDepth = maxDepth #FIELD# the maximum depth of this Harvester's recursion
        self.WIKIPEDIA_URL_ROOT_STRING = "https://en.wikipedia.org/wiki/" #FIELD# the root of all article URLS
        self.visitedURLs = set() #FIELD# set of URLs that have been visited by the Harvester
        self.FoundArticlesTitles = set() #FIELD# set of article titles found by the Harvester
        self.verbose = verbose #FIELD# gives more printouts when true
        with open(ruleset, "r") as fileStream:
           # self.ruleset = yaml.load(fileStream)#FIELD# the "rules" that the Harvester uses to determine what its seed/start locations are and which articles it should look for/ignore etc
           print("this not ready yet")

    #just a helper method for getting the text content from a wikipedia page name (e.g. "List_of_towns_in_New_Zealand")
    #Returns the text content of the page queried UNLESS there is an error, then returns None.
    def getPage(self, pageName):#TODO: maybe this method should return soup
        url = self.WIKIPEDIA_URL_ROOT_STRING + pageName
        if self.verbose:
            print("getting : " + url)
        response = requests.get(url)#TODO: probably also catch all exceptions raised by making the request and just log the URLs that cause them
        if response.status_code != 200:
            print("error making request. status code: " + response.status_code)
            return None
        return response.text

    #takes the text/content of a wikipedia article page and uses the rules in the rules.yml file
    #to determine whether the article should be saved.
    #Returns True if the article is relevant to what we are looking for (defined in rules.yml)
    #Returns False if the article is not relevant to what we are looking for OR if there is an error
    def determineArticleRelevance(self, textContent):
        print("using rules.yml to determine this shit senpai")
        #check that there's nothing in article black list present here

        #check if there's something in article seek list here


    #gets the page with the article page name provided. If that page is a list, recursively call this
    #method to find even more articles. If that page is a "leaf" article, then find out whether it is an
    #article that we are interested in.
    #Returns a set of page name strings that belong to relevant articles that were either the article whose
    #name was initially provided to this method, or some "descendant" articles that are reachable from this article
    #via recursive calls (if this method was provided with a list article).
    def findArticles(self, pageName, depth, textualDescOfBranch):
        #check that we haven't gone too deep

        #mark this URL as visited so that we don't come back

        #if we are at a relevant list, scrape the links in here and return the result of the recursive calls

        #if we are at a leaf, then check whether we want to return this as relevant or not


        #if the article that we are at is neither a desired list, nor a desired leaf, return the empty set








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
    progressLogFile.write("finished search that started with : " + "https://en.wikipedia.org/wiki/List_of_towns_in_New_Zealand \nhttps://en.wikipedia.org/wiki/Lists_of_New_Zealanders \n")
    progressLogFile.close()


    examineArticle("https://en.wikipedia.org/wiki/Category:Lists_of_places_in_New_Zealand", 0)
    progressLogFile = open("C:\!2015SCHOLARSHIPSTUFF\wikipediaNZRelatedScrapeResults\serachingProgress.txt", "w")
    progressLogFile.write("finished search that started with : " + "https://en.wikipedia.org/wiki/List_of_towns_in_New_Zealand \nhttps://en.wikipedia.org/wiki/Lists_of_New_Zealanders \nhttps://en.wikipedia.org/wiki/Category:Lists_of_places_in_New_Zealand \n")
    progressLogFile.close()


    #we have gathered all of the article IDs, so let's write them to a file that our java program will use
    fileToSaveIDs = open("C:\!2015SCHOLARSHIPSTUFF\wikipediaNZRelatedScrapeResults\onlyLookingAtFirstPara.txt", "w")
    for each in range(0, len(nzRelatedArticlesIDs)):
        try:
            fileToSaveIDs.write(nzRelatedArticlesIDs[each] + "," + nzRelatedArticlesTitle[each] + "\n")
        except UnicodeEncodeError:
            print("error encoding: " + nzRelatedArticlesTitle[each])
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

    try:
        articleToExamineResponse = requests.get(wikipediaArticleURL)
        articleSoup = BeautifulSoup(articleToExamineResponse.text, 'html.parser')
        firstParagraph = str(articleSoup.find('p')).lower()
    except:
        print("exception trying to get the article: " + wikipediaArticleURL + " so we will stop this branch")
        return None

    if "new zealand" in firstParagraph:
        print("found an nz related leaf article: " + articleSoup.title.text)
        articleSoupText = articleSoup.get_text()
        #NOTE: this is a gross bit of regular expression black magic that finds the unique
        #ID of the page which is a javascript var (i think...).
        regexIDMatch = regex.search("wgArticleId\":...........", articleSoupText)
        if regexIDMatch:
            matchFound = regexIDMatch.group(0)
            foundID = regex.sub("[^0-9]", "", matchFound)
            nzRelatedArticlesIDs.append(foundID)
            nzRelatedArticlesTitle.append(articleSoup.title.text.lower())
            assert len(nzRelatedArticlesIDs) == len(nzRelatedArticlesTitle), "those should always be the same size"





if __name__ == '__main__':
    main2()
