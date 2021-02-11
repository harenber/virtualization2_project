FROM python:latest
RUN pip install websockets
WORKDIR /usr/src/app
ADD test-client.py .
CMD [ "python3", "test-client.py" ]
