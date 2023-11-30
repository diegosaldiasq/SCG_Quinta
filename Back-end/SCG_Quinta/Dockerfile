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

RUN python manage.py makemigrations

EXPOSE 8000

CMD ["gunicorn", "SCG_Quinta.wsgi:application", "--bind", "0.0.0.0:8000"]