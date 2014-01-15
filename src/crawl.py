from page import Page
from collections import namedtuple
import heapq
import itertools

"""
A tuple which contains
priority: the priority of the set of links in the pq (not unique)
id: the unique id of the set of links, used for tiebreakers
links: set of links
"""

Links = namedtuple('Links', ['priority', 'id', 'links'])
def crawl_web(seed, max_depth = 10, max_pages = 1000):
	crawled = set()
	crawl_queue =  [] # priority queue ensures that more "shallow" links are handled first
	index = {}
	graph = {}
	counter = itertools.count()

	"""
	Add set of links to queue of sets, crawled_queue.
	Makes sure links is not in the set of already crawled urls.
	"""
	def add_links(links, depth = 0):
		count = next(counter)
		new_links = links.difference(crawled)
		entry = Links(priority = depth, id = count, links = new_links)
		heapq.heappush(crawl_queue, entry)

	"""
	Adds all of the words in page.content to the index of words
	to sets of urls
	"""
	def index_page(page):
		words = page.content.split()
		for word in words:
			if word in index:
				index[word.lower()].add(page.url)
			else:
				index[word.lower()] = {page.url}

	add_links({seed}, 0)
	pages = 0
	while crawl_queue:
		entry = heapq.heappop(crawl_queue)
		to_crawl = entry.links
		depth = entry.priority
		while to_crawl and pages < max_pages:
			url = to_crawl.pop()
			page = Page(url)
			if page.is_valid() and not url in crawled:
				print url, depth
				pages += 1
				crawled.add(url)
				index_page(page)
				graph[url] = page.outgoing_links
				if depth < max_depth:
					add_links(page.outgoing_links, depth + 1)
	return index, graph

"""
Page Rank Algorithm where d is the damping constant, and the
calculates p_k_rank for each p in graph, where k is max_iterations
"""
def page_rank(graph, d = 0.8, max_iterations = 10):
	graph_size = len(graph)
	ranks = {}

	if graph_size < 1:
		return ranks

	inital_rank = 1.0 / graph_size
	for url in graph:
		ranks[url] = inital_rank

	inital_val = (1.0 - d) / graph_size
	new_ranks = {}
	for i in xrange(max_iterations):
		for page in graph:
			next_rank = inital_val
			# for all nodes page is incident to
			for node in graph:
				if page in graph[node]:
					next_rank += d * (ranks[node] / len(graph[node]))
			new_ranks[page] = next_rank
		ranks = new_ranks
	return ranks