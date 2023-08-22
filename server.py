import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from quart import Quart, render_template
import subprocess
import glob
import hupper
from routes.file_management import file_management

app = Quart(__name__, template_folder='./templates', static_folder='./assets')
app.config['TEMPLATES_AUTO_RELOAD'] = True
pywebview_process = None

# Register blueprints
app.register_blueprint(file_management, url_prefix='/file')

@app.route('/')
async def index():
    print("Rendering index.html")  # Debugging output
    return await render_template('index.html')

@app.before_serving
async def startup_event():
    global pywebview_process
    pywebview_process = subprocess.Popen(["python", "pywebview.py"])

@app.after_serving
async def shutdown_event():
    global pywebview_process
    if pywebview_process:
        pywebview_process.terminate()  # Sends SIGTERM to the process
        pywebview_process.wait()  # Waits for process to finish

def run_server():
    print("Running server...")

    # Explicitly list the files to be watched
    assets = glob.glob('./assets/*')
    routes = glob.glob('./routes/*.py')
    html_files = glob.glob('./templates/*.html')
    watched_files = html_files + ['./pywebview.py'] + routes + assets

    print(f"Watching the following files: {watched_files}")

    # Start the reloader
    reloader = hupper.get_reloader()
    reloader.watch_files(watched_files)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(serve(app, Config()))
