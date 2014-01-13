from page import Page

def crawl_web(seed, max_depth = 10, max_pages = 1000):
	to_crawl, crawled = {seed}, set()
	index, graph = {}, {}

	def crawl(url, depth):
		if hasattr(crawl, 'pages'):
			crawl.pages += 1
		else:
			crawl.pages = 1

		if crawl.pages >= max_pages or depth >= max_depth or url in crawled or not url:
			crawl.pages -= 1
			return

		crawled.add(url)
		page = Page(url)
		if not page.is_valid():
			return
		index_page(index, page)
		graph[url] = page.links
		outgoing_links = page.links
		while outgoing_links or to_crawl:
			if outgoing_links:
				next_url = outgoing_links.pop()
				next_depth = depth + 1
			else:
				next_url = to_crawl.pop()
				next_depth = depth

			to_crawl.update(outgoing_links)
			crawl(next_url, next_depth)

	crawl(seed, 0)
	return (index, graph)

def index_page(index, page):
	words = page.content.split()
	for word in words:
		if word in index:
			index[word].add(page.url)
		else:
			index[word] = {page.url}

# Page Rank Algorithm where d is the damping constant
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
