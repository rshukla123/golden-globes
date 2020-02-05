import nltk
import sys
from src import helpers
from nltk.tokenize import TweetTokenizer as tokenizer

def main(tweets, award, sw, is_person):
	if 'cecil' in award:
		return []

	nominee_candidates = {}
	nominee_sw = ['nominee', 'nominated', 'nomination', 'nominate', 'nominees', 'nominations']

	if is_person:
		low, high = 2, 3
	else:
		low, high = 1, 6
	tkn_award = tokenizer().tokenize(award)

	for tweet in tweets:
		trash = True
		lower_tweet = [x.lower() for x in tweet]
		if any([s in tweet for s in nominee_sw]):
			clean_tweet = [tkn for tkn in lower_tweet if all([tkn not in stop for stop in [sw, nominee_sw, tkn_award]])]
			for i in range(low, high):
				for phrase in helpers.ngrams(clean_tweet, i):
					name = ' '.join(phrase)
					if name in award:
						continue
					if name in nominee_candidates:
						nominee_candidates[name] += 1
					else:
						nominee_candidates[name] = 1

	rankings = [(name, v) for name, v in sorted(nominee_candidates.items(), key=lambda item: item[1])]
	rankings.reverse()
	nominees = [n[0] for n in rankings[:6]]

	return nominees