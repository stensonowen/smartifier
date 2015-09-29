from nltk.tag.stanford import POSTagger
from nltk.tokenize import word_tokenize
import os
sentence = "What is the airspeed of an unladen swallow?"
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
	"JJR":	"Comparitive Adjective",
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
	"RBR":	"Comparitive Adverb",
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

def tag(sentence):
	tokens = word_tokenize(sentence)
	return tagger.tag(tokens)

