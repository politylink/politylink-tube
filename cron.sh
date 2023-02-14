# crontab -e
# */30 * * * * /bin/zsh ~/politylink/politylink-press/cron.sh &> ~/politylink/politylink-press/out/cron/log/cron.log

set -ue

cd ~/politylink/politylink-press
poetry run python cron.py
