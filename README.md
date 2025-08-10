# DreamsMusic

Delivering Superior Music Experience to Telegram.

## Commands List

| Command        | Description                                      |
|----------------|------------------------------------------------|
| `/start`       | Check if the bot is alive and running           |
| `/play`        | Play a song or playlist in the voice chat       |
| `/pause`       | Pause the currently playing music                |
| `/resume`      | Resume paused music                              |
| `/stop`        | Stop music playback and leave the voice chat    |
| `/skip`        | Skip the current song and play the next in queue|
| `/restart`     | Restart the music player or bot                   |
| `/queue`       | Show the current music queue                      |
| `/song`        | Get details about the currently playing song     |
| `/seek`        | Seek to a specific position in the current song |
| `/speed`       | Adjust playback speed (e.g., slow, normal, fast) |
| `/loop`        | Toggle loop mode for current song or queue       |
| `/playlist`    | Manage your saved playlists (add, delete, view)  |
| `/stats`       | View bot usage statistics and current sessions   |
| `/maintenance` | Enable or disable maintenance mode                |
| `/logger`      | Enable or disable logging of bot events           |
| `/settings`    | Adjust playback and bot behavior settings         |
| `/language`    | Change the bot's language (English, Hindi, etc.) |
| `/auth`        | Authorize users to control the bot                |
| `/unauth`      | Remove user authorization                          |
| `/authusers`   | List all authorized users                          |
| `/broadcast`  | Send a message to all users                        |
| `/help`        | Show this help message with commands               |

---

**Note:**  
- Commands like `/play` accept URLs, song names, or playlist links.  
- Admin commands like `/auth`, `/maintenance`, `/logger` require proper permissions.  
- The bot supports multi-language commands, currently English and Hindi.



## Deploy

Click any button below to deploy DreamsMusic instantly on your preferred platform:

[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/DreamsRobot/DreamsMusic)

[![Deploy on Render](https://render.com/images/deploy-to-render-button.svg)](https://dashboard.render.com/deploy?repo=https://github.com/DreamsRobot/DreamsMusic)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/DreamsRobot/DreamsMusic)


---

# DreamsMusic Telegram Music Bot

A Telegram Music Bot with assistant user (string session) for joining voice chats and streaming music — no YouTube API or cookies needed.

## Features

- Plays music in voice chats via assistant user account (string session)  
- Play, pause, resume, stop, skip, end commands  
- Playlist management commands  
- Welcome messages  
- Multi-language support (English & Hindi)  
- Maintenance mode toggle  
- Logger enable/disable  
- Stats command including playlist and user stats  
- Playback control settings for admins or everyone  
- User authorization mode with auth commands  
- Public open-source code for community use and contributions made by CFCBots

---

## VPS Setup Guide

Follow these steps to set up and run DreamsMusic on your VPS.

```bash
sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install python3-pip ffmpeg git -y

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
source ~/.bashrc
nvm install v18

git clone https://github.com/DreamsRobot/DreamsMusic.git
cd DreamsMusic

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

cp sample.env .env

vi .env

sudo apt install tmux -y
tmux

python3 main.py
```

## Special Thanks 🙏

[![CFCBots](https://img.shields.io/badge/CFCBots-%231DA1F2.svg?style=for-the-badge&logo=telegram&logoColor=white&animation=fade)](https://t.me/CFCBots)  
[![CloseFriendsCommunity](https://img.shields.io/badge/CloseFriendsCommunity-%231DA1F2.svg?style=for-the-badge&logo=telegram&logoColor=white&animation=fade)](https://t.me/CloseFriends/community)

---

*Made with ❤️ and ☕ by DreamsMusic Team*
