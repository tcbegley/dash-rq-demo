# README

This repository demonstrates use of Redis and RQ for asynchronously executing
long running tasks in Plotly Dash. The task the app executes is meaningless, it
converts a string to upper case character by character with a time delay for
each character. Hopefully however the programming pattern is clear and the
example should be easily adaptable to other applications.

From the [RQ docs][rq-docs]:

> RQ (Redis Queue) is a simple Python library for queueing jobs and processing
> them in the background with workers.

This example uses a callback to add longer running tasks to an RQ job queue. A
second callback firing on an interval checks the current status of the job,
either retrieving the result or updating a progress bar to indicate progress
made on the task.

A version of this app that uses a PostgreSQL database to store results of long
running tasks can be found on the
[`postgresql` branch](https://github.com/tcbegley/dash-rq-demo/tree/postgresql).

This example can be run locally, or deployed as is to [Heroku][heroku]. You can
also check out a deployed version [here][dash-rq-demo].

## Run locally

Make sure you have [Python>=3.6][python36] and [Redis][redis]. You will need to
[start a Redis server][redis-server]. See the links for more details, but
probably you will want to run something like:

```sh
redis-server &
```

Then do the following (preferably in a virtual environment):

```sh
git clone https://github.com/tcbegley/dash-rq-demo.git
cd dash-rq-demo

pip install -r requirements.txt

# runs worker.py in the background and run_locally.py
python worker.py & python run_locally.py
```

The app should be visible at [localhost:8050](https://127.0.0.1:8050).

## Heroku

To deploy your own copy of this app on Heroku, just click on this button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)][deploy-endpoint]

Alternatively if you would like to set things up manually, follow the below
steps. It's recommended you still have Python>=3.6 and Redis installed locally
so that you can test the deployment with `heroku local`. You will also need to
install the [Heroku CLI][heroku-cli].

### Test locally

The setup is similar to the local option above, but we use `heroku local` to
test the deployment rather than running manually as a pair of Python processes.
You can see the configuration in `Procfile`.

```sh
git clone https://github.com/tcbegley/dash-rq-demo.git
cd dash-rq-demo

pip install -r requirements.txt

heroku local
```

The app will be visible at [0.0.0.0:5000](https://0.0.0.0:5000).

### Deploying the app

If you were able to successfully run the app using `heroku local`, you can now
run the following to deploy to Heroku itself. Note we need to add the Redis
addon, and also use `heroku scale worker=1` to start a worker for processing
the queue in the background.

```sh
heroku create
git push heroku main

heroku addons:create redistogo
heroku scale worker=1

heroku open
```

## Contributing

If something is unclear or you find a bug feel free to submit an issue or pull
request.

[dash-rq-demo]: https://dash-rq-demo.herokuapp.com/
[deploy-endpoint]: https://heroku.com/deploy?template=https://github.com/tcbegley/dash-rq-demo
[heroku]: https://www.heroku.com/
[heroku-cli]: https://devcenter.heroku.com/articles/heroku-cli
[python36]: https://www.python.org/
[redis]: https://redis.io/
[redis-server]: https://redis.io/topics/quickstart#starting-redis
[rq-docs]: https://python-rq.org/
