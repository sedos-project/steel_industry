import pandas as pd
import json
import numpy as np
import logging


def split_name(name):
    """
    divide a "_"-seperated string into a list of strings, depending on last charakter is digit.
    return: list of strings.
    Parameters
    ----------
    name: string
        certain entry in the “name” column of result.csv.
    """
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
    """
    Splits the entries in column “name” of data and corresponding assignment in columns of output.
    Parameters
    ----------
    data: pd.Dataframe
        Contains the data of results.csv without helper_processes.
    output: pd.Dataframe.
        Contains the output data at current stage. See result_data_adapter.py
        for column names.
    """
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
            output.loc[i, "new"] = 1 if a[-1] == 2 else a[-1]
            a = a[:-1]
            output.loc[i, "specification"] = '_'.join(a)
        else:
            output.loc[i, "process"] = data.loc[i, "name"]
            output.loc[i, "sector"] = a[0]
            a = a[1:]
            output.loc[i, "category"] = a[0]
            a = a[1:]
            output.loc[i, "specification"] = '_'.join(a)
            output.loc[i, "new"] = 0 if data.loc[i, "name"] in ["ind_source_steel_scrap_iron"] else 1

def var_name_function(data,output):
    """
    Splits the entries in column “var_name” of data and apply corresponding assignment in columns of output.
    Parameters
    ----------
    data: pd.Dataframe
        Contains the data of results.csv.
    output: pd.Dataframe.
        Contains the output data at current stage. See result_data_adapter.py
        for column names.
    """
    for i in data.index:
        a = data.loc[i, "var_name"].split('_')
        # Various conditions, depending on the entries in the “var_name” column

        # invest_out - condition
        if '_'.join(a[:2]) == 'invest_out':
            a = a[2:]
            output.loc[i, "output_groups"] = '_'.join(a) # there is only invest_out
            if output.loc[i, "new"] == 0:
                output.loc[i, "parameter"] = "capacity_inst"
            else:
                output.loc[i, "parameter"] = "capacity_new"
            continue

        # invest_cost - condition
        if '_'.join(a[:2]) == 'invest_costs':
            output.loc[i, "parameter"] = "costs_investment"
            a = a[3:]
            output.loc[i, "output_groups"] = '_'.join(a) # there is only invest_cost_out
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
            if x.process == "helper_source_exo_steel" or x.process == "helper_sink_exo_steel":
                return "Mt"
            elif "helper_import_electricity_from_plug" in x.process:
                return "MWh"

        elif parameter == "capacity_new" or parameter == "capacity_inst":
            possible_units_dict = {
                key: value for key, value in units.items() if "capacity" in key}
            if len(possible_units_dict) != 1:
                possible_units_dict = {key: value for key, value in
                                       units.items() if commodity in key}
            if x.process == "x2x_other_biogas_treatment":
                return "MW"

        elif parameter == "costs_investment":
            possible_units_dict = {
                key: value for key, value in units.items() if
                "cost_inv" in key}
            if x.process == "x2x_other_biogas_treatment":
                return "EUR"
        else:
            logging.warning(
                f"Add {parameter} to add_units() to get unit for {x['process']}.")
            return np.nan

        possible_units = list(
            set([value for value in possible_units_dict.values()]))
        if len(possible_units) != 1:
            if x.process == "helper_pow_ind_grid_elec":
                return "MWh"
            logging.warning(
                f"No unit or more than one unit found for {commodity} of "
                f"{x['process']}: {possible_units}.")
            return np.nan
        # If the unit is retrieved from a conversion_factor, the unit in
        # the numerator is the unit of the commodity, same accounts for
        # investment costs
        if "," in possible_units[0]:
            unit = possible_units[0].split(",")[0]
        else:
            unit = possible_units[0].split("/")[0]

        return unit

    output["unit"] = output[
        ["parameter", "process", "input_groups", "output_groups"]
    ].apply(lambda x: apply_units(x, units[x["process"]], output), axis=1)

def change_values_to_string_array(output, columns):
    """
    change datatype of certain columns from string to string-array.
    Parameters
    ----------
    output: pd.Dataframe
        Contains the output data at current stage. See result_data_adapter.py
        for column names.
    columns: string-array
        Contains certain columns of output.
    """
    for column in columns:
        output[column] = output[column].apply(
            lambda x: json.dumps([x]) if x is not np.nan else np.nan)

