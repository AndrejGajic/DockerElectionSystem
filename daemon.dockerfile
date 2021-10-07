FROM python:3

RUN mkdir -p /opt/src/elections/daemon


WORKDIR /opt/src/elections/daemon

COPY elections/daemon/utils.py ./utils.py
COPY elections/daemon/configuration.py ./configuration.py
COPY elections/daemon/application.py ./application.py
COPY elections/daemon/models.py ./models.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "application.py"]