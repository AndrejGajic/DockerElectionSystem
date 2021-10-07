FROM python:3

RUN mkdir -p /opt/src/elections/user
WORKDIR /opt/src/elections/user

COPY elections/user/configuration.py ./configuration.py
COPY elections/user/application.py ./application.py
COPY elections/user/csvParser.py ./csvParser.py
COPY ./roleCheck.py ./roleCheck.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]