"""
APIs that use APIs and so forth
"""

import local_settings as settings
import bottlenose
from xml.dom import minidom as xml
from itertools import count


class Search():
	"""
	Integration with Amazon API to show search results and so forth

	TO DO: 
		- better parsing for output as dictionary or std out
		- error container to report back any issues

	POSSIBLE TO DO:

	"""

	def __init__(self,title="",author="",keywords="",style="json",output="detailed"):

		# setup the search terms from args
		self.title = title
		self.author = author
		self.keywords = keywords
		self.rawstyle = style
		self.rawoutput = output

		# setup the result data type ---> defaults to json using the xml2json stylesheet
		styles = {
				"xml" : "XML",
				"json" : "xml2json.xslt" # we should host this ourselves then - must be a URL
			}
		
		self.style = styles[self.rawstyle]

		# we will fire up a parsing procedure if we have XML style
		if self.style == "XML":
			self.parse = True
		else:
			self.parse = False
	
		# search result type ---> defaults to ItemAttributes (most detailed)
		outputTypes = {
				"images" : "Images",
				"detailed" : "ItemAttributes"
			}
		
		self.outputMethod = outputTypes[self.rawoutput]

		# setup the API access - these are temporarily filled in with my affilate id
		keys = {
				'access_key' : settings.amazon["access_key"],
				'secret_key' : settings.amazon["secret_key"],
				'affiliate_id' : settings.amazon["affiliate_id"]
			}

		self.amazon = bottlenose.Amazon(keys['access_key'],keys['secret_key'],keys['affiliate_id'])
	
		# run the search to populate self.results with an xml string
		self.search()


	def search(self):
		"Do the search"
		
		self.results = self.amazon.ItemSearch(
				SearchIndex = "Books",
				Style = self.style,
				ResponseGroup = self.outputMethod,
				Sort = "relevancerank",
				Title = self.title,
				Author = self.author,
				Keywords = self.keywords
			)

		# if we set Parse=True when instantiating, we will print out a nice parsed version as well
		if self.parse:
			self.parser()

		else:
#			import simplejson as json

#			self.results = json.loads(self.results)
			
			return self.results


	def parser(self):
		"Parse XML results"


		# pipe the results into our xml dom
		r = xml.parseString(self.results)

		self.parsedXML = {}
	
		# setup some attributes that we want to grab and print out
		attrs = ['Title','Author','FormattedPrice','URL']

		# iterate through by Item and if we can find the attribute we print it out
		x = count(0)

		for i in r.getElementsByTagName('Item'):

			item = next(x) 
			self.parsedXML[item] = {}
			parseItem = self.parsedXML[item]

			for attr in attrs:
				parseItem[attr] = ""
				try:
					parseItem[attr] = i.getElementsByTagName(attr)[0].childNodes[0].data
				except:
					pass


		return self.parsedXML
