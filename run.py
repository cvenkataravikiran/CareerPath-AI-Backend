import os
from core import create_app

config_name = os.getenv('FLASK_CONFIG', 'default')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()