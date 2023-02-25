# crontab -e
# */30 * * * * /bin/zsh ~/politylink/politylink-tube/builder/cron.sh &> ~/politylink/politylink-tube/builder/out/cron/log/cron.log

set -ue

# load NVM for gatsby
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

cd ~/politylink/politylink-tube/builder
poetry run python cron.py # make sure to add poetry path in .zshenv
