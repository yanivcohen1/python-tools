Flaskr
======

The basic blog app built in the Flask `tutorial`_.

.. _tutorial: http://flask.pocoo.org/docs/tutorial/

To add dependencys lib in file "setup.py"in setup(install_requires=["dependencyslibName"])

Install
-------

**Be sure to use the same version of the code as the version of the docs
you're reading.** You probably want the latest tagged version, but the
default Git version is the master branch. ::

    # clone the repository
    $ git clone https://github.com/pallets/flask
    $ cd flask
    # checkout the correct version
    $ git tag  # shows the tagged versions
    $ git checkout latest-tag-found-above
    $ cd examples/tutorial

Create a virtualenv and activate it::

    $ python3 -m venv venv
    $ . venv/bin/activate

on linux use pip3 and python3

Add to windows path:
C:\Users\yaniv\anaconda3
C:\Users\yaniv\anaconda3\Scripts; 
C:\Users\yaniv\anaconda3\Library\bin 
//install
pip install virtualenv
//for anaconda3 open powerShell in admin and type:
Set-ExecutionPolicy RemoteSigned
// then "control"+"shift"+"p" and type "reload window"

Or on Windows cmd::

    $ py -m venv venv
    $ venv\Scripts\activate.bat
    $ venv\Scripts\activate

Install Flaskr::

    $ pip install -e .
    #linux
    $pip install --user pipenv
    $pip install --user -e .

Or if you are using the master branch, install Flask from source before
installing Flaskr::

    $ pip install -e ../..
    $ pip install -e .


Run
---

on linux ::

    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run

on PS ::

    > $env:FLASK_APP = "flaskr"
    > $env:FLASK_ENV = "development"
    > flask init-db
    > flask run

    to run the angular server.py > $env:FLASK_APP = ".\flaskr\server.py"
    flask run
    yarn
    yarn start
    Open http://127.0.0.1:4200 in a browser.

Or on Windows cmd::

cd .\flaskr\
    > set FLASK_APP=flaskr
    > set FLASK_ENV=development
    > flask init-db
    > flask run

//run the .\flaskr\app.py
Open http://127.0.0.1:5000 in a browser.
username: yaniv
pass: 1234

Debug in vsc
---
run in debug window task: 'Python: Flask'

Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser

Deploy
---
https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/
https://github.com/pallets/flask/tree/master/examples/tutorial
python3 -m ensurepip --default-pip
python3 -m pip install --upgrade pip setuptools wheel
pip install wheel
//python setup.py sdist
python setup.py sdist bdist_wheel
this creacte a dist directory

Run with a Production machine
---
Create a virtualenv as above describe
pip install flaskr-1.0.0-py3-none-any.whl
Run as above describe

Run as production server
---
pip install waitress
disable the firewall comodo
Create a virtualenv as above describe
Run as above describe without the development variable
waitress-serve --port=5000 --call 'flaskr:create_app'
// --call 'module:function'
// module is the file name.
// need to import the fileName from mainModule