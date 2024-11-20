import pandas as pd

def split_name(name):
    '''
    :param:  name: (string) - Entry in the “name” column of result.csv
    :return: (list) of strings
    :logik: divide a "_"-seperated string into a list of strings
    '''
    a = name.split('_')
    if len(a) == 1:
        return a
    if len(a) > 1:
        parts = name.rsplit('_', 1)
        if parts[1].isdigit():  # Checks whether the last part is a number
            return parts[0].split('_') + [int(parts[1])]
        else:
            return name.split('_')

def name_function(data,output):
    '''
    :param:  data: (pd.Dataframe)
             output: (pd.Dataframe)
    :return: output values for output
    :logik: Splits the entries in column “name” of data and corresponding assignment in columns of output
    '''
    for i in data.index:
        a = split_name(data.loc[i, "name"])
        # Various conditions, depending on the entries in the “name” column
        if len(a) == 1:
            output.loc[i, "process"] = data.loc[i, "name"]
            continue
        if isinstance(a[-1], int):
            output.loc[i, "process"] = data.loc[i, "name"]
            output.loc[i, "sector"] = a[0]
            a = a[1:]
            output.loc[i, "category"] = a[0]
            a = a[1:]
            output.loc[i, "new"] = a[-1]
            a = a[:-1]
            output.loc[i, "specification"] = a
        else:
            output.loc[i, "process"] = data.loc[i, "name"]
            output.loc[i, "sector"] = a[0]
            a = a[1:]
            output.loc[i, "category"] = a[0]
            a = a[1:]
            output.loc[i, "specification"] = a

def var_name_function(data,output):
    '''
    :param:  data: (pd.Dataframe)
                 output: (pd.Dataframe)
    :return: output values (string/int) for output (pd.Dataframe)
    :logik: Splits the entries in column “var_name” of data and corresponding assignment in columns of output
    '''
    #energy_units = ["MWh","kWh","PJ"]
    #weighted_units = ["Mt","Mt/a","kg"]
    for i in data.index:
        a = data.loc[i, "var_name"].split('_')
        # Various conditions, depending on the entries in the “var_name” column
        # invest - condition
        if a[0] == "invest":
            a = a[2:]
            output.loc[i, "output_groups"] = '_'.join(a) # there is only invest_out
            continue
        # flow - condition
        if a[0] == "flow":
            output.loc[i, "parameter"] = "flow_volume"
            if a[1] == "in":
                a = a[2:]
                output.loc[i, "input_groups"] = '_'.join(a)
                continue
            if a[1] == "out":
                a = a[2:]
                output.loc[i, "output_groups"] = '_'.join(a)
                continue
        # system - condition
        else:
            output.loc[i, "process"] = '_'.join(a[:2])
            output.loc[i, "parameter"] = a[-1]

def add_units(output, units):
    """
    Adds units to `output` depending on input data units.

    Uses apply_units() to adapt the `output`.

    Parameters
    ----------
    output : pd.DataFrame
        Contains the output data at current stage. See result_data_adapter.py
        for column names.
    units : dict
        Result of es.units. keys: process names values: dict containing
        parameters of optimization as keys and units as values.
    """
    def apply_units(x, units, output):
        parameter = x["parameter"]

        # Get commodity for which the unit is needed
        commodities = x[["input_groups", "output_groups"]].dropna()
        if len(commodities) != 1:
            logging.warning(
                f"Unit can only be defined for 1 commodity, got {commodities} "
                f"for {x['process']} {parameter}.")
            return np.nan
        commodity = commodities.iloc[0]

        if parameter == "flow_volume":
            # Get possible units, drop duplicates
            possible_units_dict = {
                key: value for key, value in units.items() if commodity in key}
            if len(possible_units_dict) > 1:
                # if there is a conversion factor it is used over ef_ and flow shares
                possible_units_dict = {
                    key: value for key, value in possible_units_dict.items()
                        if "ef_" not in key and "flow_share_" not in key}

        elif parameter == "capacity_x_inst":
            possible_units_dict = {
                key: value for key, value in units.items() if "capacity" in key}
            if len(possible_units_dict) != 1:
                possible_units_dict = {key: value for key, value in
                                       units.items() if commodity in key}

        # elif parameter == "":
        else:
            return np.nan
            logging.warning(f"No unit found for {parameter} of {x['process']}.")

        possible_units = list(
            set([value for value in possible_units_dict.values()]))
        if len(possible_units) != 1:
            logging.warning(
                f"No unit or more than one unit found for {commodity} of "
                f"{x['process']}: {possible_units}.")
            return np.nan
        # If the unit is retrieved from a conversion_factor, the unit in
        # the numerator is the unit of the commodity
        unit = possible_units[0].split("/")[0]

        return unit

    output["unit"] = output[
        ["parameter", "process", "input_groups", "output_groups"]
    ].apply(lambda x: apply_units(x, units[x["process"]], output), axis=1)


