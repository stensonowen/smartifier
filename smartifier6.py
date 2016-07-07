#!/usr/bin/python2

from nltk.corpus import wordnet     #parse words
import pattern.en as pattern        #decline/conjugate
import spacy                        #parse sentences

import requests
import re

# TODO  you're  ->  you am ???
# TODO  things  ->  belongingss

WHITELIST = set([ 
    #custom whitelist in addition to just common words
    "let",  # screw up "let's"
    "'re",  # tries to parse second half of "you're" independently
    ])

def get_synonyms(word, pos):
    #fetch synonyms from bighugelabs.com
    #only interested in synonyms; ignore other results
    try:
        synonyms = [word]
        url = "http://words.bighugelabs.com/api/2/{}/{}/json".format(
                "11f898808fffe257228d17890b1101f1",
                word)
        json = requests.get(url).json()
        #get synonyms of the correct POS only
        synonyms += json[pos]['syn']
    except ValueError:
        print "Failed to find word: " + str(word) + " (" + str(pos) + ")"
    except KeyError:
        print "Failed to find part of speech " + str(word) + " (" + str(pos) + ")"
    return synonyms


def longest(lis):
    #lis a list of tuples of (word, len(word))
    #returns whichever tuple has the longest second part
    best = ("",-1)
    for entry in lis:
        if entry[1] > best[1]:
            best = entry
    return best


def select_synonym(syns):
    #return the synonym or phrase which contains the longest word
    #If you want to change how the 'best' synonym is selected,
    # this is the place to do it
    #TODO: should hyphenate multi-word synonyms so results will make more sense?
    groups = [
            [(syn,len(word)) for word in syn.split()]
            for syn in syns]
    bests = [longest(entry) for entry in groups]
    return longest(bests)[0]


def parse(nlp, sent):
    if type(sent) is not unicode:
        sent = unicode(sent)
    return [(w.text, w.tag_) for w in nlp(sent)]



class Word():
    Wn_tag = Pos_word = None

    @staticmethod
    #def new(word, pos):
    def new(token):
        tag_decode = {
            "JJ":   Adjective,
            "RB":   Adverb,
            "NNP:": ProperNoun,
            "NN":   Noun,
            "VB":   Verb,
            }
        #hint = pos[:2]
        #form = tag_decode.get(hint) or Word
        for tag in tag_decode:
            if token.tag_.startswith(tag):
                return tag_decode[tag](token)
        return Word(token)

    #def __init__(self, word, pos):
    def __init__(self, token):
        self.word   = token.text
        self.pos    = token.tag_
        self.space  = len(token.whitespace_)

    def base(self):
        #wn_tag = Word.TagToWn(self.pos) #noun/verb/ad[v|j]
        wn_tag = self.Wn_tag or None
        if wn_tag and len(self.pos) > 2:
            #not base form already
            guess = wordnet.morphy(self.word, wn_tag)
            return guess or self.word
        else:
            return self.word

    def re_base(self, new_base):
        self.word = new_base

    def __str__(self):
        return self.word + " "*self.space
            


#subclasses categorized/defined by what attribute they have
#adjectives and adverbs both have 'degree'

class Degree(Word):
    #adj or adv
    def re_base(self, new_base):
        if self.pos[-1] == "S":
            self.word = pattern.superlative(new_base)
        elif self.pos[-1] == "R":
            self.word = pattern.comparative(new_base)
        else:
            self.word = new_base


class Adjective(Degree):
    Wn_tag = wordnet.ADJ
    Pos_word = "adjective"


class Adverb(Degree):
    Wn_tag = wordnet.ADV
    Pos_word = "adverb"


class Noun(Word):
    Wn_tag = wordnet.NOUN
    Pos_word = "noun"
    
    def re_base(self, new_base):
        if self.pos == "NNS":
            #plural common noun
            self.word = pattern.pluralize(new_base)
        elif self.pos.startswith("NNP"):
            #proper noun
            self.word = self.word
        else:
            self.word = new_base

