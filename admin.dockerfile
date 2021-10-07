FROM python:3

RUN mkdir -p /opt/src/elections/admin
WORKDIR /opt/src/elections/admin

COPY elections/admin/application.py ./application.py
COPY elections/admin/configuration.py ./configuration.py
COPY elections/admin/utils.py ./utils.py
COPY elections/admin/models.py ./models.py
COPY elections/admin/manage.py ./manage.py
COPY ./roleCheck.py ./roleCheck.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]