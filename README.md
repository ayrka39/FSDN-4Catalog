# FSND-04 Catalog Project

## Description

This is an Udacity project to develop a basic catalog app, using sqlite and Flask. 

## Requirements

* Python 2.7 or above
* SQLite
* SQLAlchemy
* Flask
* Python libraries: httplib2, requests, json, oauth2client
* additionally you need a "client-secrets.json" file from Google developers console.
  
## Set Up

Install [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/)

Clone the files in this repo to a local machine.

## Usage

Go to the folder where the files are and launch VM as follows
```
vagrant up
```
```
vagrant ssh
```

Once logged in, type
```
cd /vagrant/yourfolder (where cloned files are located)
```


Run three python files one by one 
```
python database_setup.py
```
```
python database_init.py
```
```
python application.py
```
Open your browser and check the app at
```
http://127.0.0.1:5000
```
