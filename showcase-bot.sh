#!/bin/bash
cd /home/bot/metadata-bot/showcase
while :
do
        source ../venv/bin/activate
	echo "loading"
        python3 ./showcase-bot.py
done