def filter_rows_by_helper(data,helper_processes):
    """
    returns pd.dataframe with selected helper_processes from data.
    Parameters
    ----------
    data: pd.Dataframe
        Contains the data of results.csv.
    helper_processes: string-array
        Contains selected helper_processes.
    """
    return data[data["name"].isin(helper_processes)]

def helper_results(helper,output):
    """
    generate results for helper_output from data which contains helper_processes.

    uses var_name_function to Splits the entries in column
    “var_name” of data and apply corresponding assignment in columns of helper_output.

    Parameters
    ----------
    helper: pd.Dataframe
        Contains the data with helper_processes of results.csv.
    output: pd.Dataframe
        Contains the helper_output data at current stage. See result_data_adapter.py
        for column names.
    """
    for i in helper.index:
        output.loc[i, "process"] = helper.loc[i, "name"]
        output.loc[i, "year"] = helper.loc[i, "year"]
        if helper.loc[i,"name"] == "helper_import_electricity_from_plug":
            output.loc[i,"sector"] = "ind"
            output.loc[i,"category"] = "electricity"
            output.loc[i, "specification"] = "plug"
            output.loc[i, "new"] = 1
            continue
        if helper.loc[i,"name"] == "helper_import_electricity_from_plug_renewable":
            output.loc[i,"sector"] = "ind"
            output.loc[i,"category"] = "electricity"
            output.loc[i, "specification"] = "shortage"
            output.loc[i, "new"] = 1
            continue
        if helper.loc[i,"name"] == "helper_source_exo_steel":
            output.loc[i,"sector"] = "ind"
            output.loc[i,"category"] = "steel"
            output.loc[i, "specification"] = "shortage"
            output.loc[i, "new"] = 1
            continue
        if helper.loc[i,"name"] == "helper_pow_ind_grid_elec":
            output.loc[i,"sector"] = "ind"
            output.loc[i,"category"] = "electricity"
            output.loc[i, "specification"] = "conversion"
            output.loc[i, "new"] = 1
            continue
        if helper.loc[i,"name"] == "helper_sink_exo_steel":
            output.loc[i,"sector"] = "ind"
            output.loc[i,"category"] = "steel"
            output.loc[i, "specification"] = "demand"
            output.loc[i, "new"] = 0
            continue
    var_name_function(helper,output)

def calculate_co2_eq(sedos_results):
    """
    Calculate equivalent co2-emissions of all processes and generate new rows with output_group "emi_co2_eq".
    Parameters
    ----------
    sedos_results: pd.Dataframe
        Contains the sedos_results at current stage. See result_data_adapter.py.
    """
    # filter sedos_results by processes with ch4-, n20- and co2-emissions
    emis = ["emi_ch4_f_ind", "emi_n2o_f_ind", "emi_co2_p_ind", "emi_co2_neg_imp", "emi_co2_reusable", "emi_co2_f_pow", "emi_co2_f_ind"]
    sedos_emis = sedos_results[sedos_results["output_groups"].isin(emis)]

    # Pivot to facilitate calculations
    pivot_df = sedos_emis.pivot_table(
        index=["process", "year"],
        columns="output_groups",
        values="value",
        aggfunc="first"
    ).reset_index()
    # fill NaN with "0"
    pivot_df = pivot_df.fillna(0)
    pivot_df["emi_co2_eq"] = abs(pivot_df["emi_co2_p_ind"] - pivot_df["emi_co2_neg_imp"] + pivot_df["emi_co2_reusable"] +
                              pivot_df["emi_co2_f_pow"] + pivot_df["emi_co2_f_ind"] + 28 * pivot_df["emi_ch4_f_ind"] + 265 * pivot_df["emi_n2o_f_ind"])

    # create dataframe with new rows included calculated co2 - emissions
    new_rows = pivot_df[["process", "year", "emi_co2_eq"]].rename(columns={"emi_co2_eq": "value"})
    new_rows["output_groups"] = "emi_co2_eq"

    # complete new dataframe with the data of the included processes
    grouped = sedos_emis.groupby('process').agg({
        'parameter': 'first',
        'sector': 'first',
        'category': 'first',
        'specification': 'first',
        'new': 'first',
        'unit': 'first'
    }).reset_index()

    new_rows = pd.merge(new_rows, grouped, on="process", how="left")
    # merge new rows to sedos_results
    sedos_results = pd.concat([sedos_results, new_rows], ignore_index=True)

    return sedos_results




