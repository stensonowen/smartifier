# Smartifier
Use a thesaurus and a language toolkit to make any block of text sound smarter (or more pretentious) while maintaining (theoretically) correct grammar.
Originally written Summer of 2014


I was playing around with python as an interface for software from the Stanford Natural Language Processing Group (http://nlp.stanford.edu/software/), a Java-based engine, and started trying to disassemble and re-assemble sentences. 

A while ago I'd had the idea to look up every word in a sentence in a thesaurus and replace it with its longest synonym, but this would be largely ineffective because it would only work (well) with words in their base forms (e.g. "see" becomes "observe", but "seeing" is either unrecognized or becomes "observe" anyway). This seemed like an interesting and useful addition (I was also curious about the limits of the software, because it seemed quite accurate). 

I also looked into the Natural Language ToolKit (http://www.nltk.org/), which had the advantage of being native to Python and drawing from multiple sources, such as Princeton's WordNet. They both seemed to have different strengths, so I tested them in different areas that I planned to use. For example, the Stanford NLP Group's parser took context into account better than the NLTK's (e.g. in the sentence "they saw him", "saw" is a simple past verb, not a literal saw), whereas NLTK could very accurately differentiate between a word's forms.

The result takes a paragraph as input, identifies the role of each word in a sentence, and checks for possible replacements. Assuming the word is an appropriate part of speech (e.g. adjective, verb, etc. but not article or proper noun), it looks up the base form using the Big Huge Thesaurus API (https://words.bighugelabs.com/). It takes the longest synonym (or possibly a synonym's homophone), converts it into the original word's form, and replaces it in the paragraph. It later cycles through words and fixes possible minor errors (e.g. capitalization, 'a' vs. 'an', etc.) and outputs the result. 

The final project (Smartifier4.py) is a little rough around the edges, but it was more out of curiosity than anything (I stopped once I had a working version with only mindless debugging left to do). Included is one of the text blocks I used to test final version, the "about me" section of http://xkcd.com.

Edit (9/29/15): In the process of removing weird non-python dependencies (mostly the Stanford POSTagger). Currently the modified smartifier only requires a few python libraries: to set up, pip install pattern and nltk (and mechanize, but that'll probably go also). Then in python, import nltk, run nltk.download(), and download wordnet.
