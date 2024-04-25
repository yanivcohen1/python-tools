import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="flaskr",
    version="1.0.0",
    url="http://flask.pocoo.org/docs/tutorial/",
    license="BSD",
    maintainer="Pallets team",
    maintainer_email="contact@palletsprojects.com",
    description="The basic blog app built in the Flask tutorial.",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    # add libs here
    # to add lib A version 1 and lib B at lest version 2 "'A>=1,<2', 'B>=2', c==3.1"
    install_requires=["flask==1.1.2", "marshmallow-dataclass==8.4.1", "marshmallow-enum==1.5.1", "flask-jsonpify==1.5.0",
      "flask-sqlalchemy==2.5.1", "flask-restful==0.3.8", "flask-cors==3.0.10", "Flask-JWT==0.3.2", "itsdangerous==1.1.0",
      "flask-socketio==5.0.1", "schedule==1.1.0", "Jinja2==2.11.3", "markupsafe==1.1.1", "werkzeug==1.0.1", "pynput==1.7.6",
      "scapy", "psutil", "keyboard", "sortedcontainers", "numpy", "matplotlib", "pandas", "pandas_datareader",
      "plotly", "cufflinks", "ipykernel", "selenium", "webdriver-manager", "sympy==1.6.2", "scipy", "pycryptodome",
      "ipywidgets", "IPython", "seaborn", "nbformat", "openpyxl", "jupyterlab-mathjax3", "google-generativeai",
      "pint", "scikit-image", "streamlit", "vpython", "pygame"
      ], # "cupy"
    extras_require={"test": ["pytest", "coverage"]},
)
