import os
import environ
from os.path import join, dirname, abspath

env = environ.Env()

env_path_file = join(dirname(dirname(abspath(__file__))), '.env')
env.read_env(env_path_file)


SMTP_SERVER_ADDRESS = os.environ.get('SMTP_SERVER_ADDRESS')
SMTP_SERVER_PORT = os.environ.get('SMTP_SERVER_PORT')
SENDER_ADDRESS = os.environ.get('SENDER_ADDRESS')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')