FROM python:3

RUN mkdir -p /opt/src/elections/modification
WORKDIR /opt/src/elections/modification

COPY elections/modification/application.py ./application.py
COPY elections/modification/configuration.py ./configuration.py
COPY elections/modification/models.py ./models.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]