from crawl import crawl_web, page_rank
from search import ordered_search, lucky_search

"""
usage: test.py seed_url
"""

def test(seed):
	print 'Crawling web . . .'
	index, graph = crawl_web(seed)
	print 'Calculating Page Rank . . .'
	ranks = page_rank(graph)
	print ranks
	print ordered_search(index, ranks, 'dogs')
	print lucky_search(index, ranks, 'cats')

if __name__ == '__main__':
	import sys
	if len(sys.argv) >= 2:
		test(sys.argv[1])