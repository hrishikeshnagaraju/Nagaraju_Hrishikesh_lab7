FROM python:3.9
EXPOSE 5050
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install sqlalchemy
RUN pip install celery
COPY Nagaraju_Hrishikesh_lab7.py /app
CMD python Nagaraju_Hrishikesh_lab7.py