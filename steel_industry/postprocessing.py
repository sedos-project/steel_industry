import pandas as pd

from oemof.solph import processing
from oemof.tabular.postprocessing import calculations, core, naming


def get_results(model):
    try:
        # results = processing.results(m)
        results = processing.convert_keys_to_strings(processing.results(model))
    except ValueError:
        raise ValueError(
            "For processing results of a multi-period optimization "
            "containing mimos you have to drop the mimo groups from "
            "the model results.\n Try adding the following line here "
            "https://github.com/oemof/oemof-solph/blob/v0.5.2.dev1/src/oemof/solph/processing.py#L241 : \n "
            "`df_dict = {key: value for key, value in df_dict.items() if type(key[1]) != str}`")
    return results


def get_inputs(model):
    try:
        inputs = processing.parameter_as_dict(model)
    except ValueError:
        raise ValueError(f"For processing the input parameters of an "
                         f"optimization all sequences must be of the same "
                         f"length.\n Try adding the following lines here "
                         f"https://github.com/oemof/oemof-solph/blob/214ef4636afb13349983d3178f64348db2d9ad51/src/oemof/solph/processing.py#L578 : \n"
                         f"`from steel_industry.processing_helpers import process_component_data`\n"
                         f"`com_data = process_component_data(com_data)`")
    return inputs


def process_results(es, file_name):
    all_scalars = calculations.run_postprocessing(es)

    all_scalars.to_csv(file_name)
