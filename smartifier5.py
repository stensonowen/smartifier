import mechanize, re, os
from nltk.corpus import wordnet as wn
from pattern.en import comparative, superlative, pluralize, conjugate, referenced
from pattern.en import parse
from datetime import datetime

br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

whitelist = ["be", "am", "is", "are", "was", "were", "been", "have", "had", "has"]

adjective_forms = ["JJ", "JJR", "JJS"]
adverb_forms = ["RB", "RBR", "RBS"]
noun_forms = ["NN", "NNS"]
verb_forms = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]


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

		html = re.sub('"', "", html)

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
	#tokens = sentence.split()
	#return tagger.tag(tokens)
        return parse(sentence, chunks=False)

def optimizer(synset):
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


#import input.txt
f = open("input.txt", "r")
paragraph = f.read()
f.close()

#ANALYTICS:
start = datetime.now()
totalwords, replacedwords = 0, 0


paragraph = re.sub("\n", " ", paragraph)
sentences = re.findall("[^\.\?\!]+[\.\?\!]+ ", paragraph)
text = ""

for sentence in sentences:
	#tagged_sentence = tag(sentence)
        tagged_sentence = parse(sentence, chunks=False).split()[0]
	for tagged_word in tagged_sentence:
		if tagged_word[1] in whitelist:
			text += tagged_word[0]
		elif tagged_word[1] in adjective_forms:
                        synonym = convert_adjective(tagged_word[0], tagged_word[1])
			try:
				synonym = convert_adjective(tagged_word[0], tagged_word[1])
                                print tagged_word[0] + ': success'
			except:
				text += tagged_word[0]
                                print tagged_word[0] + ': failed'
			else:
				text += synonym
				replacedwords += 1
		elif tagged_word[1] in adverb_forms:
			try:
				synonym = convert_adverb(tagged_word[0], tagged_word[1])
                                print tagged_word[0] + ': success'
			except:
				text += tagged_word[0]
                                print tagged_word[0] + ': failed'
			else:
				text += synonym
				replacedwords += 1
		elif tagged_word[1] in noun_forms:
			try:
				synonym = convert_noun(tagged_word[0], tagged_word[1])
                                print tagged_word[0] + ': success'
			except: 
				text += tagged_word[0]
                                print tagged_word[0] + ': failed'
			else:
				text += synonym
				replacedwords += 1
		elif tagged_word[1] in verb_forms:
			try:
				synonym = convert_verb(tagged_word[0], tagged_word[1])
                                print tagged_word[0] + ': success'
			except:
				text += tagged_word[0]
                                print tagged_word[0] + ': failed'
			else:
				text += synonym
				replacedwords += 1
		else:
			text += tagged_word[0]
	                print tagged_word[0] + '(' + tagged_word[1] + '): NOT FOUND'	
                text += " "
		totalwords += 1

#Fix: spaces before punctuation
text = re.sub(" \.", ".", text)
text = re.sub(" \?", "?", text)
text = re.sub(" !", "!", text)

#Fix a/an instances
for article_pair in re.findall("(?<![\w])[aA]+[n]* [\w-]+", text):
	text = re.sub(article_pair, referenced(article_pair.split()[1]), text)

#Fix Capitalization issues
text = str.capitalize(str(text[0])) + text[1:]
for letter in re.finditer("(?<=[\.\?!] )[a-z]", text):
	text = text[:letter.start()] + str.capitalize(str(text[letter.start()])) + text[letter.end():]

#ANALYTICS:
delta = datetime.now() - start
seconds = delta.seconds
summary = "Initiated at " + str(start.time()) + " on " + str(start.date()) + ".\n"
summary += "Process completed after " 
if seconds < 60:
	summary += str(seconds) + " seconds."
else:
	summary += str(seconds/60) + " minutes " + str(seconds-(seconds/60)*60) + " seconds."
summary += "\nReplaced " + str(replacedwords) + " words out of " + str(totalwords) + " total (" + str(int(100*(float(replacedwords)/float(totalwords))+.5)) + "%).\n\n"

#export output.txt
f = open("output.txt", "w")
f.write(summary + text)
f.close()




'''TO BE FIXED:
		Spaces before end punctuation
		Apostrophes fuck shit up
	A/an confusion still?
		implement whitelist
	Start-Of-Sentence Capitalization? (untested)
	Eliminated last sentence??
        Add 1000 most common words to whitelist
'''
#Thesaurus service provided by words.bighugelabs.com
