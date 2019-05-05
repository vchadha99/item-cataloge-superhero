SUPERHERO Catalogue WEB APPLICATION

This project is made for the Udacity FullStack Course.
This will help you to manage all powers of superhero which will particularly be displayed under their respective SUPERHERO.

.......................................................

Explanation of the contents of files:
=> This projects main file is project.py
=> The SQL database is stored in database_setup.py
=> The initial data is entered already in superhero.py
=> All the templates used in this project are stored in Templates folder.
=> The background image  is available in static folder.

.......................................................

PREREQUISITES:
=> Python
=> HTML
=> CSS
=> Flask
=> Postgresql
=> JSON
=> Vagrant 
.......................................................

How To Run:

=> Launch the Vagrant VM from inside the vagrant folder with:
=> vagrant up
=> vagrant ssh
=> Then move inside the itemvarun folder:
=> cd /vagrant / itemvarun
=> Then run the main file:
=> python project.py
=> After this command you are able to run the full flegded application at the URL:
=>  http://localhost:5000/

.......................................................


JSON:

The following are open to the public:

 /heros/JSON - Return JSON for all the heros

 /heros/<int:hero_id>/JSON - Return JSON of all the powers for a hero

 /heros/<int:hero_id>/<int:power_id>/JSON - Return JSON for a power