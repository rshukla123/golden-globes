import sys
import re
import json
import nltk
from nltk.tokenize import TweetTokenizer as tokenizer
from nltk.corpus import stopwords
from string import punctuation

def clean_tweet(tkns):
	# test
	english_stop = set(stopwords.words('english'))
	gg_stop = ['best', 'goldenglobes', '#goldenglobes', '#goldenglobe', 'golden', 'globes', 'globe']
	twitter_stop = ['&amp;', 'rt']
	stops = [english_stop, gg_stop, twitter_stop, punctuation]

	clean_tokens = []

	for tkn in tkns:
		if not any([tkn.lower() in stop for stop in stops]) and \
				not '//t.co/' in tkn and \
				re.fullmatch(r'''[a-zA-Z0-9-'#@]+''', tkn):
			clean_tokens.append(tkn)

	return clean_tokens

def main(year):
	print('Importing %s tweets...' % year)
	with open('data/gg' + year + '.json', 'r') as f:
		db = json.load(f)
	f.close()

	print('Cleaning tweets...')
	clean_tweets = [clean_tweet(tokenizer().tokenize(tweet['text'])) for tweet in db]

	print('Saving cleaned tweets...')
	with open('data/clean_gg' + year + '.json', 'w+') as clean_file:
		json.dump(clean_tweets, clean_file)
	clean_file.close()
