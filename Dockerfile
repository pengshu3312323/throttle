FROM python:3.6-slim

WORKDIR /throttle

ADD . /throttle

RUN pip install --trusted-host pypi.python.org -r req.txt

CMD ["python", "throttle/controller.py"]
