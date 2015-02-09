import mechanize

br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


api_key, format = "11f898808fffe257228d17890b1101f1", "json"

api_key = "11f898808fffe257228d17890b1101f1"
format = "json"

def retrieve_data(word, pos):
	#url = "http://words.bighugelabs.com/api/2/" + api_key + "/" + word + "/" + format
	url = "http://words.bighugelabs.com/api/2/" + "11f898808fffe257228d17890b1101f1" + "/" + word + "/json"
	html = br.open(url).read()

	Synonyms, Antonyms, Relateds, Similars = [], [], [], []
	categories = ["syn", "ant", "rel", "sim"]

	while '"' in html:
		html = html[:html.index('"')] + html[html.index('"')+len('"'):]
	pos = pos + ':{'
	i = html.index(pos)
	segment = html[i+len(pos):html.find("}", i)]

	for category in categories:
		title = category + ':['
		if title in segment:
			j = segment.index(title)
			subsegment = segment[j+5:segment.find("]", j)]
			if category == "syn":
				Synonyms = subsegment.split(",")
			elif category == "ant":
				Antonyms = subsegment.split(",")
			elif category == "rel":
				Relateds = subsegment.split(",")
			elif category == "sim":
				Similars = subsegment.split(",")

	return Synonyms, Antonyms, Relateds, Similars
