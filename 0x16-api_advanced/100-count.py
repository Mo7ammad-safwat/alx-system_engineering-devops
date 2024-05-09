#!/usr/bin/python3
"""
This module contains a function 'count_words' that recursively fetches titles
from all hot posts of a subreddit and counts occurrences of specified keywords,
printing them in a specified sorted order. Keywords are counted case-insensitively
and punctuation is ignored.
"""

import requests
import re

def count_words(subreddit, word_list, counts=None, after=None):
    """
    Recursively counts keyword occurrences in subreddit hot post titles.

    Args:
    subreddit (str): The subreddit name.
    word_list (list): The list of keywords to count.
    counts (dict, optional): Accumulator for keyword counts.
    after (str, optional): 'after' marker for Reddit API pagination.
    """
    if counts is None:
        counts = {word.lower(): 0 for word in word_list}

    headers = {'User-Agent': 'Reddit Keyword Counter/0.1'}
    url = f'https://www.reddit.com/r/{subreddit}/hot.json?limit=100'
    if after:
        url += f"&after={after}"
    
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        if after is None:  # Only print nothing on the first call
            return
        else:
            print_results(counts)
            return

    data = response.json()
    posts = data.get('data', {}).get('children', [])
    if not posts and after is None:
        return

    for post in posts:
        title = post['data']['title'].lower()
        for word in counts:
            counts[word] += len(re.findall(r'\b{}\b'.format(re.escape(word)), title))

    after = data['data'].get('after', None)
    if after is not None:
        count_words(subreddit, word_list, counts, after)
    else:
        print_results(counts)

def print_results(counts):
    """
    Prints the keyword counts sorted by the count in descending order
    and alphabetically if counts are equal.
    """
    sorted_counts = sorted((count, word) for word, count in counts.items() if count > 0)
    sorted_counts.sort(reverse=True, key=lambda x: (x[0], -ord(x[1][0])))
    for count, word in sorted_counts:
        print(f"{word}: {count}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        count_words(sys.argv[1], [x for x in sys.argv[2].split()])
