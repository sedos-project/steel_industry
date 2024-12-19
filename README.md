# Steel industry

Models steel industry with the SEDOS reference dataset. 

## Introduction
In the SEDOS project, we created an open-source model structure and data set that incorporates 
key future technologies for electricity, heat, conversions, transport, and industry within a 
sector-coupled energy system. 
Within this repository a part of this energy system is modeled (steel industry).
Functionalities include:
* Download of data and metadata from a DataBus Collection
* Transformation and adaption of data with [data_adapter](https://github.com/sedos-project/data_adapter) and [data_adapter_oemof](https://github.com/sedos-project/data_adapter_oemof).
* Bulilding of energy system with [oemof.tabular]()
* Solving of energy system and processing results
* Postprocessing of results with integrated result data adapter for visualising results with the [SEDOS-dashboard](https://sedos.apps.rl-institut.de).

For more information about the SEDOS project check out our [documentation](https://sedos-project.github.io/organization/).

## Getting Started

### Installation

To install steel_industry, follow these steps:

* git-clone steel_industry into local folder:
  `git clone https://github.com/sedos-project/steel_industry.git`
* enter folder `cd steel_industry`
* create virtual environment using conda: `conda env create -f environment.yml`
* activate environment: `conda activate steel_industry`
* install data_adapter_oemof package using poetry, via: `poetry install`
* If you have trouble try `poetry update`.

Note: data_adapter_oemof is installed on branch `sedos/steel_sector`

### Usage

To model the steel industry run the script `run_steel_industry`.