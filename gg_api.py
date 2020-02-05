import os
import sys
import json

from src import clean_tweets, sort_tweets, query_hosts, query_awards, process_tweets

'''Version 0.35'''

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    hosts = query_hosts.main(year)
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    awards = query_awards.main(year)
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    with open('results/partial_gg%s.json' % year, 'r') as f:
        data = json.load(f)
    f.close()

    nominees = {}
    for award in data:
        if award == 'hosts':
            continue
        nominees[award] = data[award]['nominees']
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    with open('results/partial_gg%s.json' % year, 'r') as f:
        data = json.load(f)
    f.close()

    winners = {}
    for award in data:
        if award == 'hosts':
            continue
        winners[award] = data[award]['winner']
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    with open('results/partial_gg%s.json' % year, 'r') as f:
        data = json.load(f)
    f.close()

    presenters = {}
    for award in data:
        if award == 'hosts':
            continue
        presenters[award] = data[award]['presenters']
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    print('Beginning pre-ceremony queries...')

    for year in ['2013']:
        if not os.path.exists('data/clean_gg' + year + '.lst'):
            clean_tweets.main(year)

    print('Pre-ceremony queries complete')
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    year = sys.argv[1]

    hosts = get_hosts(year)
    print('\nHost(s):', ', '.join(hosts))

    awards = get_awards(year)
    print('\nAwards:\n\t', '\n\t'.join(awards), '\n')

    sorted_path = 'data/sorted_gg%s.json' % year
    if os.path.exists(sorted_path):
        with open(sorted_path, 'r') as f:
            award_tweets = json.load(f)
        f.close()
    else:
        award_tweets = sort_tweets.main(year, OFFICIAL_AWARDS_1315)
        with open(sorted_path, 'w+') as f:
            json.dump(award_tweets, f)
        f.close()

    gg_sw = []
    sw = ['actor', 'actress', 'tv', 'television', 'series', 'film', 'comedy', 'drama', 'director']

    process_tweets.main(year, award_tweets, sw)

    show = {
        'hosts': hosts,
        'awards': awards
    }

    winners = get_winner(year)
    nominees = get_nominees(year)
    presenters = get_presenters(year)

    for award in award_tweets:
        show[award] = {
            'winner': winners[award],
            'nominees': nominees[award],
            'presenters': presenters[award]
        }

    with open('results/gg' + year + '.json', 'w+') as f:
        json.dump(show, f)
    f.close()

if __name__ == '__main__':
    # pre_ceremony()
    main()
