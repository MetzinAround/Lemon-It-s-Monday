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

TWEET_TEXT = f"'{choice(quotes)}' - Liz Lemon. #automated"


def post_tweet():
    settings = get_settings()
    image_path = Path(__file__).resolve().with_name("lemonitsmonday.png")

    auth = tweepy.OAuth1UserHandler(
        settings["api_key"],
        settings["api_secret"],
        settings["access_token"],
        settings["access_token_secret"],
    )
    api = tweepy.API(auth, wait_on_rate_limit=True)
    client = tweepy.Client(
        consumer_key=settings["api_key"],
        consumer_secret=settings["api_secret"],
        access_token=settings["access_token"],
        access_token_secret=settings["access_token_secret"],
        wait_on_rate_limit=True,
    )

    print("Checking credentials...")
    user = api.verify_credentials()
    print(f"Authenticated as @{user.screen_name}")

    print(f"Uploading media from {image_path}...")
    media = api.media_upload(filename=str(image_path))

    print("Posting tweet via X API v2...")
    response = client.create_tweet(text=TWEET_TEXT, media_ids=[media.media_id])
    print(f"Tweet posted successfully: {response.data['id']}")


if __name__ == "__main__":
    try:
        post_tweet()
    except Exception as exc:
        print(f"Error: {exc}")
        if hasattr(exc, "response") and exc.response is not None:
            print(f"HTTP status: {exc.response.status_code}")
            print(f"Response body: {exc.response.text}")
        print("This usually means the app is authenticated, but X is rejecting the write request because the app/account has no remaining API credits or does not have a posting tier enabled.")
        raise SystemExit(1)
