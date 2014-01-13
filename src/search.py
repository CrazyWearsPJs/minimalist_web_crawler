def lucky_search(index, ranks, keyword):
	urls = index.get(keyword)
	if urls and ranks:
		return max(urls, key = lambda x: ranks[x])
	else:
		return None

def ordered_search(index, ranks, keyword):
	urls = index.get(keyword)
	if urls and ranks:
		return sorted(urls, key = lambda x: ranks[x])
	else:
		return None
