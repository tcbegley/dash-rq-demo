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

This example can be run locally, or deployed as is to [Heroku][heroku].

## Run locally

Start by cloning this repository to your machine.

```
git clone https://github.com/tcbegley/dash-rq-demo.git
cd dash-rq-demo
```

### Docker

If you have [Docker][docker] installed, run the app with

```sh
docker compose up
```

The app can be accessed at [localhost:8050](https://127.0.0.1:8050).

You can alternatively run `docker-compose.dev.yml` for development purposes.
This volume mounts the source code into the container and uses a development
server so that you can benefit from hot-reloading without rebuilding the
container.

```sh
docker compose -f docker-compose.dev.yml up
```
### Run manually

If you don't want to use Docker, first make sure you have
[Python>=3.7][python37] and [Redis][redis] installed. Once you've done this you
will need to [start a Redis server][redis-server]. See the links for more
details, but probably you will want to run something like:

```sh
redis-server &
```

Then do the following (preferably in a virtual environment):

```sh
pip install -r requirements.txt

# runs worker.py in the background and run_locally.py
python worker.py & python run_locally.py
```

The app can be accessed at [localhost:8050](https://127.0.0.1:8050).

## Heroku

To deploy your own copy of this app on Heroku, just click on this button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)][deploy-endpoint]

**Note**: you may need to wait a few minutes for the Redis addon to start before the app starts working.

Alternatively if you would like to set things up manually, follow the below
steps. You will need to install the [Heroku CLI][heroku-cli].

First clone this repository and navigate to it

```sh
git clone https://github.com/tcbegley/dash-rq-demo.git
cd dash-rq-demo
```

Create a new Heroku app and push the contents of this repository

```sh
heroku create
git push heroku main
```

Create the Redis addon, note that this can take a few minutes to start.

```sh
heroku addons:create heroku-redis:hobby-dev
```

You can check the status of the addon with the following command. The app will not work until the addon has been successfully created.

```sh
heroku addons:info heroku-redis
```

Add a worker to handle the background tasks.

```sh
heroku scale worker=1
```

Open the deployed app in your browser

```sh
heroku open
```

## Contributing

If something is unclear or you find a bug feel free to submit an issue or pull
request.

[deploy-endpoint]: https://heroku.com/deploy?template=https://github.com/tcbegley/dash-rq-demo
[docker]: https://www.docker.com/
[heroku]: https://www.heroku.com/
[heroku-cli]: https://devcenter.heroku.com/articles/heroku-cli
[python37]: https://www.python.org/
[redis]: https://redis.io/
[redis-server]: https://redis.io/topics/quickstart#starting-redis
[rq-docs]: https://python-rq.org/
