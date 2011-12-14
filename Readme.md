Static-Org
========================

This application is for securely serving static content based on a user being
part of a google apps organization. To run:

1. Setup your environment

    virtualenv --no-site-packages venv
    source venv/bin/activate
    pip install -r requirements.txt

2. Put any items you wish to secure into the templates folder
3. Set an environment variable for your google apps domain

    export DOMAIN=mydomain.com

4. Start the webserver

    python app.py

To deploy this to Heroku simply:

    heroku create -s cedar
    git push heroku master
    heroku config:add DOMAIN=mydomain.com

