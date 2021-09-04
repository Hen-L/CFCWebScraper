# main code file for web scraper

#imports
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import re


# Function to scrape webpage
def scrape_web_page(url):
    print("Scraping Webpage...")
    page = requests.get(url) #requesting the index page from url

    return(page) #returning the page


# Function to list externally located images
def list_external_images(scrapedpage):
    print("Listing External Images...") #outputting prompt
    externalimages = [] #creating list for the external images
    # searching for div files with class as img (how the external image are loaded)
    for divimgitem in scrapedpage.find_all('div', 'img'):
        print(divimgitem) #printing the imgs
        externalimages.append(str(divimgitem['style'])) #appending the image

    #uncomment below section to find external svg xml resources
    '''
    #finding svg external graphics
    for item in scrapedpage.find_all('svg'):
        print(item) #print the svg
        externalimages.append(str(item)) #appending the svg image
    '''

    return externalimages #returning the external images


# Function to list externally located scripts
def list_external_scripts(scrapedpage):
    print("Listing External scripts...") #outputting prompt
    externalscripts = [] #create list for external scripts
    #looking for script tags with a src
    for scriptitem in scrapedpage.find_all('script', {'src': True}):
        #if the src starts with "/" then it is hosted on the site, looking for everything else (external)
        if (scriptitem['src'][0] != "/"):
            print(scriptitem) #printing the script
            externalscripts.append(str(scriptitem['src'])) #append to the external scripts list

    return externalscripts #return the external scripts


# Function to list externally located fonts
def list_external_fonts(scrapedpage, url):
    print("Listing External fonts and css files...") #outputting prompt
    externalfonts = [] #making list of external fonts

    for fontsitem in scrapedpage.find_all("link"): #find all links (where fonts are found)
        if fontsitem.attrs.get("href"): #if there is href attribute
            fonturl = urljoin(url, fontsitem.attrs.get("href")) #joining the non fully completed urls
            if fonturl[0:31] != "https://www.cfcunderwriting.com": #if hosted on the site
                externalfonts.append(str(fonturl)) #append the css/font url
                print(fonturl) #printing the font/css url

    return externalfonts #return the extenral fonts


# Function to dump images, scripts and fonts to json
def dump_images_scripts_fonts_tojson(images, scripts, fonts):
    print("Dumping images, scripts and fonts to JSON...") #outputting prompt

    with open("externalresources.json", 'r+') as file: #opening a json file
        jsondata = json.load(file) #loading the json file data
        jsondata["images"] = images #adding the images list to the json data
        jsondata["scripts"] = scripts #adding the scripts list to the json data
        jsondata["fonts"] = fonts #adding the fonts list to the json data
        file.seek(0) #referencing the beginning of the file
        json.dump(jsondata, file, indent=4) #duming the json data into the file

    print(jsondata) #printing the json to console




# Function to enumerate hyperlinks (linear search)
def enumerate_hyperlinks_find_privacypolicy(scrapedpage, url):
    print("enumerating hyperlinks...") #outputting prompt
    privacypolicyurl = ""
    for anchoritem in scrapedpage.find_all('a'): #finding all anchors/hyperlinks
        wholeurl= urljoin(url, anchoritem.attrs.get("href")) #joinig the urls hosted on site
        print(wholeurl)#printing the urls
        if anchoritem.string == "Privacy policy": #if the item is the Privacy policy in the text
            privacypolicyurl = wholeurl #store it into a variable

    print('Privacy policy url:') #outputting prompt

    #print and return the privacy policy url
    print(privacypolicyurl)
    return privacypolicyurl






# Function to count the words and their frequencies. Then dump to json.
def count_words(scrapedpage):
    print("Counting words...") #outputting prompt
    wordsdict = {} #initializing a word dictionary
    allwords = "" #initalizing a string for all the words

    for worditem in scrapedpage: #loopthrough all the words
        allwords += worditem #add it to the string

    #replacing new lines with spaces and removing excess whitespace
    allwordsformatted = " ".join(item for item in allwords.split('\n') if item).strip()
    #using a regex expression to match to only upper and lowercase words and then set them all to lower case
    allwordsformatted = re.sub('[^a-zA-Z ]+', '', allwordsformatted).lower()
    #print(allwordsformatted) #uncomment to print all wordsafter they have been formatted
    for word in allwordsformatted.split(): #loop through all the words in the string
        #print(word) #uncomment to print all words seperatley
        if word not in wordsdict: #if the word isnt in the words dictionary
            wordsdict.update({word: 1}) #add it and put count to 1
        else: #if it is in the word dictionary
            currentwordcount = wordsdict[word] + 1 #increment the word count
            wordsdict.update({word: currentwordcount}) #add it back to dictionary

    print(wordsdict) #printing the word dictionary

    #opening the wordcount json
    with open('wordcount.json', 'w') as fp:
        json.dump(wordsdict, fp, indent=4) #dumping the words into the json file



#main decleration
if __name__ == '__main__':
    # calling function to scrape index page of cfcunderwriting.com
    scrapedpage = scrape_web_page("https://www.cfcunderwriting.com")
    print(scrapedpage) #print scraped page code

    parsedhtmlindex = BeautifulSoup(scrapedpage.text, 'html.parser')  # passing the html from the webpage
    print(parsedhtmlindex) #printing the scraped index html

    externalimages = list_external_images(parsedhtmlindex) # calling function to list external images
    externalscripts = list_external_scripts(parsedhtmlindex) #calling function to list external scripts
    #calling function to list extenral fonts/css
    externalfonts = list_external_fonts(parsedhtmlindex, "https://www.cfcunderwriting.com")

    #calling function to dump the images, scripts and fonts to json file
    dump_images_scripts_fonts_tojson(externalimages, externalscripts, externalfonts)

    privacypolicyurl = enumerate_hyperlinks_find_privacypolicy(parsedhtmlindex, "https://www.cfcunderwriting.com") #calling function to enumerate links in index
    #calling function to scrape privacy page
    privacypolicyscraped = scrape_web_page(privacypolicyurl)
    print(privacypolicyscraped.text) #printing scraped privacy policy html

    # parsing the html and getting the plain text
    parsedhtmlprivacy = BeautifulSoup(privacypolicyscraped.content, 'html.parser').text.strip()
    count_words(parsedhtmlprivacy) #calling function to count the words on privacy page
