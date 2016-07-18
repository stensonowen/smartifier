# Smartifier
Use a thesaurus and a language toolkit to make any block of text sound smarter (or more pretentious) while maintaining (theoretically) correct grammar.
Originally written Summer of 2014

###About

This uses [nltk](http://www.nltk.org/), [pattern](http://www.clips.ua.ac.be/pattern), and [spaCy](https://spacy.io/) for natural language processing; it parses each word (spaCy), converts it to its base form (nltk.corpus.wordnet), looks up synonyms for the lemma (with [Big Huge Thesaurus](https://words.bighugelabs.com/)), converts the longest synonym to the form of the original (pattern.en), and replaces the original with it.

Synonyms are only checked for words that spaCy recognizes as adjectives, adverbs, (common) nouns, and verbs. It also omits a list of common words that aren't easily replaced; this data is mostly pulled from the 100 most commonly used English words, with a few tweaks. 

I originally wrote it in the summer of 2014. [That version](old/Smartifier4.py) was a little rough, as I wrote it while still learning Python. It used the [Stanford parser](http://nlp.stanford.edu/software/lex-parser.shtml), which is very good, but was clunky in my project because it's written in Java. spaCy's POS-tagger is both extremely good and extremely fast, and it also plays nicely with Python. spaCy is also much easier to set up in my experience (though that's probably not fair because I set up the Stanford parser on Windows when I was in high school).

Unfortunately, pattern is only for Python2. There is an [admirable effort](https://github.com/pattern3/pattern) to port it to Python3, which I might contribute to, but it doesn't seem to be in a place where I could incorporate it. So for now the project is Python2. The [bit that I need](https://github.com/pattern3/pattern/tree/master/pattern/text/en) seems to work with Python3, but I've had mixed results building the whole project. So I ported smartifier to Python3 and threw together a vagrant box that would handle the language dependencies and draw from just part of pattern3. 


###Quick Setup

`vagrant up`, `vagrant ssh`, `python3 /vagrant/smartifier.py input output`

Provisioning the vagrant box can take a little while; the brunt of the setup is downloading the debian image (~300MB), setting up the VM, and downloading spaCy data (~500MB). On a mediocre machine with a mediocre internet connection it takes about 30 minutes.

Once set up, the python script can take positional input/output arguments or use standard input/output. For example, `echo "the quick brown fox jumps over the lazy dog" | python3 smartifier.py  > output`.

###Parser Selection

I spent some time looking around for other options for parsers. I considered Google's recently open-sourced option, "Parsey McParseface", which seemed pleasantly accurate, but it would be unpleasant to interface (the most straightforward way to do so would probably be to parse the results of a `subprocesses` call, which is pretty icky; digging through the code so I could just `import` a fork of it sounds unpleasant, and it would mean I'd have to use python 2.7). 

Additionally, one of the reasons I initially wanted to rewrite this program was to make it easier to set up and use; it would be nice to just `pip install` a few dependencies rather than setting up the Stanford parser with a JVM like before. However, Parsey is build with bazel, and it felt like an insufficient improvement to require a dependency that needed to be run via a JVM. 

I found [spaCy](https://spacy.io) on [HN](https://news.ycombinator.com/item?id=8942783) and it looked like a good candidate. It doesn't require a complex setup, just `pip` and to download a (albeit large) language model. Additionally, it seems to be almost as accurate as PMcPF, but significantly faster (maybe. I might be comparing POS-tagging to POS-tagging + dependency parsing, which isn't fair. I might have to do some benchmarks).


