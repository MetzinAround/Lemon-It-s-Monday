#!/usr/bin/env python3

from pathlib import Path
from random import choice

import tweepy

from config import get_settings

quotes = [
    "I want to go to there.",
    "Ain't no party like a Liz Lemon party 'cause a Liz Lemon party is mandatory.",
    "I'm a star, I'm on top, somebody bring me some ham.",
    "Can I share with you my worldview? All of humankind has one thing in common: the sandwich.",
    "I'm going to go talk to some food about this.",
    "Blurg.",
    "What the what?",
    "If reality TV has taught us anything, it's that you can't keep people with no shame down.",
    "High Fiving a Million Angels!",
    "I already have a drink... do you think he'd buy me mozarella sticks?",
    "Guess who's got two thumbs, speaks limited French, and hasn't cried once today? This moi.",
    "I'm going to the gym later, so I deserve a treat!",
]

TWEET_TEXT = choice(quotes)


def post_tweet():
    settings = get_settings()
    image_path = Path("lemonitsmonday.png")

    auth = tweepy.OAuth1UserHandler(
        settings["api_key"],
        settings["api_secret"],
        settings["access_token"],
        settings["access_token_secret"],
    )
    api = tweepy.API(auth, wait_on_rate_limit=True)
    api.verify_credentials()

    media = api.media_upload(filename=str(image_path))
    api.update_status(status=TWEET_TEXT, media_ids=[media.media_id])
    print("Tweet posted successfully")


if __name__ == "__main__":
    try:
        post_tweet()
    except Exception as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)
