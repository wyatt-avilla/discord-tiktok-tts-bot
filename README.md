# Invite link
- Not currently public. If you're interested, feel free to reach out and I'll probably give you access.

# Functionality
- `/tts` plays the given text in the chosen voice
- `/join` joins your voice channel
- `/leave` disconnects the bot if it's in a voice channel

# Credit
Uses the same API as [this](https://github.com/Weilbyte/tiktok-tts) repo

# File Descriptions
- `sensitive.py` houses discord bot token
- `json-request.py` responsible for requesting base64 audio conversion
- `bot.py` core bot functionality

# Dependencies

## Python
`pip install -U discord requests PyNaCl`

## OS

### Windows
- [Python 3.10+](https://www.python.org/downloads/)
- [FFmpeg](https://ffmpeg.org/) (with it added as a path environment variable)

### Ubuntu
`apt-get install python3 python3-pip python-dev-is-python3 build-essential libssl-dev libffi-dev ffmpeg`