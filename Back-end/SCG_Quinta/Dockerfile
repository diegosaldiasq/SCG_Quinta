FROM python:3.8

WORKDIR /app

COPY . /app
COPY requirements.txt /app
RUN pip install --upgrade pip 
#crear ambiente virtual
#RUN pip install virtualenv
#RUN virtualenv venv 
#RUN . venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt

#RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "SCG_Quinta.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "10", "--timeout", "60"]