from setuptools import setup


deps = ['hydra-core', 'gym', 'pygame', 'matplotlib']


setup(
    name="gsslgovf",
    version="0.0.1",
    description="Honours research project. Goal selection strategies for learning goal-oriented value functions",
    url='git@github.com:mamello-justice/gsslgovf.git',
    author="Mamello Seboholi",
    author_email="1851317@wits.students.ac.za",
    packages=['gsslgovf'],
    install_requires=deps
)
