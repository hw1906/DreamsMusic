# DreamsMusic

Delivering Superior Music Experience to Telegram.

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
