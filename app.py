import sys
import hupper
from server import run_server

if __name__ == '__main__':
    print("Starting application...")
    reloader = hupper.start_reloader('server.run_server')
    print("Application started.")
