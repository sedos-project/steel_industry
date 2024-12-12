import pandas as pd
import pathlib

from oemof.tabular.cli import scenarios

from steel_industry import functions

#input_path = "results/test/results.csv"
#output_path = "results/dashboard_results/sedos_results.csv"
#scenario = "test_o_steel_tokio_v3"

def process_result(input_path, output_path, scenario, units):
    # read .csv data from input_path
    data = pd.read_csv(input_path, sep=",")

    # create empty dataframes for results
    columns = ["id", "scenario", "process", "parameter", "sector", "category",
               "specification", "new", "groups", "input_groups", "output_groups",
               "year", "unit", "value"]
    output = pd.DataFrame(columns=columns)
    helper_output = pd.DataFrame(columns=columns)

    # Applies a string replacement to each value in the name column.
    data["name"] = data["name"].str.replace(r"--\d+$", "", regex=True)

    # pick helper processes
    helper_processes = ["helper_import_electricity_from_plug", "helper_source_exo_steel",
                        "helper_pow_ind_grid_elec", "helper_sink_exo_steel"]
    helper = functions.filter_rows_by_helper(data, helper_processes)

    # Remove all rows where the entries in the “name” column begin with “helper”
    data = data[~data["name"].str.startswith("helper")]
    data.reset_index(drop=True)

    # calculate results for output dataframe
    output.value = data.var_value
    output.year = data.year
    functions.name_function(data, output)
    functions.var_name_function(data, output)

    # calculate results for helper_output dataframe
    functions.helper_results(helper, helper_output)
    helper_output["value"] = helper["var_value"]

    # concat output and helper
    sedos_results = pd.concat([output, helper_output], ignore_index=True)

    # add units
    functions.add_units(sedos_results, units)

    # calculate emissions CO2_eq
    # used equation: co2_eq = co2 + 28 x ch4 + 265 x n2o
    sedos_results = functions.calculate_co2_eq(sedos_results)

    # fill columns "scenario" and "id"
    sedos_results.scenario = scenario
    sedos_results["id"] = range(len(sedos_results))

    # change datatype of certain columns from string to string-array
    functions.change_values_to_string_array(sedos_results, columns=["input_groups", "output_groups", "groups"])

    # save results as csv
    sedos_results.to_csv(output_path, sep=";", index=False)
