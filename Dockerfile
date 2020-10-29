# We Use an official Python runtime as a parent image
FROM python:3.8.5

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
COPY requirements.txt ./

# Install production dependencies.
RUN pip install -r requirements.txt

EXPOSE 8000

CMD exec gunicorn mdm.wsgi:application — bind 0.0.0.0:8000 — workers 3
