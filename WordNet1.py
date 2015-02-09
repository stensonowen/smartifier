from nltk.corpus import wordnet as wn

word = "fast"
relatedwords = []

for syn in wn.synsets(word):
	relatedwords.append(syn)
	for sim in syn.similar_tos():
		relatedwords.append(sim)
	for lem in syn.lemma_names