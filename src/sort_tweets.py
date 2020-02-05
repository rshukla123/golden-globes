import sys
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer as tokenizer

def only_in_one(synonyms, l1, l2):
	check1 = False
	check2 = False
	for word in synonyms:
		check1 = check1 or word in l1
		check2 = check2 or word in l2
	return check1 != check2

def scrub_award(award):
	english_stop = set(stopwords.words('english'))
	gg_stop = ['best', 'performance', 'motion', 'picture', 'made', 'original']

	tknzed = tokenizer().tokenize(award)
	clean_award = []
	for tkn in tknzed:
		if not any([tkn in stop for stop in [english_stop, gg_stop]]) and tkn.isalpha():
			clean_award.append(tkn)
	return clean_award

def main(year, awards):
	print('\nLoading tweets...')
	with open('data/clean_gg%s.json' % year, 'r') as f:
		data = json.load(f)
	f.close()

	award_tweets = {}
	for award in awards:
		award_tweets[award] = []

	clean_awards = {}
	for award in awards:
		clean_awards[award] = scrub_award(award)

	required_words = [['actor'], ['actress'], ['supporting'], ['tv', 'television'], ['drama'], ['comedy', 'musical']]

	print('\nSorting tweets...')
	for tweet in data:
		lower_tweet = set(map(lambda x: x.lower(), tweet))
		sorted = False
		for award in awards:
			clean_award = clean_awards[award]
			if len(lower_tweet.intersection(set(clean_award))) / len(clean_awards[award]) >= 0.5:
				if any([only_in_one(word, clean_award, lower_tweet) for word in required_words]):
					continue
				award_tweets[award].append(tweet)

	return award_tweets
