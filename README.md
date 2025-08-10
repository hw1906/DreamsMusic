# DreamsMusic  
Delivering Superior Music Experience to Telegram.

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
