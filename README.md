# README

This repository demonstrates use of Redis and RQ for long running tasks with
Plotly Dash.

## Run locally

Make sure you Have Python >=3.6, Redis and PostgreSQL installed. Then do the
following (in a virtual environment if you wish)

```
git clone https://github.com/tcbegley/dash-rq-demo.git
cd dash-rq-demo

pip install -r requirements.txt

createdb dash-rq-demo

# runs worker.py in the background and run_locally.py
python worker.py & python run_locally.py
```

The app should be visible at

## Deploy to Heroku

This repo is configured to allow deployment to Heroku. It's recommended you
still have Python >=3.6 and PostgreSQL installed locally so that you can test
the deployment with `heroku local`.

### Test locally

The setup is similar to the local option above, but we use `heroku local` to
test the deployment rather than running manually as a pair of Python processes.

```
git clone https://github.com/tcbegley/dash-rq-demo.git
cd dash-rq-demo

pip install -r requirements.txt

createdb dash-rq-demo

heroku local
```

### Deploy to Heroku

If the app deployed successfully

```
heroku create
git push heroku master

heroku scale worker=1
heroku open
```
