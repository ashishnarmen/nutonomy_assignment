FROM python:3.8.3-alpine

WORKDIR /nutonomy_assignment
COPY . /nutonomy_assignment 
RUN pip install -r requirements.txt 
ENTRYPOINT [ "python", "-m", "unittest", "-v" ]