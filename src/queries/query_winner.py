import sys
import nltk
from nltk.tokenize import TweetTokenizer as tokenizer
from src import helpers

def main(tweets, award, sw, is_person):
	winner_candidates = {}
	winner_sw = ['won', 'winner', 'winning', 'win', 'wins',
				 'recieve', 'recieves', 'recieving', 'recieved',
				 'congrats', 'congratulations',
				 'receives', 'received', 'receiving',
				 'honored', 'honoured',
				 'accepting', 'accepts', 'accepted',
				 'speech']
	tkn_award = [tkn.lower() for tkn in tokenizer().tokenize(award)]
	stops = winner_sw + tkn_award + sw

	if is_person:
		low, high = 2, 3
	else:
		low, high = 1, 4

	for tweet in tweets:
		lower_tweet = [tkn.lower() for tkn in tweet['clean']]
		if any([sw in lower_tweet for sw in winner_sw]):
			lower_raw = [tkn.lower() for tkn in tweet['raw']]
			clean_tweet = [tkn for tkn in lower_tweet if tkn not in stops]

			for i in range(low, high):
				for phrase in helpers.ngrams(clean_tweet, i):
					front = lower_raw.index(phrase[0])
					back = lower_raw.index(phrase[-1]) + 1
					# if is_person and back - front != i:
					# 	continue

					name = ' '.join(lower_raw[front:back])

					if name in winner_candidates:
						winner_candidates[name] += 1
					else:
						winner_candidates[name] = 1

	rankings = [(name, v) for name, v in sorted(winner_candidates.items(), key=lambda item: item[1])]
	rankings.reverse()
	if not len(rankings):
		return ''

	return rankings[0][0]
