# systorian
Customizable and searchable system stats logger with a web API. Uses Django 1.9's support for fully searchable JSONFields to provide an easily extensible storage framework.

### API
`/` : Get current (most recent) system stats entry
`/api/v1/` : Get full entry list, paginated in 10s
`/api/v1/on/YEAR/MONTH/DAY/` : Get all entries made on the selected day.

Other API endpoints coming soon:
- Arbitrary time range entry selection, down to the second
- Arbitrary stat search, with optional ranges
- Netstats entries with all of the above capabilities

### Important notes
- systorian v0.1 does not have an authentication system. This project is still very much a prototype under construction.
- The installation and setup instructions were hastily prepared on OS X buy written for Ubuntu (by request). It needs Redis running locally, plus Huey (a Python task queue) running in the Django project. It will also need the Django server running to view the entries it creates.
- These deployment notes are intended for development purposes and are not tuned for production. It's a hobby project.

## Server setup summary: OS X
- (Instructions for installing Homebrew should go here)
- (Instructions for `brew install`ing PostgreSQL and Python should go here)
```bash
git clone https://github.com/BFriedland/systorian.git
cd systorian
pip install -r requirements.txt

psql postgres
CREATE USER systorian_owner WITH PASSWORD 'Pick a good password';
ALTER ROLE systorian_owner SET client_encoding TO 'utf8';
ALTER ROLE systorian_owner SET default_transaction_isolation TO 'read committed';
ALTER ROLE systorian_owner SET timezone TO 'UTC';
CREATE DATABASE systorian WITH OWNER systorian_owner;
GRANT ALL PRIVILEGES ON DATABASE systorian TO systorian_owner;
\q

brew install redis
```

Open a new terminal, or read the daemonizing section:

`redis-server`

Run the server BEFORE starting Huey:
```
./manage.py migrate
./manage.py runserver
```

In another new terminal (or make a background process):
- cd into the app directory with Django's manage.py file in it
```
./manage.py run_huey

curl -o localhost:8000
```
- The periodic task should run right away after Huey starts. It has a period of one minute by default.

## More detailed guide
- With Ubuntu notes that are partially speculative due to time constraints, will update later.

#### PostgreSQL

Installing postgres on Ubuntu:
```
sudo apt-get update
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
```

ref: http://stackoverflow.com/a/21123195
```
psql postgres
CREATE USER systorian_owner WITH PASSWORD 'systorian_owner';
ALTER ROLE systorian_owner SET client_encoding TO 'utf8';
ALTER ROLE systorian_owner SET default_transaction_isolation TO 'read committed';
ALTER ROLE systorian_owner SET timezone TO 'UTC';
CREATE DATABASE systorian WITH OWNER systorian_owner;
GRANT ALL PRIVILEGES ON DATABASE systorian TO systorian_owner;
\q
```

#### Huey and Redis

Redis is needed for huey.

Redis quickstart:
- http://redis.io/topics/quickstart
- NOTE: Only need step 1, because only the webserver needs access to redis (all on localhost)

Huey quickstart:
- https://huey.readthedocs.org/en/latest/getting-started.html
-- https://huey.readthedocs.org/en/latest/installation.html#installation

redis-server setup with homebrew, plus redis.conf location on osx: https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298#.fkm22jck2

### Starting the server

Warning, not thoroughly tested on Ubuntu. Only tested on OS X so far.
I got it to work on OS X, but this setup should hopefully translate cleanly enough to Ubuntu with the Ubuntu-specific notes here.

#### Make a virtual environment and clone in to the repository
- (Instructions for making a virtualenv go here; Python venvs need Python first)
```
git clone https://github.com/BFriedland/systorian.git
cd systorian
```

#### Postgres install and setup
```bash
sudo apt-get update
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
```

Bash, into psql:
```bash
sudo psql postgres
CREATE USER systorian_owner WITH PASSWORD 'Pick a good password';
ALTER ROLE systorian_owner SET client_encoding TO 'utf8';
ALTER ROLE systorian_owner SET default_transaction_isolation TO 'read committed';
ALTER ROLE systorian_owner SET timezone TO 'UTC';
CREATE DATABASE systorian WITH OWNER systorian_owner;
GRANT ALL PRIVILEGES ON DATABASE systorian TO systorian_owner;
\q
```

#### Redis install and setup
More bash, this gets and builds redis
```bash
sudo add-apt-repository ppa:chris-lea/redis-server
sudo apt-get update
sudo apt-get install redis-server

wget http://redis.googlecode.com/files/redis-2.4.4.tar.gz
tar xzf redis-2.4.4.tar.gz
cd redis-2.4.4
make
```

#### Daemonize redis
(note: PID file is /usr/local/var/run/redis.pid on osx at least)

##### Option 1: settings file modification
Reference: http://stackoverflow.com/a/525606
```bash
echo "%s/daemonize no/daemonize yes/g
w
q
" | ex redis.conf
redis-server redis.conf
cd ..
```

##### Option 2: Ubuntu's `daemon`
```bash
daemon redis-server redis.conf
cd ..
```

##### Option 3: Running it in a separate shell session
This approach is OS-agnostic.

#### Requirements, migrations
```bash
pip install -r requirements.txt

./manage.py migrate
```

#### Running Huey for django
##### Option 1: Ubuntu's `daemon`
```bash
daemon ./manage.py run_huey
```
##### Option 2: Running it in a separate shell session
This approach is OS-agnostic.

#### Running the server
```bash
./manage.py runserver
```
This can also be daemonized.
