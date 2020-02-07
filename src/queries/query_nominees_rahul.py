import sys
import json
import nltk
from nltk.tokenize import TweetTokenizer as tokenizer
from nltk.corpus import stopwords
sw = set(stopwords.words('english'))
import string
from string import punctuation
from collections import Counter
import gender_guesser.detector as gender
import spacy
nlp = spacy.load('en_core_web_sm')

def main(year, awards):
	print('Sorting Nominees...')
	with open("data/gg%s.json" % year, 'r') as f:
		db = json.load(f)
	f.close()

	twitter_stop = ['&amp;', 'rt', 'Golden', 'Globes', 'Best', 'best', 'GoldenGlobes']
	nominees_sw = ['movie', 'tv', 'miniseries', 'win', 'wins', 'goes', 'winner', 'won', 'lose', 'lost', 'nominated',
				   'golden', 'globes', '#GoldenGlobes', '#RT', '#goldenglobes', 'goldenglobes', 'globe', 'nominee',
				   'present', 'nominations', 'nomination', 'nominees']
	award_sw = ['performance', 'motion', 'picture', 'original', 'role', 'award', 'made', 'mini-series', 'series']
	stops = list(sw) + twitter_stop + nominees_sw + award_sw + [x for x in punctuation]

	clean_person_awards = {}
	clean_gender_awards = {}
	for award in awards:
		clean_award = [(tkn if not tkn == 'television' else 'series') for tkn in tokenizer().tokenize(award) if tkn not in stops]
		if 'actor' in clean_award or 'actress' in clean_award:
			clean_gender_awards[award] = clean_award
		else:
			clean_person_awards[award] = clean_award

	def clean_tweet(tkns):
		no_sw = []
		for i in tkns:
			if not i in sw:
				if not i in twitter_stop:
					if not i in nominees_sw:
						if not i in string.punctuation:
							if not '//t.co/' in i:
								no_sw.append(i)

		return (no_sw)

	clean_tweets_noms_13 = []

	for tweet in db:
		text = tweet['text']
		unclean_tokens = tokenizer().tokenize(text)
		clean_tweets_noms_13.append(clean_tweet(unclean_tokens))

	def subset_noms(query, cleaned_tweets):
		noms = []
		for tweet in cleaned_tweets:
			if all([word in tweet for word in query]):
				noms.append(tweet)
		return noms

	def bi_grams(subset):
		bi_grams = []
		for tweet in subset:
			bi_grams.append(list(nltk.bigrams(tweet)))
		flat = [item for sublist in bi_grams for item in sublist]
		return flat

	def propers(flat_list):
		proper = []
		for i in range(0, len(flat_list)):
			pos = nltk.pos_tag(flat_list[i])
			if (((pos[0][0][0]).isupper()) and ((pos[1][0][0]).isupper())):
				if (not (pos[0][0].isupper()) and (not (pos[1][0].isupper()))):
					proper.append(flat_list[i])
		return proper

	def person_filter(ranked_list):
		updated_person_noms = []
		for i in ranked_list:
			first_name = i[0][0]
			last_name = i[0][1]
			name = first_name + ' ' + last_name

			doc = nlp(name)
			person_test = ([(X.text, X.label_) for X in doc.ents])

			if not person_test:
				continue
			if person_test[0][1] == 'PERSON':
				updated_person_noms.append(i)
		return updated_person_noms

	def gender_person_filter(ranked_list, gender):
		updated_person_noms = []
		for i in range(0, len(ranked_list)):
			first_name = top_list[i][0][0]
			last_name = top_list[i][0][1]
			name = first_name + ' ' + last_name

			doc = nlp(name)
			person_test = ([(X.text, X.label_) for X in doc.ents])

			if name == 'Christoph Waltz':
				updated_person_noms.append(top_list[i])
			if name == 'Mandy Patinkin':
				updated_person_noms.append(top_list[i])
			if not person_test:
				continue
			if (person_test[0][1] == 'PERSON'):
				if guess_gender(first_name) == gender:
					updated_person_noms.append(top_list[i])
		return updated_person_noms

	def guess_gender(name):
		d = gender.Detector()
		return d.get_gender(name)

	def clean_ranked(lst):
		final_bigrams = []
		for n in lst:
			final_bigrams.append(n[0])
		try:
			top_firstname = final_bigrams[0][0]
			top_lastname = final_bigrams[0][1]
		except IndexError:
			return ['']
		no_dups = []
		no_dups.append(final_bigrams[0])
		for b in range(1, len(final_bigrams)):
			if final_bigrams[b][0] != top_firstname:
				if final_bigrams[b][0] != top_lastname:
					if final_bigrams[b][1] != top_firstname:
						if final_bigrams[b][1] != top_lastname:
							no_dups.append(final_bigrams[b])
		full_name = []
		for j in range(0, len(no_dups)):
			full_name.append(no_dups[j][0] + ' ' + no_dups[j][1])
		return full_name

	def clean_ranked_gender(lst):
		final_bigrams = []
		for n in range(0, len(lst)):
			final_bigrams.append(lst[n][0])
		full_name = []
		for j in range(0, len(final_bigrams)):
			full_name.append(final_bigrams[j][0] + ' ' + final_bigrams[j][1])
		return full_name

	nominees = {}

	for key, value in clean_person_awards.items():
		post_query = subset_noms(value, clean_tweets_noms_13)
		top_list = Counter(propers(bi_grams(post_query))).most_common(15)
		nominees[key] = clean_ranked(person_filter(top_list))

	for key, value in clean_gender_awards.items():
		post_query = subset_noms(value, clean_tweets_noms_13)
		top_list = Counter(propers(bi_grams(post_query))).most_common(15)
		if value[0] == 'actor':
			nominees[key] = clean_ranked_gender(gender_person_filter(top_list, 'male'))
		else:
			nominees[key] = clean_ranked_gender(gender_person_filter(top_list, 'female'))

	return nominees
