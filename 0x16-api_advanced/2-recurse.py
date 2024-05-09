#!/usr/bin/python3
"""
This module contains a function 'recurse' that recursively fetches and returns 
all hot post titles from a specified subreddit using the Reddit API. 
It returns None if the subreddit is invalid or no posts are found.
"""

import requests

def recurse(subreddit, hot_list=None, after=None):
    """Recursively fetches titles of all hot articles from a given subreddit."""
    if hot_list is None:
        hot_list = []
    
    headers = {'User-Agent': 'Reddit Post Fetcher/0.1'}
    url = f'https://www.reddit.com/r/{subreddit}/hot.json?limit=100'
    if after:
        url += f"&after={after}"
    
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        return None

    data = response.json()
    posts = data.get('data', {}).get('children', [])
    if not posts:
        return None if not hot_list else hot_list
    
    hot_list.extend(post['data']['title'] for post in posts)
    after = data['data'].get('after', None)
    if after is not None:
        return recurse(subreddit, hot_list, after)
    return hot_list

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        result = recurse(sys.argv[1])
        if result is not None:
            print(len(result))
        else:
            print("None")
