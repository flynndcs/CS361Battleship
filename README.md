# CS361Battleship
Team Hasbro


This project uses pipenv to manage its dependencies. Pipenv will enfore a specific python version, but running pipenv install will let you know if you need to update your
python or not when it reads the pipfile. So first you will install some form of python just to get pip and pipenv, you may need to update or downgrade your python from there.
In a little bit I will add more virtualenv stuff so that we actually run a local folder based python as well just to make it even easier.

# How to Run:

first install some form of python

then "pip install pipenv"

then "pipenv install" while in the same directory as the clone.

then "pipenv run python Battleship.py"



# How to create release executable:

make sure you have the dev pipenv install - "pipenv install --dev"

then while in the project folder run - "pipenv run pyinstaller -F Battleship.py"

then the exe file is created and placed into dist/Battleship.exe

This executable needs to be in the same folder as res/ and fonts/ and then it works just fine

releases consist of the res/ folder the fonts/ folder and the Battleship.exe
