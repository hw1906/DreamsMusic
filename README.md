# DreamsMusic
Delivering Superior Music Experience to Telegram.

# DreamsMusic Telegram Music Bot

A Telegram Music Bot with assistant user (string session) for joining voice chats and streaming music — no YouTube API or cookies needed.

## Features

- Plays music in voice chats via assistant user account (string session)
- Play, pause, resume, stop, skip, end commands
- Welcome messages
- Multi-language support (English & Hindi)
- Maintenance mode toggle
- Logger enable/disable
- Stats command
- Playback control settings for admins or everyone

## Setup

1. Clone this repo

# VPS SETUP
# 1. Upgrade & Update your system packages
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install required packages
sudo apt-get install python3-pip ffmpeg git -y

# 3. (Optional) Upgrade pip inside your system (recommended to use venv instead)
# sudo pip3 install --upgrade pip

# 4. Install Node.js (using nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
source ~/.bashrc
nvm install v18

# 5. Clone your DreamsMusic repository and enter folder
git clone https://github.com/DreamsRobot/DreamsMusic.git
cd DreamsMusic

# 6. Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 7. Install Python dependencies from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# 8. Create your .env file from the sample
cp sample.env .env

# 9. Edit .env to add your configuration values
vi .env
# (Press i to edit, enter values, then Esc and :wq to save)

# 10. Install tmux and start a session (optional)
sudo apt install tmux -y
tmux

# 11. Run your bot
bash start
# or if no start script,
# python3 main.py
