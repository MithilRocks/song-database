# Song Application in Flask (Task)

To initialize the application, simply run the shell file `./install.sh` and then `python app.py`. This will take care of installing all the packages.

In case the installation fails, please follow the following steps:

### Step 1: Clone repo
Open command prompt. Clone this repository in the location of your choice using `git clone https://github.com/MithilRocks/song-database.git`

### Step 2: Setup and installation 
Change directory to `song-database` folder.

Run the command `pipenv shell` to run virtual environment. Wait for a few minutes for the virtual environment to finish the setup.

[If pipenv not available, install it using `pip install pipenv`](https://pypi.org/project/pipenv/)

Next, run the command `pipenv sync` to install all the dependencies. Give it another minute. 

### Step 3: Run application
The application is ready to run. Ensure virual enviroment is active before doing so. One can check this by looking at the virtual environment name displayed in the command line.

Run the command: `python app.py`

Finally visit `http://127.0.0.1:5000/`
