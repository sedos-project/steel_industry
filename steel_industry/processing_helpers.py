import logging


def process_component_data(component_data):
    """
    Prepares component data of oemof.solph.processing for results processing.

    This function should be used in oemof.solph.processing here:
    `https://github.com/oemof/oemof-solph/blob/214ef4636afb13349983d3178f64348db2d9ad51/src/oemof/solph/processing.py#L578`

    - Removes mimo (multi input mulit output) groups from `component_data` as
    it is not needed for the processing of the results.
    - Stretches shorter sequences to the length of the longest sequence as all
    sequences have to be of the same length.

    """
    logging.debug("Dropping mimo group entries from inputs")
    component_data["sequences"] = {
        key: value for key, value in component_data["sequences"].items() if "group_" not in key
    }
    # all sequences have to be of the same length
    length_dict = {key: len(value) for key, value in component_data["sequences"].items()}
    if bool(length_dict):
        print(f"Amount of time steps per parameter: {length_dict}")
    if len(set(length_dict.values())) > 1:
        max_length = max(
            len(value) for value in component_data["sequences"].values())
        for key, value in component_data["sequences"].items():
            if len(value) < max_length:
                logging.info(
                    f"Stretching {key} of {component_data['scalars']['label']} to length of longest time series: {max_length}, because sequences have to be of the same length.")
                component_data["sequences"][key] = value * (max_length // len(value)) + value[:max_length % len(value)]

    return component_data