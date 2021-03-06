# set-up reference for Ubuntu 14.04

# install required programs.
sudo apt-get install git
sudo apt-get install sqlite3
sudo apt-get install python-pip
sudo pip install virtualenv

# set-up github.
ssh-keygen -t rsa -C $EMAIL
ssh-add ~/.ssh/id_rsa
# add `~/.ssh/id_rsa.pub` to github
ssh -T git@github.com
git clone git@github.com:zvxr/lc_commons
git config --global user.email $EMAIL
git config --global user.name $USERNAME

# set-up virtual environment
cd lc_commons
virtualenv venv
source venv/bin/activate
pip install mock
pip install requests==2.5.3
pip install python-dateutil
## add to venv/bin/activate:
## export PYTHONPATH="/path/to/lc_commons"

# make database.
sqlite3 lc_commons.db < assets/db_schema.sql
