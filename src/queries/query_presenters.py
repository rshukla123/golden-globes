import sys
import nltk
from src import helpers
from nltk.tokenize import TweetTokenizer as tokenizer

def main(tweets, nominees, award, sw):
	presenter_candidates = {}
	presenter_sw = ['present', 'presenter', 'presentation', 'presenting', 'presenta', 'presents',
					'introduce', 'introduced', 'introducing',
					'hand', 'hands', 'handing']
	tkn_award = tokenizer().tokenize(award)

	for tweet in tweets:
		lower_tweet = [x.lower() for x in tweet['clean']]
		if any([s in lower_tweet for s in presenter_sw]):
			lower_raw = [tkn.lower() for tkn in tweet['raw']]
			clean_tweet = [tkn for tkn in lower_tweet if all([tkn not in stop for stop in [sw, presenter_sw, tkn_award]])]

			for i in range(2, 3):
				for phrase in helpers.ngrams(clean_tweet, i):
					front = lower_raw.index(phrase[0])
					back = lower_raw.index(phrase[-1]) + 1
					if back - front != i:
						continue

					name = ' '.join(lower_raw[front:back])

					if name in nominees or name in award:
						continue
					if name in presenter_candidates:
						presenter_candidates[name] += 1
					else:
						presenter_candidates[name] = 1

	rankings = [name for name, v in sorted(presenter_candidates.items(), key=lambda item: item[1])]
	rankings.reverse()

	if not len(rankings):
		return ''

	return rankings[0]
