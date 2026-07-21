# Lemon-It-s-Monday
What a week, huh?

## X/Twitter posting bot
This repo now includes a Python script that can post the existing image (`lemonitsmonday.png`) to the X/Twitter account configured in `.env`.

### Setup
1. Install dependencies:
   `python3 -m pip install -r requirements.txt`
2. Fill in the values in `.env` (or copy `.env.example` to `.env` and edit it).
3. Run a safe dry run first:
   `python3 bot.py --dry-run`
4. When ready, post live:
   `python3 bot.py`

### Required X/Twitter credentials
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`

### Cron example for SparkedHost
To run the bot every Monday at 5:00 PM PT:

```bash
TZ=America/Los_Angeles
0 17 * * 1 /usr/bin/python3 /path/to/this/repo/bot.py >> /path/to/this/repo/bot.log 2>&1
```

If you want to avoid live posts during setup, keep `DRY_RUN=true` until the credentials are verified.
