FROM python:3

RUN wget https://nodejs.org/dist/v10.16.0/node-v10.16.0-linux-x64.tar.xz && \
    tar xf node-v10.16.0-linux-x64.tar.xz -C /opt/ && \
    rm -rf node-v10.16.0-linux-x64.tar.xz
ENV PATH=$PATH:/opt/node-v10.16.0-linux-x64/bin

WORKDIR /app
COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app
EXPOSE 80

CMD ["python", "app.py"]