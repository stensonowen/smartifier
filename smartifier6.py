#!/usr/bin/python2
from nltk.corpus import wordnet as wn
import pattern.en as pattern
import spacy


def new_nlp():
    return spacy.en.English(parser=False, entity=False)

def parse(nlp, sent):
    return [(w.text, w.tag_) for w in nlp(sent)]



class Word():
    Wn_tag = Pos_word = None

    @staticmethod
    def TagToObj(tag):
        return {
            "JJ": Adjective,
            "RB": Adverb,
            "NN": Noun,
            "VB": Verb,
            }.get(tag)


            
    @staticmethod
    def new(word, pos):
        hint = pos[:2]
        form = Word.TagToObj(hint) or Word
        return form(word, pos)

    def __init__(self, word, pos):
        self.word = word
        self.pos = pos

    def base(self):
        #wn_tag = Word.TagToWn(self.pos) #noun/verb/ad[v|j]
        wn_tag = self.Wn_tag or None
        if wn_tag and len(self.pos) > 2:
            #not base form already
            guess = wn.morphy(self.word, wn_tag)
            return guess or self.word
        else:
            return self.word

    def re_base(self, new_base):
        return "ERR"


#subclasses categorized/defined by what attribute they have
#adjectives and adverbs both have 'degree'

class Degree(Word):
    #adj or adv

    def re_base(self, new_base):
        if self.pos[-1] == "S":
            return pattern.superlative(new_base)
        elif self.post[-1] == "R":
            return pattern.comparative(new_base)
        else:
            return new_base


class Adjective(Degree):
    Wn_tag = wn.ADJ
    Pos_word = "adjective"


class Adverb(Degree):
    Wn_tag = wn.ADV
    Pos_word = "adverb"


class Noun(Word):
    Wn_tag = wn.NOUN
    Pos_word = "noun"
    
    def re_base(self, new_base):
        if self.pos[-1] == "S":
            return pattern.pluralize(new_base)
        else:
            return new_base


class Verb(Word):
    Wn_tag = wn.VERB
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

if __name__ == "__main__":
    s = u"the quick brown fox jumps over the lazy dog"
    nlp = new_nlp()
    tokens = parse(nlp, s)

    words = [Word.new(word,pos) for (word,pos) in tokens]
    print("word \t base \t parse\n")
    for w in words:
        print(w.word, "\t", w.base())

    a = Word("faster", "JJR")
    print(a.word, "\t", a.re_base("quick"))



    a = Word.new("green", "JJ")
    b = Word.new("happiest", "VBZ")
    c = Word.new("gorilla", "VBD")
    x = [a, b, c]
    #jprint("Bases: " + ", ".join([i.base() for i in x]))
    #print("Parses: " + ", ".join([i.parse() for i in x]))




