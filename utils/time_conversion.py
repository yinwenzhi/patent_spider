def secondstohour(seconds):
	m, s = divmod(int(seconds), 60)
	h, m = divmod(m, 60)
	return "{:02}时:{:02}分:{:02}秒".format(h, m, s)

def countlasttime(seconds, spider_all, spider_hassuccessed, page_all):
	return secondstohour(seconds / spider_all * (page_all - spider_all - spider_hassuccessed))