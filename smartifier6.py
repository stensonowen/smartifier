#!/usr/bin/python2

from nltk.corpus import wordnet     #parse words
import pattern.en as pattern        #decline/conjugate
import spacy                        #parse sentences

import requests


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
    best = ("",-1)
    for entry in lis:
        if entry[1] > best[1]:
            best = entry
    return best


def select_synonym(syns):
    #return the synonym or phrase which contains the longest word
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
    def new(word, pos):
        tag_decode = {
            "JJ": Adjective,
            "RB": Adverb,
            "NN": Noun,
            "VB": Verb,
            }
        hint = pos[:2]
        form = tag_decode.get(hint) or Word
        return form(word, pos)

    def __init__(self, word, pos):
        self.word = word
        self.pos = pos

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
        return self.word

            


#subclasses categorized/defined by what attribute they have
#adjectives and adverbs both have 'degree'

class Degree(Word):
    #adj or adv
    def re_base(self, new_base):
        if self.pos[-1] == "S":
            return pattern.superlative(new_base)
        elif self.pos[-1] == "R":
            return pattern.comparative(new_base)
        else:
            return new_base


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
        if self.pos[-1] == "S":
            return pattern.pluralize(new_base)
        else:
            return new_base


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
        return pattern.conjugate(new_base, desc)

def smartify(nlp, sent):
    if type(sent) is not unicode:
        sent = unicode(sent)

    f = open("whitelist", "r")
    whitelist = f.readlines()
    whitelist = [word.strip().lower() for word in whitelist]
    whitelist = set(whitelist)

    words = [Word.new(w.text, w.tag_) for w in nlp(sent)]

    results = []
    for word in words:
        #convert word if it is a specific class
        #only smartify noun/verb/ad[j|v] 
        invalid_pos  = word.Pos_word is None
        invalid_word = word.word.lower() in whitelist
        if invalid_pos or invalid_word:
            results.append(word.word)
        else:
            syns = get_synonyms(word.base(), word.Pos_word)
            syn  = select_synonym(syns)
            results.append(word.re_base(syn))
    return results



if __name__ == "__main__":
    s = "the quick brown fox jumps over the lazy dog"
    s = "stacy's mom has got it going on"
    s = "what the fuck did you just say about me you little bitch?"
    s = "obama said you're fat"
    s = "is it true?"
    s = "what the fuck did you just say about me you little bitch?"

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




