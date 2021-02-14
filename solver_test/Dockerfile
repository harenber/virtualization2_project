FROM python:latest
RUN pip install websockets numpy pandas
WORKDIR /solver/
ADD solver.py .
EXPOSE 8002
CMD [ "python3", "solver.py"]
