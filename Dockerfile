# syntax=docker/dockerfile:1

# set python and working directory
FROM python:3.8
WORKDIR /app

# copy over requirements and install
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# copy over files
COPY . .

# run the bot
CMD ["python3", "bot.py"]