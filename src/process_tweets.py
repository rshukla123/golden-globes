import sys
import json
from src.queries import query_winner, query_nominees, query_presenters

def main(year, award_tweets, sw):
	print('\nProcessing tweets...')
	results = {}

	for n, award in enumerate(award_tweets):
		prog = int(20*(n/len(award_tweets)))
		print('\r|' + prog*'=' + (20-prog)*' ' + '|', end='')

		is_person = any([title in award for title in ['actor', 'actress', 'director', 'screenplay', 'original', 'cecil']])

		tweets = award_tweets[award]
		winner = query_winner.main(tweets, award, sw, is_person)
		nominees = query_nominees.main(tweets, award, sw, is_person)
		if winner not in nominees: nominees.append(winner)
		presenters = query_presenters.main(tweets, nominees, award, sw)

		results[award] = {
			'winner': winner,
			'nominees': nominees,
			'presenters': presenters
		}
	print('\r|' + 20*'=' + '|')

	# for r in results:
	# 	print('%s:' % r)
	# 	for cat in results[r]:
	# 		if isinstance(results[r][cat], str):
	# 			print('\t%s:' % cat, results[r][cat])
	# 		else:
	# 			print('\t%s:' % cat, ', '.join(results[r][cat]))
	print('fuck')
	with open('results/partial_gg%s.json' % year, 'w+') as f:
		json.dump(results, f)
	f.close()