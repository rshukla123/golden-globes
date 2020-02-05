import sys
import json
from src import helpers
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer as tokenizer
from string import punctuation

def main(year):
	print('\nSearching for awards...')

	# Import twitter data
	with open('data/gg%s.json' % year, 'r') as f:
		data = json.load(f)
	f.close()

	# Generate a list of all stopwords
	punc = ''.split(punctuation)
	english_stop = stopwords.words('english')
	gg_stop = ['goldenglobes', '#goldenglobes', '#goldenglobe', 'golden', 'globes', 'globe']
	twitter_stop = ['&amp;', 'rt']
	stops = set(english_stop + gg_stop + twitter_stop + punc)

	award_candidates = {}

	size = len(set([d['text'] for d in data]))

	for n, tweet in enumerate(set([d['text'] for d in data])):
		helpers.prog_print(n, size)

		# Generate all relevant forms of the tweet
		tkn_tweet = tokenizer().tokenize(tweet)
		lower_tweet = [tkn.lower() for tkn in tkn_tweet]
		clean_tweet = [x for x in lower_tweet]
		for sw in set(clean_tweet).intersection(stops):
			clean_tweet.remove(sw)

		if 'best' in clean_tweet:
			tagged_tweet = nltk.pos_tag(clean_tweet)
			for i in range(2, 8):
				ind = clean_tweet.index('best')

				# If we hit the end of the tweet or the last word in the segment isn't a noun, we don't need to look at it
				if ind + i > len(clean_tweet):
					break
				if 'NN' not in tagged_tweet[ind+i-1]:
					continue

				# Find the segment in the uncut tweet, so we have the stopwords
				front, back = lower_tweet.index('best'), lower_tweet.index(clean_tweet[ind+i-1])

				# Piece it together and add it to the candidates list
				name = ' '.join(lower_tweet[front:back+1])
				if name in award_candidates:
					award_candidates[name] += 1
				else:
					award_candidates[name] = 1

	# Sort dict by number of appearances
	rankings = [(name, v) for name, v in sorted(award_candidates.items(), key=lambda item: item[1])]
	rankings.reverse()

	return [i[0] for i in rankings if i[1] > 80 and i[0]]