#!/usr/bin/python3

from nltk.corpus import wordnet     #parse words
import pattern.en as pattern        #decline/conjugate
import spacy                        #parse sentences

import requests
import argparse, sys, re

# TODO  things  ->  belongingss ??
#   wordnet.morphy("things","n") -> "things"
#       wordnet fails to get base of word
#       so a BHT synonym for "things" is "belongings"
#       which is assumed to also be singular
#       so pattern tries to pluralize it by adding an s


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
        print("Failed to find word: " + str(word) + " (" + str(pos) + ")")
    except KeyError:
        print("Failed to find part of speech " + str(word) + " (" + str(pos) + ")")
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
    #TODO: should maybe hyphenate multi-word synonyms so results will make more sense?
    groups = [
            [(syn,len(word)) for word in syn.split()]
            for syn in syns]
    bests = [longest(entry) for entry in groups]
    return longest(bests)[0]


def parse_(nlp, sent):
    #TODO: delete
    #if type(sent) is not unicode:
    #    sent = unicode(sent)
    return [(w.text, w.tag_) for w in nlp(sent)]



class Word():
    Wn_tag = Pos_word = None

    #ProperNoun is kind of assymetric; 
    # What's the best way to handle it?
    @staticmethod
    def new_(token):
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

    @staticmethod
    def new(token):
        tag_decode = {
            "JJ":   Adjective,
            "RB":   Adverb,
            "NN":   Noun,
            "VB":   Verb,
            }
        hint = token.tag_[:2]
        if token.tag_ == "NNP":
            form = ProperNoun
        else:
            form = tag_decode.get(hint) or Word
        return form(token)


    def __init__(self, token):
        self.word   = token.text
        self.pos    = token.tag_
        self.space  = len(token.whitespace_)
        #store spacy datum for whether word followed by spacy
        #spacy.Doc better at parsing than I am

    def base(self):
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
    #if type(sent) is not unicode:
    #    sent = unicode(sent)

    from whitelist import whitelist

    words = [Word.new(token) for token in nlp(sent)]

    results = []
    for word in words:
        #convert word if it is a specific class
        #only smartify noun/verb/ad[j|v] 
        base = word.base().lower()
        invalid_pos  = word.Pos_word is None or "'" in base
        invalid_word = base in whitelist #or base in WHITELIST
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
        if (word == "a" or word == "an") and i < len(words)-1:
            word = pattern.article(words[i+1]) #, function="indefinite") 

        #capitalize first word
        if i == 0:
            word = word[0].upper() + word[1:]

        sent += word
    return sent.strip()




if __name__ == "w__main__":
    s = "the quick brown fox jumps over the lazy dog"
    s = "stacy's mom has got it going on"
    s = "what the fuck did you just say about me you little bitch?"
    s = "I am seated in an office, surrounded by heads and bodies"
    s = '"That\'s what", she said'
    s = "Bush hid the facts."
    s = "Abraham Lincoln once said, \"If you're a racist, I will attack you with the North,\" and those are the principles that I carry with me in the workplace."
    s = "rtifier6.smartify(nlp, s))We did not manufacture the algorithmic rule. The algorithmic rule systematically finds Jesus. The algorithmic rule obliterated Jeeves.The algorithmic rule is criminalised in China. The algorithmic rule is from Jersey. The algorithmic rule perpetually finds Jesus.This is not the algorithmic rule. This is penny-pinching."
    s = "In soft regions are born soft men."
    s = "The major problem—one of the major problems, for there are several—one of the many major problems with governing people is that of whom you get to do it; or rather of who manages to get people to let them do it to them. To summarize: it is a well-known fact that those people who must want to rule people are, ipso facto, those least suited to do it. To summarize the summary: anyone who is capable of getting themselves made President should on no account be allowed to do the job." 
    s = "The path of the righteous man is beset on all sides by the iniquities of the selfish and the tyranny of evil men. Blessed is he, who in the name of charity and good will, shepherds the weak through the valley of darkness, for he is truly his brother’s keeper and the finder of lost children. And I will strike down upon thee with great vengeance and furious anger those who would attempt to poison and destroy my brothers. And you will know my name is the Lord when I lay my vengeance upon thee."


    nlp = spacy.en.English(tagger=True, parser=False, entity=False)
    t = smartify(nlp, s)
    #print(" ".join(t))
    print(fix(t))



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('input',  
            nargs   = '?', 
            type    = argparse.FileType('r'), 
            default = sys.stdin,
            help    = "File to read input from; default is stdin")
    ap.add_argument('output', 
            nargs   = '?', 
            type    = argparse.FileType('w'), 
            default = sys.stdout,
            help    = "File to write output to; default is stdout")
    args = ap.parse_args()

    text = args.input.read()
    nlp = spacy.en.English(tagger=True, parser=False, entity=False)
    result = smartify(nlp, text)
    result = fix(result)

    args.output.write(result + "\n")

    args.input.close()
    args.output.close()

        




