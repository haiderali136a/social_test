# social_test

1. Use

docker-compose build web

to build the webapp

2. Use 

docker-compose run web python manage.py migrate

to apply migrations

3. Use

docker-compose run web pytest

to run the tests


Social Automation Robot works outside docker environment (for now)

For this you have to comment the postgres db configurations and enable the sqlite default config in settings file.

Then you can run the server with manage.py command.

Then finally run the bot using command:

python manage.py social_automation_bot
