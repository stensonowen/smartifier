#Classify Stanford data, organize into relevant data in preparation to specify search query

from nltk.tag.stanford import POSTagger
from nltk.tokenize import word_tokenize
import os, re
from nltk.corpus import wordnet as wn
from pattern.en import comparative, superlative, pluralize
from pattern.en import conjugate, verbs, tenses, PAST, PL, PARTICIPLE

#sentence = "What is the airspeed of an unladen swallow?"
os.environ['JAVAHOME'] = "G:\\Programs\\Java\\jdk1.8.0_05\\bin\\java.exe"
tagger = POSTagger("G:\\Scripts\\Python\\WordsWordsWords\\stanford-postagger-2014-06-16\\models\\english-bidirectional-distsim.tagger", "G:\\Scripts\\Python\\WordsWordsWords\\stanford-postagger-2014-06-16\\stanford-postagger.jar")

tagset = {
	"CC": 	"Coordinating Conjunction",
	"CD": 	"Cardinal Number",
	"DT": 	"Determiner",
	"EX": 	"Existential There",
	"FW":	"Foreign Word",
	"IN":	"Preposition or Subordinating Conjunction",
	"JJ":	"Positive Adjective",
	"JJR":	"Comparative Adjective",
	"JJS":	"Superlative Adjective"
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

#only execute if synonyms are found?
#use the synonym that contains the longest word
def optimizer(synset): #add in antonyms, related terms, and similar terms?
	leader, score = "", 0
	for syn in synset:
		parts = re.split("-| ", syn)
		parts = sorted(parts, key=len)
		if len(parts[-1]) > score:
			leader = syn
			score = len(parts[-1])
	return leader

def tag(sentence):
	tokens = word_tokenize(sentence)
	return tagger.tag(tokens)

def convert_adjective(adjective, tag):
	#determine, save form (pos, comp, superl)
	if tag == "JJ":
		form = "Positive"
	elif tag == "JJR":
		form = "Comparative"
	elif tag == "JJS":
		form = "Superlative"
	else:
		form = "Positive"
		print "\nERROR: Form Not Found!\n"
	#if comp or superl, convert to base form
	if len(wn.morphy(adjective, wn.ADJ)) > 0:
		base = wn.morphy(adjective, wn.ADJ)		#-p-r-o-d-u-c-e- -e-r-r-o-r-s-?-
	#find synonyms for base form
	Synonyms = retrieve_data(base, "adjective")[0]
	#find ideal synonyms
	synonym = optimizer(Synonyms)
	#if comp or superl, convert synonym to proper form
	if form == "Comparative":
		synonym = comparative(synonym)
	elif form == "Superlative":
		synonym = superlative(synonym)
	#return synonym
	return synonym

def convert_adverb(adverb, tag):
	if tag == "RB":
		form = "Positive"
	elif tag == "RBR":
		form = "Comparative"
	elif tag == "RBS":
		form = "Superlative"
	else:
		form = "Positive"
		print "\nERROR: Form Not Found!\n"
	if len(wn.morphy(adverb, wn.ADV)) > 0:
		base = wn.morphy(adverb, wn.ADV)
	Synonyms = retrieve_data(base, "adverb")[0]
	synonym = optimizer(Synonyms)
	if form == "Comparative":
		synonym = comparative(synonym)
	elif form == "Superlative":
		synonym = superlative(synonym)
	return synonym

def convert_noun(noun, tag):
	if tag == "NN":
		form = "Singular"
	elif tag == "NNP":
		form = "Plural"
	else:
		form = "Singular"
		print "\nERROR: Form Not Found!\n"
	if len(wn.morphy(noun, wn.NOUN)) > 0:
		base = wn.morphy(noun, wn.NOUN)
	Synonyms = retrieve_data(base, "noun")[0]
	synonym = optimizer(Synonyms)
	if form == "Plural":
		synonym = pluralize(synonym)
	return synonym

whitelist = ["be", "am", "is", "are", "was", "were", "been", "have"]
def convert_verb(verb, tag):
	if len(wn.morphy(verb, wn.VERB)) > 0:
		base = wn.morphy(verb, wn.VERB)
	Synonyms = retrieve_data(base, "verb")[0]
	synonym = optimizer(Synonyms)
	if tag == "VB":		#verb, base form:		ask, assemble, assess, ...
		#synonym = conjugate(synonym, tense=INFINITIVE)
		synonym = conjugate(synonym, "inf")
	elif tag == "VBD":	#verb, past tense:		dipped, pleaded, swiped, ...
		#synonym = conjugate(synonym, tense=PAST)
		synonym = conjugate(synonym, "p")
	elif tag == "VBG":	#verb, present participle / gerund:		stirring, angering, judging, ...
		#synonym = conjugate(synonym, tense=PARTICIPLE)
		synonym = conjugate(synonym, "part")
	elif tag == "VBN":	#verb, past participle:		used, flourished, imitated, dubbed, ...
		#synonym = conjugate(synonym, tense=PAST+PARTICIPLE)
		synonym = conjugate(synonym, "ppart")
	elif tag == "VBP":	#verb, present tense, 1st/2nd person singular:		wrap, resort, sue, twist, ...
		#synonym = conjugate(synonym, person=1, number=SINGULAR)
		synonym = conjugate(synonym, "1sg")
	elif tag == "VBZ":	#verb, present tense, 3rd person singular:		bases, marks, mixes, slaps, ...
		#synonym = conjugate()
		synonym = conjugate(synonym, "3sg")