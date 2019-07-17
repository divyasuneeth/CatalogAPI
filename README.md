# Description

This web application provides a list of items within a variety of categories and integrate third party user registration and authentication.
This is a RESTful web application created with Python 3 and the Python micro-framework Flask.
The app uses SQLite database that contains a catalog of items and associated information.
The database is created by running database_setup.py and initial data is populated by running itemsforcatalog.py
The main code is located in application.py
This app uses google for third party authentication.

## Usage
**Steps to run the APP:**

* Install Vagrant and VirtualBox
* Clone the catalog repo (https://github.com/divyasuneeth/CatalogAPI)
* Launch the Vagrant VM using **vagrant up** command followed by vagrant ssh
* navigate to the catalog folder on your vagrant machine
* run application.py

## How to navigate the APP:

The home page displays variety of categories, and a list of recently added items.
A list of items belonging to a category is displayed on selecting a category.
Further, on selecting an item, the description of the item is displayed.

__*User authentication is required to add an category or item .*__
After login, the user can also edit and delete an existing item.