class ProperNoun(Noun):
    #Just exists for organization's sake
    #Do not try to parse this; it's probably a waste of time
    Wn_tag = Pos_word = None


class Verb(Word):
    Wn_tag = wordnet.VERB
    Pos_word = "verb"

    def re_base(self, new_base):
        #get description based on third char of tag
        tag_to_desc = {
                "D": "p",       #past tense
                "G": "part",    #gerund
                "N": "ppart",   #past part
                "P": "1sg",     #non-3rd-person sing pres
                "Z": "3sg",     #3rd-person sing pres
                }
        hint = self.pos[2:3]
        desc = tag_to_desc.get(hint) or "inf"   #base
        self.word = pattern.conjugate(new_base, desc)

def smartify(nlp, sent):
    if type(sent) is not unicode:
        sent = unicode(sent)

    #f = open("whitelist_1k", "r")
    #   https://simple.wikipedia.org/wiki/Wikipedia:List_of_1000_basic_words
    f = open("whitelist", "r")
    whitelist = f.readlines()
    whitelist = [word.strip().lower() for word in whitelist]
    whitelist = set(whitelist)

    #make words lowercase to facilitate strcmps
    #words = [Word.new(w.text, w.tag_) for w in nlp(sent)]
    words = [Word.new(token) for token in nlp(sent)]

    results = []
    for word in words:
        #convert word if it is a specific class
        #only smartify noun/verb/ad[j|v] 
        base = word.base().lower()
        invalid_pos  = word.Pos_word is None
        invalid_word = base in whitelist or base in WHITELIST
        if invalid_pos or invalid_word:
            results.append(str(word))
        else:
            syns = get_synonyms(base, word.Pos_word)
            syn  = select_synonym(syns)
            word.re_base(syn)
            results.append(str(word))
    return results

def fix(words):
    #words is a list of words; 
    #most of this stuff is fixed by using spacy's spacing
    '''Things to fix:
        * spaces around hyphens
        * hyphenated pluralizations?
            * a/an fixes
            * capitalize: proper nouns / first words
        * quotation marks?
    ''' 
    sent = ""
    for i in range(len(words)):
        #iterating by index allows easier lookahead/-behind
        #make sure all changes that conflict have mutually exclusive triggers

        word = words[i]

        #handle indefinite articles
        if word == "a" or word == "an" and i < len(words)-1:
            word = pattern.article(words[i+1]) #, function="indefinite") 


        #capitalize first word
        if i == 0:
            word = word[0].upper() + word[1:]

        sent += word
    return sent.strip()




if __name__ == "__main__":
    s = "the quick brown fox jumps over the lazy dog"
    s = "stacy's mom has got it going on"
    s = "what the fuck did you just say about me you little bitch?"
    s = "obama said you're fat"
    s = "is it true?"
    s = "I am seated in an office, surrounded by heads and bodies"
    s = '"That\'s what", she said'

    nlp = spacy.en.English(tagger=True, parser=False, entity=False)
    t = smartify(nlp, s)
    print " ".join(t)



if __name__ == "x__main__":
    #print get_synonyms("word", "noun")
    words = ["alpha", "beta", "gamma", "delta", "epsilon"]
    print select_synonym(words)
    words2 = ["a", "b b b b b b b", "exc f"]
    print select_synonym(words2)


if __name__ == "y__main__":
    s = "the quick brown fox jumps over the lazy dog"
    nlp = new_nlp()
    tokens = parse(nlp, s)

    words = [Word.new(word,pos) for (word,pos) in tokens]
    print "word \t base \t parse\n" 
    for w in words:
        print w.word, "\t", w.base() 

    a = Word("faster", "JJR")
    print a.word, "\t", a.re_base("quick") 



    a = Word.new("green", "JJ")
    b = Word.new("happiest", "VBZ")
    c = Word.new("gorilla", "VBD")
    x = [a, b, c]
    #jprint("Bases: " + ", ".join([i.base() for i in x]))
    #print("Parses: " + ", ".join([i.parse() for i in x]))




