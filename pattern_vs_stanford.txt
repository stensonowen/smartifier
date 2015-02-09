Python 2.7.6 (default, Nov 10 2013, 19:24:24) [MSC v.1500 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> from nltk.tag.stanford import POSTagger
>>> from nltk.tokenize import word_tokenize
>>> from pattern.en import parse
>>> import os
>>> os.environ['JAVAHOME'] = "G:\\Programs\\Java\\jdk1.8.0_05\\bin\\java.exe"
>>> tagger = POSTagger("G:\\Scripts\\Python\\WordsWordsWords\\stanford-postagger-2014-06-16\\models\\english-bidirectional-distsim.tagger", "G:\\Scripts\\Python\\WordsWordsWords\\stanford-postagger-2014-06-16\\stanford-postagger.jar")
>>> 
>>> def tag1(sentence):
	tokens = word_tokenize(sentence)
	return tagger.tag(tokens)

>>> def tag2(sentence):
	return parse(sentence, chunks=False)

>>> 
>>> test1 = "The quick brown fox jumps over the lazy dog"
>>> 
>>> tag1(test1)
[('The', 'DT'), ('quick', 'JJ'), ('brown', 'JJ'), ('fox', 'NN'), ('jumps', 'VBZ'), ('over', 'IN'), ('the', 'DT'), ('lazy', 'JJ'), ('dog', 'NN')]
>>> tag2(test1)
u'The/DT quick/JJ brown/JJ fox/NN jumps/NNS over/IN the/DT lazy/JJ dog/NN'
>>> def tag11(sentence):
	tokens = word_tokenize(sentence)
	text = ""
	for word in tagger.tag(tokens):
		text += word[0] + "/" + word[1] + " "
	return text

>>> tag11(test1)
'The/DT quick/JJ brown/JJ fox/NN jumps/VBZ over/IN the/DT lazy/JJ dog/NN '
>>> def tag1(sentence):
	tokens = word_tokenize(sentence)
	text = ""
	for word in tagger.tag(tokens):
		text += word[0] + "/" + word[1] + " "
	return text

>>> 
>>> 
>>> 
>>> tag1(test1)
'The/DT quick/JJ brown/JJ fox/NN jumps/VBZ over/IN the/DT lazy/JJ dog/NN '
>>> tag2(test1)
u'The/DT quick/JJ brown/JJ fox/NN jumps/NNS over/IN the/DT lazy/JJ dog/NN'
>>> 
>>> print tag1(test1)
The/DT quick/JJ brown/JJ fox/NN jumps/VBZ over/IN the/DT lazy/JJ dog/NN 
>>> print tag2(test1)
The/DT quick/JJ brown/JJ fox/NN jumps/NNS over/IN the/DT lazy/JJ dog/NN
>>> 
>>> 


>>> 

>>> 
>>> test2 = "A waitress and an ex-cop fall in love back stage."
>>> 
>>> print tag1(test2)
A/DT waitress/NN and/CC an/DT ex-cop/JJ fall/NN in/IN love/NN back/NN stage/NN ./. 
>>> print tag2(test2)
A/DT waitress/NN and/CC an/DT ex-cop/NN fall/NN in/IN love/NN back/RB stage/NN ./.
>>> 
>>> points1, points2 = 1, 0
>>> 
>>> 
>>> 
>>> test3 = "A man dying of cancer saves a child on a military base."
>>> print tag1(test3)
A/DT man/NN dying/VBG of/IN cancer/NN saves/VBZ a/DT child/NN on/IN a/DT military/JJ base/NN ./. 
>>> print tag2(test3)
A/DT man/NN dying/VBG of/IN cancer/NN saves/VBZ a/DT child/NN on/IN a/DT military/JJ base/NN ./.
>>> 
>>> points1 += 1
>>> points2 += 1
>>> 
>>> 
>>> test4 = "Brothers lose their sanity in Montana."
>>> print tag1(test4)
Brothers/NNPS lose/VBP their/PRP$ sanity/NN in/IN Montana/NNP ./. 
>>> print tag2(test4)
Brothers/NNS lose/VBP their/PRP$ sanity/NN in/IN Montana/NNP ./.
>>> points2 += 1
>>> 
>>> 
>>> test5 = "A computer programmer adopts a baby and ends up betraying his best friend."
>>> print tag1(test5)
A/DT computer/NN programmer/NN adopts/VBZ a/DT baby/NN and/CC ends/VBZ up/RP betraying/VBG his/PRP$ best/JJS friend/NN ./. 
>>> print tag2(test5)
A/DT computer/NN programmer/NN adopts/VBZ a/DT baby/NN and/CC ends/VBZ up/IN betraying/VBG his/PRP$ best/JJS friend/NN ./.
>>> points1 += 1
>>> 
>>> 
>>> test6 = "A prostitute renews his faith over the Winter."
>>> print tag1(test6)
A/DT prostitute/NN renews/VBZ his/PRP$ faith/NN over/IN the/DT Winter/NNP ./. 
>>> print tag2(test6)
A/DT prostitute/NN renews/VBZ his/PRP$ faith/NN over/IN the/DT Winter/NNPS ./.
>>> points1 += 1
>>> 
>>> 
>>> 
>>> test7 = "A desperate mother must return money stolen from the mob."
>>> print tag1(test7)
A/DT desperate/JJ mother/NN must/MD return/VB money/NN stolen/VBN from/IN the/DT mob/NN ./. 
>>> print tag2(test7)
A/DT desperate/JJ mother/NN must/MD return/VB money/NN stolen/VBN from/IN the/DT mob/NN ./.
>>> points1 -= 1
>>> points2 -= 1
>>> 
>>> 
>>> test8 = "A bad chef finishes a marathon in prison."
>>> print tag1(test8)
A/DT bad/JJ chef/NN finishes/VBZ a/DT marathon/NN in/IN prison/NN ./. 
>>> print tag2(test8)
A/DT bad/JJ chef/NN finishes/VBZ a/DT marathon/NN in/IN prison/NN ./.
>>> 
>>> 
>>> test9 = "A prince is transformed by a radioactive spider in Purgatory."
>>> print tag1(test8)
A/DT bad/JJ chef/NN finishes/VBZ a/DT marathon/NN in/IN prison/NN ./. 
>>> print tag2(test8)
A/DT bad/JJ chef/NN finishes/VBZ a/DT marathon/NN in/IN prison/NN ./.
>>> 
>>> 
>>> test10 = "Feuding neighbors are robbed while running from the mob."
>>> print tag1(test8)
A/DT bad/JJ chef/NN finishes/VBZ a/DT marathon/NN in/IN prison/NN ./. 
>>> print tag2(test8)
A/DT bad/JJ chef/NN finishes/VBZ a/DT marathon/NN in/IN prison/NN ./.
>>> print tag1(test9)
A/DT prince/NN is/VBZ transformed/VBN by/IN a/DT radioactive/JJ spider/NN in/IN Purgatory/NNP ./. 
>>> print tag2(test9)
A/DT prince/NN is/VBZ transformed/VBN by/IN a/DT radioactive/JJ spider/NN in/IN Purgatory/NNP ./.
>>> 
>>> 
>>> print tag1(test10)
Feuding/VBG neighbors/NNS are/VBP robbed/VBN while/IN running/VBG from/IN the/DT mob/NN ./. 
>>> print tag2(test10)
Feuding/VBG neighbors/NNS are/VBP robbed/VBN while/IN running/VBG from/IN the/DT mob/NN ./.
>>> 
>>> 
>>> test11 = "An insane flight attendant has 24 hours to save her family from kidnappers."
>>> print tag1(test11)
An/DT insane/JJ flight/NN attendant/NN has/VBZ 24/CD hours/NNS to/TO save/VB her/PRP$ family/NN from/IN kidnappers/NNS ./. 
>>> print tag2(test11)
An/DT insane/JJ flight/NN attendant/NN has/VBZ 24/CD hours/NNS to/TO save/VB her/PRP$ family/NN from/IN kidnappers/NNS ./.
>>> 
>>> 
>>> test12 = "A sister and brother overhear a conversation that changes everything at The White House."
>>> print tag1(test12)
A/DT sister/NN and/CC brother/NN overhear/VBP a/DT conversation/NN that/WDT changes/VBZ everything/NN at/IN The/DT White/NNP House/NNP ./. 
>>> print tag2(test12)
A/DT sister/NN and/CC brother/NN overhear/VB a/DT conversation/NN that/IN changes/NNS everything/NN at/IN The/DT White/NNP House/NNP ./.
>>> points1 += 1
>>> 
>>> 
>>> points1
4
>>> points2
1
>>> 
>>> 
>>> 
>>> test13 = "A child dying of cancer meets someone who shares a common friend in a spooky cemetary."
>>> print tag1(test13)
A/DT child/NN dying/VBG of/IN cancer/NN meets/VBZ someone/NN who/WP shares/VBZ a/DT common/JJ friend/NN in/IN a/DT spooky/JJ cemetary/NN ./. 
>>> print tag2(test13)
A/DT child/NN dying/VBG of/IN cancer/NN meets/VBZ someone/NN who/WP shares/NNS a/DT common/JJ friend/NN in/IN a/DT spooky/JJ cemetary/NN ./.
>>> points1+= 1
>>> 
>>> 
>>> 
