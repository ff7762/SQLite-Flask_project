FROM python:3-alpine3.9
WORKDIR /opt/apiproject-dir
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY apiproject/models/ apiproject/models/
COPY apiproject/connector.py apiproject/
COPY setup_and_seed.py .
RUN python setup_and_seed.py
COPY . .
CMD python app.py
EXPOSE 5000/tcp
