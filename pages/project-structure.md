---
layout: default
title: Project Structure
index: 3
---

# Project Structure

The Explore Flask book provides [great documentation](https://exploreflask.com/organizing.html) on best practices for organizing your project. For this sample blogging application, we're going to keep it simple:

```
run.py
requirements.txt
blog/
	__init__.py
	models.py
	views.py
	static/
		style.css
	templates/
		index.html
		register.html
		login.html
		logout.html
		profile.html
		display_posts.html
```

Recall that we created `requirements.txt` in the previous step. Typically, the bulk of the action will take place in `models.py` (where we'll define classes, methods, etc.) and `views.py` (where we'll define our views, or site pages). The `__init__.py` file in the `blog/` directory allows it to be used as a [package](https://exploreflask.com/organizing.html#package).

In `views.py`, we'll import the classes and functions we need from `models.py` and initialize the app.

`run.py` is "the file that is invoked to start up a development server. It gets a copy of the app from your package and runs it. This won’t be used in production, but it will see a lot of mileage in development." My `run.py` file looks like this:

```python
from blog import app
import os

app.secret_key = os.urandom(24)
app.run(debug=True)
```

Setting the app's `secret_key` allows you to use sessions, which will be explained later. Setting `debug` to `True` allows you to see the stacktrace when anything goes wrong. When putting your application into production, however, `debug` should be set to `False`. At the end of the tutorial, we'll start our sample blog with `python run.py` and navigate to [http://localhost:5000](http://localhost:5000).

The `blog/static` directory contains CSS, JavaScript, and images, and the `blog/templates` directory contains our Jinja2 templates.

Note that if you're on Neo4j 2.2 and above, you'll need to set environment variables `NEO4J_USERNAME` and `NEO4J_PASSWORD` to your username and password, respectively:

```
$ export NEO4J_USERNAME=username
$ export NEO4J_PASSWORD=password
```

Or, set `dbms.security.auth_enabled=false` in `conf/neo4j-server.properties`.

<p align="right"><a href="{{ site.baseurl }}/pages/the-data-model.html">Next: The Data Model</a></p>