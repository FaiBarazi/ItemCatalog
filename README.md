# Movie Genre
A mini site that allows to add, Edit and Delete movies based on specific genre. The site requires a google login to edit content.

## Running the site, Pre-requests:
### Requirements:

- [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
- [Vagrant](https://www.vagrantup.com/downloads.html)
- python 3

###  Setup:
- Install VirtualBox to create a virtual database server on your machine.
- Install Vagrant which configures the VM and lets you share files between your host computer and the VM's filesystem.
- Download the [VM Setup](https://github.com/udacity/fullstack-nanodegree-vm) file from udacity for fast setup. 
- download the [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
- Save the ItemCatalog folder in the vagrant folder
- On the terminal go the directory of the VM Setup and run: 

```
$ vagrant up
```
```
$ vagrant ssh
```

## Running the Genre App
Once it is up and running, type **vagrant ssh**. This will log your terminal into the virtual machine, and you'll get a Linux shell prompt. When you want to log out, type **exit** at the shell prompt.  To turn the virtual machine off (without deleting anything), type **vagrant halt**. If you do this, you'll need to run **vagrant up** again before you can log into it.


Now that you have Vagrant up and running type **vagrant ssh** to log into your VM.  change to the /vagrant directory by typing **cd /vagrant**. This will take you to the shared folder between your virtual machine and host machine.

Type **ls** to ensure that you are inside the directory that contains main.py, database_setup.py, populateDB.py ..etc and two directories named 'templates' and 'static'

Now type **python3 database_setup.py** to initialize the database.

Type **python3 populateDB.py* to populate the database with genre and movies. (Optional)

Type **python main.py** to run the Flask web server. In your browser visit **http://0.0.0.0:5000** to view the genre list app.  You should be able to view, add, edit, and delete movies.
