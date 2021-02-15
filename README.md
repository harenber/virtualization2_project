# virtualization2_project
In this repo we'll have the code we develop for the Virtualization2 Project:

Implement webserver to solve the 3-Body problem using a RK method and show the results graphycally in a containerized manner.

Right now works with docker-compose  the docker compose file is in compose folder. Simply Run docker-compose up and then visit https://localhost:8123/
-------------------------------------------------------------------------------------------------------------------------------------------------------

To test without docker compose, do:
sudo docker network create project_network

YOu'll need three terminals or run in detatch mode:

Then:
in  virtualization2_project/backend/server
sudo docker build -t my_server .
sudo docker run --rm  -v "$(pwd)":/server --network=project_network --name project_server my_server

Then, do:
in virtualization2_project/build/frontend_container
sudo docker build -t frontend .
sudo docker run --rm -it --network=project_network -p 8123:8000 frontend


then do:
in virtualization2_project/solver_test
sudo docker build -t solver .
sudo docker run -v ~/Documents/virtualization2_project/backend/server:/solver --rm --network=project_network --name=solver solver



Open your broswer and go to http://0.0.0.0:8123/

side note: 

using -v: Consists of three fields, separated by colon characters (:). The fields must be in the correct order, and the meaning of each field is not immediately obvious.
In the case of named volumes, the first field is the name of the volume, and is unique on a given host machine. For anonymous volumes, the first field is omitted.
The second field is the path where the file or directory are mounted in the container.
Source:https://docs.docker.com/storage/volumes/

--You might have to change the address if you save folder in diffrent location.
