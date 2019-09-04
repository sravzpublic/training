#!/bin/bash
sudo {{python_version}} -m pip install virtualenvwrapper
sudo {{python_version}} -m pip install virtualenv
sudo chown -R {{ansible_user_id}}.{{ansible_user_id}} /home/{{ansible_user_id}}/.cache
# Add these to ~/.profile and then source the profile
export WORKON_HOME=/home/{{ansible_user_id}}/.virtualenvs
export PROJECT_HOME={{jobs_directory}}
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/{{python_version}}
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv -p {{python_version}} {{python_version}}
export VIRTUALENVWRAPPER_VIRTUALENV=/home/{{ansible_user_id}}/virtualenv
export PATH=/home/{{ansible_user_id}}/.virtualenvs/{{python_version}}/bin/python:$PATH
workon {{python_version}}
cd {{jobs_directory}}
setvirtualenvproject
/home/{{ansible_user_id}}/.virtualenvs/{{python_version}}/bin/python -m pip install -r /tmp/requirements.txt

