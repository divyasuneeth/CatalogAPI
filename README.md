# Sports Catalog App

<a href="https://www.udacity.com/">
  <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo svg">
</a>

Udacity Full Stack Web Developer Nanodegree program


## Description
This is a RESTful web application created with Python 3 and the Python micro-framework Flask.

* The web application provides a list of items within a variety of categories
* uses third party user registration and authentication.
* app uses SQLite database that contains a catalog of items and associated information.
* Front-end forms and webpages built with Boostrap


## Usage
**Steps to run the APP:**

* Clone the [catalog repo](https://github.com/divyasuneeth/CatalogAPI)
* Install Vagrant and VirtualBox

* Launch the Vagrant VM using
** `$ vagrant up`**

* Once it is up and running, type
 **`$ vagrant ssh`**   
   * This will log your terminal into the virtual machine, and you'll get a Linux shell prompt. When you want to log out, type **`$ exit`** at the shell prompt.  To turn the virtual machine off (without deleting anything), type **`$ vagrant halt`**. If you do this, you'll need to run **`$ vagrant up`** again before you can log into it.

* navigate to the catalog folder on your vagrant machine by changing to /vagrant directory
**`$ cd /vagrant`**.
   * This will take you to the shared folder between your virtual machine and host machine.
   * Type **ls** to ensure that you are inside the directory that contains application.py, database_setup.py, and two directories named 'templates' and 'static'

* Install modules in requirements.txt
**`pip  install  -r  requirements.txt`**

* Now to initialize the database.
**`$ python database_setup.py`**

* Type to populate the database with category and items(Optional).
**`$ python itemsforcatalog.py`**  

* to run the Flask web server.
**`$ python application.py`**

* To view the Catalog app in your browser visit
**`http://localhost:8000 `**


## How to navigate the APP:

* The home page displays variety of categories, and a list of recently added items.

* A list of items belonging to a category is displayed on selecting a category.

* Further, on selecting an item, the description of the item is displayed.

__*User authentication is required to add an category or item .*__
After login, the user can also edit and delete an existing item.
