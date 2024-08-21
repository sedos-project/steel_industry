# Steel industry

Models steel industry with the SEDOS reference dataset.

## Introduction

## Installation

To install steel_industry, follow these steps:

* git-clone steel_industry into local folder:
  `git clone https://github.com/rl-institut/data_adapter_oemof.git
* enter folder `cd steel_industry`
* create virtual environment using conda: `conda env create -f environment.yml`
* activate environment: `conda activate steel_industry`
* install data_adapter_oemof package using poetry, via: `poetry install`
* If you have trouble try `poetry update`.

## Data

## Documentation

https://sedos-project.github.io/organization/scenarios/
https://sedos-project.github.io/organization/results/


## Code linting

In this template, 3 possible linters are proposed:
- flake8 only sends warnings and error about linting (PEP8)
- pylint sends warnings and error about linting (PEP8) and also allows warning about imports order
- black sends warning but can also fix the files for you

You can perfectly use the 3 of them or subset, at your preference. Don't forget to edit `.travis.yml` if you want to deactivate the automatic testing of some linters!
