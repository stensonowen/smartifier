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

tagset = {
	"CC": 	"Coordinating Conjunction",
	"CD": 	"Cardinal Number",
	"DT": 	"Determiner",
	"EX": 	"Existential There",
	"FW":	"Foreign Word",
	"IN":	"Preposition or Subordinating Conjunction",
	"JJ":	"Positive Adjective",
	"JJR":	"Comparative Adjective",
	"JJS":	"Superlative Adjective",
	"LS":	"List Item Marker",
	"MD":	"Modal",										#e.g. CAN, COULD, MIGHT, MAY...
	"NN":	"Singular Common Noun",
	"NNP":	"Singular Proper Noun",
	"NNPS":	"Plural Proper Noun",
	"NNS":	"Plural Common Noun",
	"PDT":	"Predeterminer",								#e.g. ALL, BOTH ... when they precede an article
	"POS":	"Possessive Ending",
	"PRP":	"Personal Pronoun",
	"PRP$":	"Possessive Pronoun",
	"RB":	"Positive Adverb",
	"RBR":	"Comparative Adverb",
	"RBS":	"Superlative Adverb",
	"RP":	"Particle",
	"SYM":	"Symbol",
	"TO":	"To",
	"UH":	"Uh",
	"VB":	"Base Verb",
	"VBD":	"Past Verb",
	"VBG":	"Present Participle Verb",
	"VBN":	"Past Participle Verb",
	"VBP":	"Non-3rd Person Singular Verb",
	"VBZ":	"3rd Person Singular Verb",
	"WDT":	"Wh-determiner",								#e.g. WHICH, and THAT when it is used as a relative pronoun
	"WP":	"Wh-pronoun",									#e.g. WHAT, WHO, WHOM
	"WP$":	"Possessive wh-pronoun",						#e.g. WHOSE
	"WRB":	"Wh-adverb"										#e.g. HOW, WHERE, WHY
}

#Forms to manually fix: VERBS, NOUNS (sing/plural), comparative/SUPERLATIVE ADJECTIVES, comparative/SUPERLATIVE ADVERBS, 
Replacable_Forms = ["(Positive) Adjective", "(Common) Noun", "(Positive) Adverb", "(Base) Verb"]



def retrieve_data(word, pos):
	try:
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
	except:
		print "\nERROR: Failed to find synonyms\n"
		return [word], [], [], []
	else:
		return Synonyms, Antonyms, Relateds, Similars

def tag(sentence):
	tokens = word_tokenize(sentence)
	return tagger.tag(tokens)

#only execute if synonyms are found?
#use the synonym that contains the longest word
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
	elif tag == "NNP":
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
	if tag == "VB":		#verb, base form:		ask, assemble, assess, ...
		return conjugate(synonym, "inf")
	elif tag == "VBD":	#verb, past tense:		dipped, pleaded, swiped, ...
		return conjugate(synonym, "p")
	elif tag == "VBG":	#verb, present participle / gerund:		stirring, angering, judging, ...
		return conjugate(synonym, "part")
	elif tag == "VBN":	#verb, past participle:		used, flourished, imitated, dubbed, ...
		return conjugate(synonym, "ppart")
	elif tag == "VBP":	#verb, present tense, 1st/2nd person singular:		wrap, resort, sue, twist, ...
		return conjugate(synonym, "1sg")
	elif tag == "VBZ":	#verb, present tense, 3rd person singular:		bases, marks, mixes, slaps, ...
		return conjugate(synonym, "3sg")
	else:
		print "\nERROR: Form Not Found!\n"
		return verb