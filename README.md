# Flask-Terminal

Flask-Terminal is a bad idea wrapped in an even worse implementation
Use this with care, it is a shell on your server
- [Flask-Terminal](#flask-terminal)
  - [Genesis](#genesis)
  - [Overview](#overview)
  - [Features](#features)
  - [Getting started](#getting-started)
    - [Security](#security)
    - [Requirements](#requirements)
    - [Quickstart](#quickstart)


## Genesis 
While running a docker instance with the need to do adhoc commands to interact with a mounted volume
We looked for some sort of terminal that would run in flask as a blueprint, none to be found.
Wrote our own, heavily inspired by Chad Smith's https://github.com/cs01/pyxtermjs

Flask-Terminal employs Flask and xterm.js to deliver a real-time terminal experience, enabling the execution of terminal within a web browser.

## Overview

The backend of Flask-Terminal is built on Flask, utilizing python-pty for pseudo-terminal emulation, enabling shell command execution. 
The frontend leverages xterm.js for rendering the terminal interface. 
Communication is handled through HTTP polling, circumventing the need for WebSockets. 
The application is structured as a Flask Blueprint, allowing ease of integration into larger Flask applications.

## Features

- **Browser-based Terminal**: Provides a terminal interface within the browser using xterm.js.
- **Command Execution**: Supports the execution of /bin/sh commands, including the capability to spawn additional shells.
- **Real-time Output**: Displays command execution output in real-time, facilitated by HTTP polling.
- **Command Logging**: Utilizes a Python logger to log terminal activities, aiding in audit and debugging.

## Getting started

### Security
We cannot stress how much you need to secure this application, and recommend to enable only as needed and disable immediately afterwards.
To add security to a blueprint please review how we do this with [Flask File Explorer](https://github.com/thevgergroup/flask-file-explorer?tab=readme-ov-file#flask-login-with-a-blueprint)


### Requirements

- Python 3.9 or newer
- Flask web framework
- xterm.js
- A modern web browser

### Quickstart

Installation
```sh
pip install flask-terminal
```

Configuration within flask
Ensure you implement some level of authentication in your application

```python

from flask import Flask
from flask_terminal import terminal_blueprint, configure_logger


app = Flask(__name__)
app.logger = configure_logger('flask_terminal')

app.config['SECRET_KEY'] = 'your_secret_key_here'

# Register the terminal blueprint
app.register_blueprint(terminal_blueprint, url_prefix='/terminal')

@app.route('/ping')
def ping():
    app.logger.info("Accessed /ping route")
    try:
        app.logger.info("Successfully returned 'pong'")
        return 'pong', 200
    except Exception as e:
        app.logger.error(f"Error in ping route: {e}", exc_info=True)
        return "An error occurred", 500

####
## IMPLEMENT SOME SORT OF SECURITY 
## Around your application, below is an example
###
def is_authenticated():
    """Check if the user is authenticated based on a token stored in the session."""
    # Example logic for checking if a user is authenticated
    return 'user_token' in session and session['user_token'] == 'your_secure_token'

@terminal_blueprint.before_request
def before_request_func():
    if not is_authenticated():
        # Redirect to login page or return an error
        current_app.logger.info("User not authenticated, redirecting to login.")
        return redirect('/login')  # Adjusted to use a direct path



if __name__ == '__main__':
    app.run(port=8080)
```

Launch your flask app as normal
```sh
flask -A app.py --debug run --port 8000
```

This will now make the terminal available at http://localhost:8080/terminal
The URL can be configured via the url_prefix
```python
app.register_blueprint(terminal_blueprint, url_prefix='/terminal')
```