#Classify Stanford data, organize into relevant data in preparation to specify search query

import mechanize, re, os
from nltk.tag.stanford import POSTagger
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from pattern.en import comparative, superlative, pluralize, conjugate

os.environ['JAVAHOME'] = "G:\\Programs\\Java\\jdk1.8.0_05\\bin\\java.exe"
tagger = POSTagger("G:\\Scripts\\Python\\WordsWordsWords\\stanford-postagger-2014-06-16\\models\\english-bidirectional-distsim.tagger", "G:\\Scripts\\Python\\WordsWordsWords\\stanford-postagger-2014-06-16\\stanford-postagger.jar")

br = mechanize.Browser()
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


def replace_string(oldstring, newstring, text):
	while oldstring in text:
		text = text[:text.index(oldstring)] + newstring + text[text.index(oldstring)+len(oldstring):]
	return text

def retrieve_data(word, pos):
	try:
		url = "http://words.bighugelabs.com/api/2/" + "11f898808fffe257228d17890b1101f1" + "/" + word + "/json"
		html = br.open(url).read()

		Synonyms, Antonyms, Relateds, Similars = [], [], [], []
		categories = ["syn", "ant", "rel", "sim"]

		html = replace_string('"', "", html)
		#while '"' in html:
		#	html = html[:html.index('"')] + html[html.index('"')+len('"'):]
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
	except:
		print "\nERROR: Failed to find synonyms\n"
		return [word], [], [], []
	else:
		return Synonyms, Antonyms, Relateds, Similars

def tag(sentence):
	tokens = word_tokenize(sentence)
	return tagger.tag(tokens)

#only execute if synonyms are found?
#include original? for plagiarism NO, for smartifier YES?
def optimizer(synset): #add in antonyms, related terms, and similar terms?
	leader, score = "", 0
	for syn in synset:
		parts = re.split("-| ", syn)
		parts = sorted(parts, key=len)
		if len(parts[-1]) > score:
			leader = syn
			score = len(parts[-1])
	return leader


def convert_adjective(adjective, tag):
	if len(wn.morphy(adjective, wn.ADJ)) > 0:
		base = wn.morphy(adjective, wn.ADJ)
		#raises error if nonsense word
	Synonyms = retrieve_data(base, "adjective")[0]
	synonym = optimizer(Synonyms)
	if tag == "JJ":
		return synonym
	elif tag == "JJR":
		return comparative(synonym)
	elif tag == "JJS":
		return superlative(synonym)
	else:
		print "\nERROR: Form Not Found!\n"
		return adjective

def convert_adverb(adverb, tag):
	if len(wn.morphy(adverb, wn.ADV)) > 0:
		base = wn.morphy(adverb, wn.ADV)
	Synonyms = retrieve_data(base, "adverb")[0]
	synonym = optimizer(Synonyms)
	if tag == "RB":
		return synonym
	elif tag == "RBR":
		return comparative(synonym)
	elif tag == "RBS":
		return superlative(synonym)
	else:
		print "\nERROR: Form Not Found!\n"
		return adverb

def convert_noun(noun, tag):
	if len(wn.morphy(noun, wn.NOUN)) > 0:
		base = wn.morphy(noun, wn.NOUN)
	Synonyms = retrieve_data(base, "noun")[0]
	synonym = optimizer(Synonyms)
	if tag == "NN":
		return synonym
	elif tag == "NNS":
		return pluralize(synonym)
	else:
		print "\nERROR: Form Not Found!\n"
		return noun

whitelist = ["be", "am", "is", "are", "was", "were", "been", "have"]

def convert_verb(verb, tag):
	if len(wn.morphy(verb, wn.VERB)) > 0:
		base = wn.morphy(verb, wn.VERB)
	Synonyms = retrieve_data(base, "verb")[0]
	synonym = optimizer(Synonyms)
	if tag == "VB":
		return conjugate(synonym, "inf")
	elif tag == "VBD":
		return conjugate(synonym, "p")
	elif tag == "VBG":
		return conjugate(synonym, "part")
	elif tag == "VBN":
		return conjugate(synonym, "ppart")
	elif tag == "VBP":
		return conjugate(synonym, "1sg")
	elif tag == "VBZ":
		return conjugate(synonym, "3sg")
	else:
		print "\nERROR: Form Not Found!\n"
		return verb


adjective_forms = ["JJ", "JJR", "JJS"]
adverb_forms = ["RB", "RBR", "RBS"]
noun_forms = ["NN", "NNS"]
verb_forms = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

paragraph = "I'm just this guy, you know? I'm a CNU graduate with a degree in physics. Before starting xkcd, I worked on robots at NASA's Langley Research Center in Virginia. As of June 2007 I live in Massachusetts. In my spare time I climb things, open strange doors, and go to goth clubs dressed as a frat guy so I can stand around and look terribly uncomfortable. At frat parties I do the same thing, but the other way around. "
paragraph += "I was going through old math/sketching graph paper notebooks and didn't want to lose some of the work in them, so I started scanning pages. I took the more comic-y ones and put them up on a server I was testing out, and got a bunch of readers when BoingBoing linked to me. I started drawing more seriously, gained a lot more readers, started selling t-shirts on the site, and am currently shipping t-shirts and drawing this comic full-time. It's immensely fun and I really appreciate y'all's support."

sentences = re.findall("[^\.\?\!]+[\.\?\!]+ ", paragraph)
text = ""

for sentence in sentences:
	tagged_sentence = tag(sentence)
	for tagged_word in tagged_sentence:
		if tagged_word[1] in whitelist:
			text += tagged_word[0]
		elif tagged_word[1] in adjective_forms:
			try:
				synonym = convert_adjective(tagged_word[0], tagged_word[1])
			except:
				text += tagged_word[0]
			else:
				text += synonym
		elif tagged_word[1] in adverb_forms:
			try:
				synonym = convert_adverb(tagged_word[0], tagged_word[1])
			except:
				text += tagged_word[0]
			else:
				text += synonym
		elif tagged_word[1] in noun_forms:
			try:
				synonym = convert_noun(tagged_word[0], tagged_word[1])
			except: 
				text += tagged_word[0]
			else:
				text += synonym
		elif tagged_word[1] in verb_forms:
			try:
				synonym = convert_verb(tagged_word[0], tagged_word[1])
			except:
				text += tagged_word[0]
			else:
				text += synonym
		else:
			text += tagged_word[0]
		text += " "

#Fix: spaces before punctuation
text = replace_string(" .", ".", text)
text = replace_string(" ?", "?", text)
text = replace_string(" !", "!", text)

'''#Fix: apostrophes fuck shit up
text = replace_string("'s", "is", text)	#does, has?
text = replace_string("'m", "am", text)
text = replace_string("'re", "are", text)
text = replace_string("'nt", "not", text)
text = replace_string("'ll", "will", text)
text = replace_string("'ve", "have", text)
'''

print text



raw_input()

'''TO BE FIXED:
		Spaces before end punctuation
	Apostrophes fuck shit up
	A/an confusion
	implement whitelist
'''
#Thesaurus service provided by words.bighugelabs.com