# crontab -e
# */30 * * * * /bin/zsh ~/politylink/politylink-press/cron.sh &> ~/politylink/politylink-press/out/cron/log/cron.log

set -ue

# load NVM for gatsby
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

cd ~/politylink/politylink-press
poetry run python cron.py # make sure to add poetry path in .zshenv
