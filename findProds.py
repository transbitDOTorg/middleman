# Python script to parse AliBaba pages and compare to
# Amazon prices, results in order to reveal unique and
# novel arbitrage opportunities systematically.
# Outputs a CSV of manually approved AliBaba items
# deemed capable for arbitrage by a human operator.
#
# @author   Transbit
# @email    info@transbit.org
# @version  0.1
# @reqs     Python v2.7
#
# Licensed under GPLv3

# Import all required modules
from BeautifulSoup import BeautifulSoup
import re, urllib, math, gui

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

class ParserMain:
    # Extract the item and supplier information
    # for all items in the page contained in soup
    def aliBabaPageParse(self, soup):
        if (self.currPage >= self.numPages):
            # Too many pages processed
            return None;
        soup = BeautifulSoup(urllib.urlopen(self.base_url + "_" + str(self.currPage)).read())
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
            items.append(self.aliBabaItemParse(' '.join(productsParse), ' '.join(sellersParse), ' '.join(picsParse)))

        return items

    # Extract the item and supplier information
    # for all items in the sub-pages product, sellerParse
    # and return relevant info as a dictionary
    # @todo: Clean up some of the product parsing
    def aliBabaItemParse(self, productsParse, sellersParse, picsParse):
        productsSoup    = BeautifulSoup(productsParse)
        sellersSoup     = BeautifulSoup(sellersParse)
        picsSoup        = BeautifulSoup(picsParse)

        # Parse productsSoup, sellersSoup, extract relevant item attributes
        attrs           = dict(self.parseAttrs(productsSoup).items() + self.parseAttrs(sellersSoup).items())

        # Parse picsSoup, extract relevant item attributes
        picTag          = picsSoup.find("img")
        attrs["name"]   = str(picTag["alt"])
        attrs["image"]  = str(picTag["image-src"])
    
        attrs = dict(attrs.items() + self.parseIcons(sellersSoup).items())
        return attrs
    
    # Parse soup, extract relevant item attributes from icon span
    # as AliBaba stores them (in a way that makes me a sad panda)
    def parseIcons(self, soup):
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
    def parseAttrs(self, soup):
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

    # Serve items one at a time as dictionary
    def serveNextItem(self):
        if (len(self.cachedItems) == 0):
            self.currPage+=1
            soup = BeautifulSoup(urllib.urlopen(self.base_url + "_" + str(self.currPage)).read())
            self.cachedItems = self.aliBabaPageParse(soup)
        return self.cachedItems.pop(0)

    # Main function, execution entry-point
    def main(self):
        self.numPages = 0
        self.currPage = 1
        self.cachedItems = []
        # Accept URL input for category from user
        self.base_url       = raw_input("Enter a category URL on Alibaba (from http://alibaba.com/): ").strip()
        self.require_price  = True
        self.render_colors  = True
        self.bcolors        = bcolors()
        if not self.render_colors:
            self.bcolors.disable()
        
        while True:
            user_price_threshold = raw_input("Hide items above price [$200]: ")
            try:
                if len(user_price_threshold) == 0:
                    self.price_threshold = 200
                else:
                    self.price_threshold = int(user_price_threshold)
                break
            except:
                print self.bcolors.FAIL + "Error: Invalid integer parameter." + self.bcolors.ENDC

        # Load URL if valid, otherwise throw an error and quit the program
        try:
            pageToParse = urllib.urlopen(self.base_url).read()
            print "Base URL "+self.bcolors.OKGREEN + "OK." + self.bcolors.ENDC
        except:
            print "Base URL "+self.bcolors.FAIL + "ERROR." + self.bcolors.ENDC
            exit(0)
        
        soup = BeautifulSoup(pageToParse)

        # Extract the number of pages in the search using BeautifulSoup
        # (necessary to iterate over all pages and extract all items)
        self.numPages = soup.find('span', attrs={"class":"page-num"})
        self.numPages = int(self.numPages.contents[0].split("of")[1].split(":")[0].strip())
        self.gui = gui.mainApp(self)
        self.gui.display()

# Program entry-point
mainParser = ParserMain()
mainParser.main()
