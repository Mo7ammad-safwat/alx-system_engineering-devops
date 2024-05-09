#!/usr/bin/python3
"""
This module provides a function to fetch the number of subscribers for a specified subreddit using the Reddit API.
If the subreddit does not exist or the API request fails, it returns 0.
"""

import requests

def number_of_subscribers(subreddit):
    """
    Fetch the number of subscribers to a subreddit.
    
    Args:
    subreddit (str): The name of the subreddit.
    
    Returns:
    int: The number of subscribers, or 0 if the subreddit doesn't exist.
    """
    url = f'https://www.reddit.com/r/{subreddit}/about.json'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code == 200:
        try:
            data = response.json()
            return data['data']['subscribers']
        except KeyError:
            return 0
    return 0

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        print("{:d}".format(number_of_subscribers(sys.argv[1])))
