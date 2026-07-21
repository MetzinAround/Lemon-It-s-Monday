#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import tweepy

from config import get_config, require_config

lemon = [
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
    "I'm going to the gym later, so I deserve a treat!"]

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Post the repo image to X/Twitter")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config and media file without making a live post",
    )
    parser.add_argument("--image", dest="image_path", help="Override the image path")
    return parser.parse_args()


def build_api(config: dict[str, Any]) -> tweepy.API:
    auth = tweepy.OAuth1UserHandler(
        config["twitter_api_key"],
        config["twitter_api_secret"],
        config["twitter_access_token"],
        config["twitter_access_token_secret"],
    )
    return tweepy.API(auth, wait_on_rate_limit=True)


def post_tweet(config: dict[str, Any], dry_run: bool = False) -> dict[str, Any] | None:
    image_path = Path(config["image_path"]).expanduser().resolve()
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if dry_run:
        print(f"[dry-run] would post to @{config['twitter_username']}")
        print(f"[dry-run] text: {config['tweet_text']}")
        print(f"[dry-run] image: {image_path}")
        return None

    api = build_api(config)
    media = api.media_upload(filename=str(image_path))
    tweet = api.update_status(status=config["tweet_text"], media_ids=[media.media_id])
    print(f"Posted tweet id {tweet.id}")
    return {"id": tweet.id, "text": tweet.text}


def main() -> int:
    args = parse_args()
    config = get_config()
    if args.tweet_text:
        config["tweet_text"] = args.tweet_text
    if args.image_path:
        config["image_path"] = args.image_path

    if args.dry_run:
        try:
            post_tweet(config, dry_run=True)
        except Exception as exc:  # pragma: no cover - CLI safety net
            print(f"Dry run failed: {exc}")
            return 1
        return 0

    try:
        config = require_config()
    except RuntimeError as exc:
        print(str(exc))
        return 2

    try:
        post_tweet(config, dry_run=False)
    except Exception as exc:  # pragma: no cover - CLI safety net
        print(f"Failed to post tweet: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
