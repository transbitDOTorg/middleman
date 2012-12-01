# Python script to parse AliBaba pages and compare to
# Amazon prices, results in order to reveal unique and
# novel arbitrage opportunities systematically.
# Outputs a CSV of manually approved AliBaba items
# deemed capable for arbitrage by a human operator.
#
# @author   Philip Daian
# @email    phil@linux.com
# @version  0.1
# @reqs     Python v2.7
#
# Licensed under GPLv3

# Import all required modules
from amazon import Search
from BeautifulSoup import BeautifulSoup
import re, urllib, math

# Constant storage class that allows for
# colored terminal output via ANSI codes
class bcolors:
    HEADER  =   '\033[95m'
    OKBLUE  =   '\033[94m'
    OKGREEN =   '\033[92m'
    WARNING =   '\033[93m'
    FAIL    =   '\033[91m'
    ENDC    =   '\033[0m'

    def disable(self):
        self.HEADER     = ''
        self.OKBLUE     = ''
        self.OKGREEN    = ''
        self.WARNING    = ''
        self.FAIL       = ''
        self.ENDC       = ''

# Extract the item and supplier information
# for all items in the page contained in soup
def aliBabaPageParse(soup):
    items       = []
    allProducts = soup.findAll("div", { "class" : "attr" })
    allSellers  = soup.findAll("div", { "class" : "supplier" })
    allPics     = soup.findAll("div", { "class" : "pic" })

    for i in range(0, len(allProducts)):
        productsParse = allProducts[i]
        sellersParse  = allSellers[i]
        picsParse     = allPics[i]
        productsParse = [str(x) for x in productsParse]
        sellersParse  = [str(x) for x in sellersParse]
        picsParse     = [str(x) for x in picsParse]
        # Append a map of item attributes for allProducts[i]
        items.append(aliBabaItemParse(' '.join(productsParse), ' '.join(sellersParse), ' '.join(picsParse)))

    return items

# Extract the item and supplier information
# for all items in the sub-pages product, sellerParse
# and return relevant info as a dictionary
# @todo: Clean up some of the product parsing
def aliBabaItemParse(productsParse, sellersParse, picsParse):
    productsSoup    = BeautifulSoup(productsParse)
    sellersSoup     = BeautifulSoup(sellersParse)
    picsSoup        = BeautifulSoup(picsParse)

    # Parse productsSoup, sellersSoup, extract relevant item attributes
    attrs           = dict(parseAttrs(productsSoup).items() + parseAttrs(sellersSoup).items())

    # Parse picsSoup, extract relevant item attributes
    picTag          = picsSoup.find("img")
    attrs["name"]   = str(picTag["alt"])
    attrs["image"]  = str(picTag["image-src"])
    
    attrs = dict(attrs.items() + parseIcons(sellersSoup).items())
    print attrs
    return attrs
    
# Parse soup, extract relevant item attributes from icon span
# as AliBaba stores them (in a way that makes me a sad panda)
def parseIcons(soup):
    attrs = {}
    goldTag = soup.findAll("a", href="javascript:openGsIcon();")
    attrs["isGold"] = len(goldTag) > 0
    goldYears = goldTag[0]["title"].split()[2]
    goldYearsNum = 0
    for i in range(0, len(goldYears)):
        try:
            goldYearsNum += int(goldYears[i]) * int(math.pow(10, i))
        except:
            break
    attrs["goldYears"]      = goldYearsNum
    attrs["isEscrow"]       = len(soup.findAll("a", attrs={"class":"escrowlogo icon-item"})) > 0
    attrs["isOnsiteCheck"]  = len(soup.findAll("a", attrs={"class":"onsitelogo icon-item"})) > 0
    attrs["isAssessed"]     = len(soup.findAll("a", attrs={"class":"cslogo icon-item"})) > 0
    return attrs

# Parse soup, extract relevant item attributes as AliBaba stores them
# @todo Clean this up
def parseAttrs(soup):
    attrs = {}
    allItems = soup.findAll("p")
    for i in range(0, len(allItems)):
        if len(allItems[i].contents) < 1:
            continue 
        for tagoffset in range(0, len(allItems[i].contents)):
            if ('attrName' in str(allItems[i].contents[tagoffset])):
                break
        if tagoffset == (len(allItems[i].contents) - 1):
            continue
        attrName = ' '.join(str(allItems[i].contents[tagoffset].string).split()).split(":")[0]
        attrValue = ' '.join(str(allItems[i].contents[tagoffset+1]).split())
        attrs[attrName.strip()] = attrValue.strip()
    return attrs
    
# Extract item and price information for first 
# ten Amazon search results, return relevant
# info as an array of dictionaries
def amazonSearch(itemName):
    result = Search(title="The Idea of America",author="Gordon Wood",style="xml")
    link = result.parsedXML[0]
    for i in range(0, min(len(result.parsedXML), 10)):
        pass
    print link

# Main function, execution entry-point
def main():
    # Accept URL input for category from user
    base_url        = raw_input("Enter a category URL on Alibaba (from http://alibaba.com/): ").strip()
    use_browser     = "b" in raw_input("Select display mode  [P(anel) / b(rowser)]: ").lower();
    require_price   = not "n" in raw_input("Require FOB price to display item? [Y / n]: ").lower();
    
    # Load URL if valid, otherwise throw an error and quit the program
    try:
        pageToParse = urllib.urlopen(base_url).read()
        print "Base URL "+bcolors.OKGREEN+ "OK."+bcolors.ENDC
    except:
        print "Base URL "+bcolors.FAIL+ "ERROR."+bcolors.ENDC
        exit(0)
        
    soup = BeautifulSoup(pageToParse)
    aliBabaPageParse(soup)

    # Extract the number of pages in the search using BeautifulSoup
    # (necessary to iterate over all pages and extract all items)
    numPages = soup.find('span', attrs={"class":"page-num TreFont"})
    numPages = int(numPages.contents[0].split("/")[1])

    for i in range(2, numPages+1):
        #break # @todo remove me after testing
        soup = BeautifulSoup(urllib.urlopen(base_url + "_" + str(i)).read())
        aliBabaPageParse(soup)

# Program entry-point
main()
