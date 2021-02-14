# virtualization2_project
In this repo we'll have the code we develop for the Virtualization2 Project:

Implement webserver to solve the 3-Body problem using a RK method and show the results graphycally in a containerized manner.


To test, do:
in virtualization2_project/build/frontend_container

sudo docker build -t my_server .
sudo docker run --rm  -v "$(pwd)":/server --network=project_network --name project_server my_server

then, do:
in virtualization2_project/backend/server
sudo docker build -t frontend .
sudo docker run --rm -it --network=project_network -p 8123:8000 frontend


then do:
in virtualization2_project/solver_test
sudo docker build -t solver .
sudo docker run -v ~/Documents/virtualization2_project/backend/server:/solver --rm --network=project_network --name=solver solver
