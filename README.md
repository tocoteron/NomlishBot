# NomlishBot

Standalone bot that translates original tweets to Nomlish language.

## Getting started

### Requirements

- Python3
- pip
- Selenium
- BeautifulSoup 4
- Twitter API
- [geckodriver](https://github.com/mozilla/geckodriver/releases)

### Installation

If you have not registered for [Twitter Developers](https://developer.twitter.com/content/developer-twitter/ja.html), please register and get the API keys.

Install packages:

```
pip3 install selenium beautifulsoup4 twitter
```

You have to replace the strings in `config.py` with the API keys.

```python3
# Set your keys
ACCESS_TOKEN = 'Access token'
ACCESS_TOKEN_SECRET = 'Access token secret'
CONSUMER_KEY = 'Consumer API key'
CONSUMER_SECRET = 'Consumer API secret key'
```

### Usage

Run:
```
python3 nomlish_bot.py target_user_id
```

#### Example

If the target user id is '@abc1234', you run:

```
python3 nomlish_bot.py abc1234
```
