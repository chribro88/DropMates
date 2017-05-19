# DropMates

**No instagram API key required**

Analyse those who you follow and those that follow you on instagram
unfollow those who haven't followed you back. 

This is a tool that provides you a full list of instagram followers, along with those you follow. 
It also lets you see which users you follow but don't follow you back. 
Support for automatically unfollowing those users is provided.

### Installation
```
git clone https://github.com/mihalea/dropmates
cd frienddropper
virtualenv env
source env/bin/activate
pip install requests
pip install 'requests[security]'
cp config_sample.json config.json
python dropmates.py
```

### Usage
```
usage: dropmates.py [-h] [-u USERNAME] [-p PASSWORD] [-c CONFIG] [-r] [-x]
                    [-v] [-i] (-f | -o | -s | -a)

Analyze and process instagram followers

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Instagram username
  -p PASSWORD, --password PASSWORD
                        Instagram password
  -c CONFIG, --config CONFIG
                        Application config file
  -r, --rebuild         Rebuild the user cache from the web
  -x, --verified        Filter by hiding verified users
  -v, --verbose         Verbose logging
  -i, --interactive     Interactive unfollowing
  -f, --followers       Show your followers
  -o, --following       Show the user that you follow
  -s, --shame           Show those users that don't follow you back
  -a, --auto            Automatically unfollow those users that don't follow
                        you back

example:

  # Show users who follow you and are not verified
  dropmates.py -c config.json -fx

  # Show users who don't follow you back, with debug messages
  dropmates.py -u username -p password -svv

  # Ignore local cache and automatically unfollow users, providing a UI for selecting which users
  dropmates.py -c config -ai
```
### Maximum rates
Please keep this in mind this maximum action rates in order to avoid getting banned!
- Likes: 1000 daily, 500 hourly
- Unfollow: 330 daily, 65 hourly
