# End to End Data Science Project

# 1. Create a virtual environment

    conda create -p venv python==version_num -y

# 2. Activate the virtual environment

    Win cmd pmt: conda activate venv/
    gitbash: source activate venv/

# 3. create a requirements.txt and setup.py file in root folder

    requirements.txt will have all the required packages for the project
        to Install - pip install -r requirements.txt

    setup.py will create a package of this whole project
        to Install - python setup.py install
    We can add -e . in the requriements.txt and run the requirements.txt command and that will automatically run the setup.py file
