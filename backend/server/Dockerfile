FROM python:latest
RUN pip install websockets pandas
WORKDIR /server/
ADD test-server.py .
EXPOSE 8001
CMD [ "python3", "-u", "test-server.py"]
