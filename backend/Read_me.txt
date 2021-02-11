We have a server and a client container, to test them:

cd server/ 
type this:
docker build -t my_server .
docker network create project_network
docker run --rm --network=project_network --name project_server my_server

cd client/ 
type this:
docker build -t my_client .
docker run --rm --network=project_network my_client



The server receives a request from client and send it back. Client prints it.
