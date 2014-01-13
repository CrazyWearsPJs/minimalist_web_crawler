import urllib2
#import urlparse, httplib, socket
import lxml.html as lh

"""
def valid_url(url):
	full_url = urlparse.urlsplit(url)
	sever, path = full_url[1], full_url[2]
	connection = httplib.HTTPConnection(sever, 80)
	try:
		connection.connect()
	except socket.gaierror:
		return False
	except socket.error:
		return False

	connection.putrequest('HEAD', path)
	connection.putheader('Accept', '*/*')
	connection.endheaders()

	response = connection.getresponse()
	connection.close()
	return response.status == 200
"""

class Page:
	def __init__(self, url = ""):
		self.url     = url
		self.content = self.__get_page(url)
		self.links   = self.__get_all_links(self.content)

	def is_valid(self):
		return self.url and self.content and self.links != None

	def __get_page(self, url):
		try:
			response = urllib2.urlopen(url)
			return response.read()
		except:
			# raise Exception("{} returned error: {}".format(url, e))
			return None

	def __get_all_links(self, page_content):
		if not page_content:
			return None
		document_tree = lh.fromstring(page_content)
		links = set(document_tree.xpath('//a/@href'))
		#links = filter(lambda x: valid_url(x), links)
		return links

