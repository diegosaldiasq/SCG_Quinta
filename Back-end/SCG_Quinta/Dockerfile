FROM python:3.8

WORKDIR /app

COPY requirements.txt /app
RUN pip install --upgrade pip 
#crear ambiente vistual
RUN pip install virtualenv
RUN virtualenv venv 
RUN . venv/bin/activate
RUN pip install -r requirements.txt 


COPY . /app

EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]