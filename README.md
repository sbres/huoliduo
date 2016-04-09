# huoliduo_docker
Docker config for huoliduo stuff

Now let's get this shit started

We will use docker compose.
(install docker compose :v https://docs.docker.com/compose/install/ )
Just run:


For dev:

git clone or paste your repo

- git clone 
	git clone https://github.com/vplotton/perfectFood.git ./frontend/static_files/huoliduo
	Yeah the directory must be called huoliduo !

- copy
	go to ./frontend/static_files/ create a directory called huoliduo
	you shoud have ./frontend/static_files/huoliduo/app and ./frontend/static_files/huoliduo/bower
	Check it good plz !!!


Then run this:
docker-compose -f docker-compose.yml up

For prod run:

docker-compose -f production.yml up
(That's it no more touching)



Everything should be runing 

http://127.0.0.1/ Shoud go to the app

http://127.0.0.1:81/admin/index.html Shoud go to the web admin page

ATENTION: ssl is activated by default in localhost you will have errors !


Troubleshoting 

If the api is not working change the host on this file

	- frontend/static_files/scripts/models/Order.js

Arround line 22 - 26 


#########################################################
#														#
#			How to make an update on production 		#
#				(To test)								#
#########################################################


Example we want to run the newest version of the webapp

while everything is runing normaly we run:
	- docker-compose -f production.yml build --no-cache volume_github
	- docker-compose -f production.yml rm volume_github
	- docker-compose -f production.yml up --no-deps -d volume_github

