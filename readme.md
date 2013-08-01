flask-environ
=============

A tiny wrapper around `os.environ` that provides a concise way of importing
configuration from the environment.


Quickstart
----------

```python
from flask import Flask
from flask_environ import get, collect, word_for_true

app = Flask(__name__)

app.config.update(collect(
    get('DEBUG', default=False, convert=word_for_true),
    get('HOST', default='127.0.0.1'),
    get('PORT', default=5000, convert=int),
    get('SECRET_KEY',
        'SQLALCHEMY_DATABASE_URI',
        'TWITTER_CONSUMER_KEY',
        'TWITTER_CONSUMER_SECRET',
    ),
))
```

ta-daa!


Usage
-----


### `flask_environ.get(*env_keys, **settings)`

returns environment variables as a `dict`, keyed by their names.

```python
>>> from flask_environ import get
>>> get('HOME')
{'HOME': '/home/phil'}
>>> get('DISPLAY', 'SHELL', 'TERM')
{'TERM': 'xterm', 'SHELL': '/bin/bash', 'DISPLAY': ':0'}
```


#### The `convert` setting

A callable for changing the environment variable. Note that _all_ environment
variables come back as strings by default.

```python
>>> from flask_environ import get
>>> get('XDG_SESSION_ID', 'DEBUG')
{'DEBUG': 'True', 'XDG_SESSION_ID': '1'}  # Everything is strings?!
>>> get('XDG_SESSION_ID', convert=int)
{'XDG_SESSION_ID': 1}
```


#### The 'default' setting

You can probably guess...

```bash
[phil@notdeadyet ~]$ printenv
XDG_SESSION_ID=1
SHELL=/bin/bash
USER=phil
HOME=/home/phil
DISPLAY=:0
DEBUG=True
[phil@notdeadyet ~]]$ python
Python 2.7.5 (default, May 12 2013, 12:00:47) 
[GCC 4.8.0 20130502 (prerelease)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from flask_environ import get
>>> get('DEBUG', default='False')  # DEBUG is in the environment
{'DEBUG': 'True'}
>>> get('PORT', default=5000)  # PORT is not in the environment
{'PORT': 5000}
```

Note that if the default is used, it will _not_ pass through `convert`.


#### The 'config_key' setting

Renames the key in the resulting dict.

```python
>>> from flask_environ import get
>>> get('TERM', config_key='TERMINAL')
{'TERMINAL': 'xterm'}
```


### `flask_environ.collect(*dicts)`

Merges dictionaries, intended for use with multiple `get`s.

```python
>>> from flask_environ import get, collect
>>> collect(
...     get('TERM', config_key='TERMINAL'),
...     get('PORT', convert=int, default=5000),
...     get('USER',
...         'HOME'),
... )
{'TERMINAL': 'xterm', 'HOME': '/home/phil', 'PORT': 5000, 'USER': 'phil'}
```


### `flask_environ.word_for_true(word)`

Test whether `word` should be considered a boolean `True`. Acceptable strings
include `true`, `yes`, `on`, and `1` (the numeral one as a string). It is case-
insensitive.

This function is provided as a convenience, intended for use with the `convert`
setting.

```python
>>> from flask_environ import get, word_for_true
>>> get('DEBUG')
{'DEBUG': 'True'}
>>> get('DEBUG', default=False, convert=word_for_true)
{'DEBUG': True}
>>> from os import environ; environ['DEBUG'] = 'False'
>>> get('DEBUG', default=False, convert=word_for_true)
{'DEBUG': False}
>>> del environ['DEBUG']
>>> get('DEBUG', default=False, convert=word_for_true)
{'DEBUG': False}



Patterns
--------


### Flask

Flask keeps app configuration in an attribute called `config`. It's basically
a dictionary. So it has a nice `update` method for setting configuration.

The problem is that getting configuration from the environment is redundant,
tedious, and (I think) kind of ugly:

```python
from os import environ
from flask import Flask

app = Flask(__name__)

app.config.update(
    DEBUG=(environ.get('DEBUG') == 'True'),
    HOST=environ.get('HOST', '127.0.0.1'),
    PORT=int(environ.get('PORT', 5000)),
    SQLALCHEMY_DATABASE_URI=environ['DATABASE_URI'],
    SECRET_KEY=environ['SECRET_KEY'],
    TWITTER_CONSUMER_KEY=environ['TWITTER_CONSUMER_KEY'],
    TWITTER_CONSUMER_SECRETE=environ['TWITTER_CONSUMER_SECRET'],
)

```python
from flask import Flask
from flask_environ import get, collect, word_for_true

app = Flask(__name__)

app.config.update(collect(
    get('DEBUG', default=False, convert=word_for_true),
    get('HOST', default='127.0.0.1'),
    get('PORT', default=5000, convert=int),
    get('DATABASE_URI', config_key='SQLALCHEMY_DATABASE_URI'),
    get('SECRET_KEY',
        'TWITTER_CONSUMER_KEY',
        'TWITTER_CONSUMER_SECRET',
    ),
))
```


### Managing Environment Variables

...would be pushing the scope of this readme a bit. but possibly helpful?


Exceptions
----------

blah blah blah
