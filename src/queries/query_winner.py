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

	if is_person:
		low, high = 2, 3
	else:
		low, high = 1, 6

	for tweet in tweets:
		lower_tweet = [tkn.lower() for tkn in tweet]
		if any([sw in lower_tweet for sw in winner_sw]):
			clean_tweet = [tkn for tkn in lower_tweet if tkn not in winner_sw and tkn not in tkn_award and tkn not in sw]
			for i in range(low, high):
				for phrase in helpers.ngrams(clean_tweet, i):
					name = ' '.join(phrase)
					if name in winner_candidates:
						winner_candidates[name] += 1
					else:
						winner_candidates[name] = 1

	rankings = [(name, v) for name, v in sorted(winner_candidates.items(), key=lambda item: item[1])]
	rankings.reverse()
	if not len(rankings):
		return ''

	return rankings[0][0]
