FROM python:latest
RUN pip install websockets
WORKDIR /server/
ADD test-server.py .
EXPOSE 8001
CMD [ "python3", "test-server.py"]
