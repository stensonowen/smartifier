import mechanize, re

br = mechanize.Browser()

br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)	#ducking it up?
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

html = br.open("http://icanhazip.com").read()


#_href="/dictionary/[\w]+">[\w]+</a>_ finds only links
#_>[\w]+</a>_


word = "smart"
pos = "adjective"
url = "http://www.merriam-webster.com/thesaurus/" + word + "[" + pos + "]"

Synonyms = []
RelatedWords = []
Antonyms = []
NearAntonyms = []

html = br.open(url).read()

html = html[html.index("<span>Definition of"):html.index("</span></div></div><br")]

while "<strong>" in html:
	relation = re.search("<strong>[\w ]+</strong>", html).group(0)
	segment = html[html.index(relation):html.index("></div>")+7]
	words = re.findall(">[\w ]+</a>", segment)
	
	if relation[8:-9] == "Synonyms":
		for word in words:
			word = word[1:-4]
			if word not in Synonyms:
				Synonyms.append(word)
	elif relation[8:-9] == "Related Words":
		for word in words:
			word = word[1:-4]
			if word not in RelatedWords:
				RelatedWords.append(word)
	elif relation[8:-9] == "Antonyms":
		for word in words:
			word = word[1:-4]
			if word not in Antonyms:
				Antonyms.append(word)
	elif relation[8:-9] == "Near Antonyms":
		for word in words:
			word = word[1:-4]
			if word not in NearAntonyms:
				NearAntonyms.append(word)
	else:
		print "\nERROR: Unknown Category\n"

	html = html[html.index("></div>")+7:]