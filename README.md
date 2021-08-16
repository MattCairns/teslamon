# Teslamon
Monitor the tesla inventory and push a notifcation to pushover if there are new vehicles.

[![NPM Version][npm-image]][npm-url]
[![Build Status][travis-image]][travis-url]
[![Downloads Stats][npm-downloads]][npm-url]

## Installation

Rename config_example.yml to config.yml and enter your details then execute:

```sh
docker-compose build
docker-compose up
```


## Pushover
To use pushover you need a user key and a api key.  Create a pushover account, your user key is located at the homepage (https://pushover.net/) and you can create an API key at https://pushover.net/apps/build 

Enter these details in config.yml and you're good to go.
