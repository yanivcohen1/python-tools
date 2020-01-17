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
    install_requires=["flask", "marshmallow-dataclass", "marshmallow-enum", "flask-jsonpify",
     "flask-sqlalchemy", "flask-restful", "flask-cors", "Flask-JWT", "itsdangerous"],
    extras_require={"test": ["pytest", "coverage"]},
)
