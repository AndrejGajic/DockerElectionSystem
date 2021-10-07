FROM python:3

RUN mkdir -p /opt/src/elections/admin
WORKDIR /opt/src/elections/admin

COPY elections/admin/migrate.py ./migrate.py
COPY elections/admin/configuration.py ./configuration.py
COPY elections/admin/models.py ./models.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

# RUN rm -rf ./migrations

ENTRYPOINT ["python", "./migrate.py"]