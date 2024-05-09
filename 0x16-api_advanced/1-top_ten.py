#!/usr/bin/python3
"""
Module to fetch and print titles of the top ten hot posts from a subreddit.
If the subreddit is invalid or non-existent, it prints None.
"""

import requests

def top_ten(subreddit):
    """
    Prints the titles of the top ten hot posts from a subreddit.

    Args:
    subreddit (str): The subreddit name.
    """
    url = f'https://www.reddit.com/r/{subreddit}/hot.json?limit=10'
    headers = {'User-Agent': 'Mozilla/5.0 (Ubuntu; Linux x86_64)'}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code == 200:
        data = response.json()
        posts = data.get('data', {}).get('children', [])
        if not posts:
            print(None)
        for post in posts:
            print(post['data']['title'])
    else:
        print(None)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        top_ten(sys.argv[1])
