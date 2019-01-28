#!/bin/bash
twitterscraper 😄 -p 150 --begindate 2017-04-08 --enddate 2018-01-28 --lang ja -o happy.json &
twitterscraper 😢 -p 150 --begindate 2017-04-08 --enddate 2018-01-28 --lang ja -o sad.json &
twitterscraper 😠 -p 150 --begindate 2017-04-08 --enddate 2018-01-28 --lang ja -o angry.json &
twitterscraper 🤢  -p 150 --begindate 2017-04-08 --enddate 2018-01-28 --lang ja -o disgust.json &
twitterscraper 😨 -p 150 --begindate 2017-04-08 --enddate 2018-01-28 --lang ja -o fear.json &
twitterscraper 😲 -p 150 --begindate 2017-04-08 --enddate 2018-01-28 --lang ja -o surprise.json &

wait;

echo "Done!:twitterscraper"
