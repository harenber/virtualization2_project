At the moment it's possible to communicate with the container from the host machine using ICP. Use the comands:

docker build -t project_server .
docker run -p 8001:8001 project_server

And then in the folder client run the pythons script.
