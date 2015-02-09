#http://stackoverflow.com/questions/7404720/nltk-fails-to-find-the-java-executable

#from nltk.tag.stanford import POSTagger
#from nltk.tag.stanford import StanfordTagger

#st = POSTagger('/usr/share/stanford-postagger/models/english-bidirectional-distsim.tagger', '/usr/share/stanford-postagger/stanford-postagger.jar')
#st = POSTagger('G:/Scripts/Python/Smartifier/stanford-postagger-2014-06-16/models/english-bidirectional-distsim.tagger', 'G:/Scripts/Python/Smartifier/stanford-postagger-2014-06-16/stanford-postagger.jar')
#st = POSTagger('G:\Scripts\Python\Smartifier\stanford-postagger-2014-06-16\models\english-bidirectional-distsim.tagger', 'G:\Scripts\Python\Smartifier\stanford-postagger-2014-06-16\stanford-postagger.jar')
#st = POSTagger('\stanford-postagger-2014-06-16\models\english-bidirectional-distsim.tagger', '\stanford-postagger-2014-06-16\stanford-postagger.jar')
#st = StanfordTagger("english-bidirectional-distsim")


from nltk.tag import StanfordTagger
import os
path_to_model = os.path.join("G:\Scripts\Python\WordsWordsWords\stanford-postagger-2014-06-16\models", "english-bidirectional-distsim.tagger")
path_to_jar = os.path.join("G:\Scripts\Python\WordsWordsWords\stanford-postagger-2014-06-16", "stanford-postagger.jar")
st = StanfordTagger(path_to_model, path_to_jar)
st.tag("What is the airspeed of an unladen swallow ?".split())




#path_to_java = os.path.join("G:\Programs\Java\jdk1.8.0_05\bin", "java.exe")

import os, nltk
sentence = "What is the airspeed of an unladen swallow ?"
path_to_model = "G:\\Scripts\\Python\\WordsWordsWords\\stanford-postagger-2014-06-16\\models\\english-bidirectional-distsim.tagger"
path_to_jar = "G:\\Scripts\\Python\\WordsWordsWords\\stanford-postagger-2014-06-16\\stanford-postagger.jar"
path_to_java = "G:\\Programs\\Java\\jdk1.8.0_05\\bin\\java.exe"
os.environ['JAVAHOME'] = path_to_java
tagger = nltk.tag.stanford.POSTagger(path_to_model, path_to_jar)
tokens = nltk.tokenize.word_tokenize(sentence)
print tagger.tag(tokens)



from nltk.tag.stanford import POSTagger
from nltk.tokenize import word_tokenize
import os
sentence = "What is the airspeed of an unladen swallow?"
os.environ['JAVAHOME'] = "G:\\Programs\\Java\\jdk1.8.0_05\\bin\\java.exe"
tagger = POSTagger("G:\\Scripts\\Python\\WordsWordsWords\\stanford-postagger-2014-06-16\\models\\english-bidirectional-distsim.tagger", "G:\\Scripts\\Python\\WordsWordsWords\\stanford-postagger-2014-06-16\\stanford-postagger.jar")
tokens = word_tokenize(sentence)
print tagger.tag(tokens)



