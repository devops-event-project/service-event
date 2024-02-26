FROM python:3.11.7-alpine
RUN mkdir -p /service-event
WORKDIR /service-event

COPY requirements.txt /service-event/
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
COPY . /service-event
EXPOSE 8081

CMD ["uvicorn", "index:service_event", "--host", "0.0.0.0", "--port", "8081"]