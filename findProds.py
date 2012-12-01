# Python script to parse AliBaba pages and compare to
# Amazon prices, results in order to reveal unique and
# novel arbitrage opportunities systematically.
# Outputs a CSV of manually approved AliBaba items
# deemed capable for arbitrage by a human operator.
#
# @author Philip Daian
# @email  phil@linux.com
# 
# Licensed under GPLv3

# Import all required modules
from amazon import Search
from BeautifulSoup import BeautifulSoup
import re, urllib

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
    items = []
    allProducts = soup.findAll("div", { "class" : "attr" })
    allSellers  = soup.findAll("div", { "class" : "supplier" })
    allPics  = soup.findAll("div", { "class" : "pic" })
    for i in range(0, len(allProducts)):
        productsParse = allProducts[i]
        sellersParse  = allSellers[i]
        picsParse      = allPics[i]
        productsParse = [str(x) for x in productsParse]
        sellersParse  = [str(x) for x in sellersParse]
        picsParse  = [str(x) for x in picsParse]
        # Append a map of item attributes for allProducts[i]
        items.append(aliBabaItemParse(' '.join(productsParse), ' '.join(sellersParse), ' '.join(picParse)))
    return items

# Extract the item and supplier information
# for all items in the sub-pages product, sellerParse
# and return relevant info as a dictionary
def aliBabaItemParse(productsParse, sellersParse, picParse):
    attrs = {}
    productsSoup = BeautifulSoup(productsParse)
    sellersSoup  = BeautifulSoup(sellersParse)
    allProducts = productsSoup.findAll("p")
    allSellers = sellersSoup.findAll("p")
    for i in range(0, len(allProducts)):
        if len(allProducts[i].contents) < 1:
            continue 
        for tagoffset in range(0, len(allProducts[i].contents)):
            if ('attrName' in str(allProducts[i].contents[tagoffset])):
                break
        if tagoffset == (len(allProducts[i].contents) - 1):
            continue
        attrName = ' '.join(str(allProducts[i].contents[tagoffset].string).split()).split(":")[0]
        attrValue = ' '.join(str(allProducts[i].contents[tagoffset+1]).split())
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
        break # @todo remove me after testing
        soup = BeautifulSoup(urllib.urlopen(base_url + "_" + str(i)).read())
        aliBabaPageParse(soup)

# Program entry-point
main()