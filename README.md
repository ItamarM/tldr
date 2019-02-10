# [OUTDATED] Automatic channel summarizer bot for Slack

A simple slack chat bot to summarize a channel content for you (TL;DR).

## Installation
```sh
pip install slackbot
pip install nltk
pip install breadability
pip install docopt
pip install requests
```

## Usage

### Generate the slack api token

First you need to get the slack api token for your bot. You have two options:

1. If you use a [bot user integration](https://api.slack.com/bot-users) of slack, you can get the api token on the integration page.
2. If you use a real slack user, you can generate an api token on [slack web api page](https://api.slack.com/web).

### Configure the api token
You need to configure the `API_TOKEN` in a python module `tldr.py` and `test_slacker.py`.

#### Run the bot
```sh
cd src
make run
```

## TODO
- Use env variables correctly (For slack token + Slacker)
- See minor TODO(s) in the `tldr.py`
