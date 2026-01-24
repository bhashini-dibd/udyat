import logging

from flask import Flask
from flask.blueprints import Blueprint
from flask_cors import CORS
from flask_mail import Mail
from gunicorn.app.base import BaseApplication

import config
import routes

logging.basicConfig(filename='info.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

log = logging.getLogger('file')

server = Flask(__name__)

server.config.update(config.MAIL_SETTINGS)
# creating an instance of Mail class
mail = Mail(server)

if config.ENABLE_CORS:
    cors = CORS(server, resources={r"/api/*": {"origins": "*"}})

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint, url_prefix=config.CONTEXT_PATH)


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        configs = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in configs.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


# 3. Run inside __main__
if __name__ == '__main__':
    options = {
        'bind': '0.0.0.0:8000',
        'workers': 4,  # Number of worker processes
        'threads': 2,  # Threads per worker (gthreads mode)
        'timeout': 120,

        'errorlog': '-',  # '-' means log to stdout (terminal)
        'accesslog': '-',  # Log request access to stdout too
        'capture_output': True,  # Redirect python 'print' to errorlog
        'loglevel': 'info'  # Ensure info/print level is visible
    }

    print(f"Starting Gunicorn with options: {options}")
    StandaloneApplication(server, options).run()
