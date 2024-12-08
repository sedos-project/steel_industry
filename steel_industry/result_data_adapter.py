import pandas as pd
import pathlib
from steel_industry import functions

'''
# Arbeitsverzeichnis festlegen
# NZ : Brauche ich um das Script ausführen zu können
import os
os.chdir("/home/norman/RLI_Mounts/usershare/SEDOS/steel_industry2/steel_industry")
'''
# später Input == Pfad zur results.csv tabelle
# Preparation Output

# create dataframe for results
columns = ["id", "scenario", "process", "parameter", "sector", "category",
           "specification", "new", "groups", "input_groups", "output_groups",
           "year", "unit", "value"]

output = pd.DataFrame(columns= columns)

helper_output = pd.DataFrame(columns= columns)

# Preparation Input

data = pd.read_csv(pathlib.Path(__file__).parent / "results" / "test" / "results.csv",
                        sep=",")

# alternative
'''
data = pd.read_csv("results/test/results.csv",
                   sep=",")
'''
# Applies a string replacement to each value in the name column.
data["name"] = data["name"].str.replace(r"--\d+$", "", regex=True)

# pick selected helpe_processes
'''
helper_import_electricity_from_plug
helper_source_exo_steel
helper_pow_ind_grid_elec
helper_sink_exo_steel

notes:
helper only with var_name: flow_...
'''
helper_processes = ["helper_import_electricity_from_plug", "helper_source_exo_steel",
                    "helper_pow_ind_grid_elec", "helper_sink_exo_steel"]

helper = functions.filter_rows_by_helper(data, helper_processes)

# Remove all rows where the entries in the “name” column begin with “helper”
data = data[~data["name"].str.startswith("helper")]
data.reset_index(drop=True)

# --------------------------------------------------------------------------------------------------------------------->

# fill the output dataframe with data
output.value = data.var_value
output.year = data.year

functions.name_function(data,output)
functions.var_name_function(data,output) #-> später ausführen -> nach helper

output.unit = "t"

'''
# todo getting the units will be part of data_adapter_industry, when result_data_adapter is a function
from oemof.solph._energy_system import EnergySystem
es = EnergySystem()
es.restore(pathlib.Path(__file__).parent / "results" / "energysystem")
units = es.units
functions.add_units(output, units)
'''

output = output[columns] # ? Wozu ?

# fill the helper_output with data

functions.helper_results(helper,helper_output)

helper_output["value"] = helper["var_value"]

# TO DO: units zu helper noch hinzufügen
# -> functions.add_units(helper_output, units)

helper_output.unit = "t"

# concat output and helper

sedos_results = pd.concat([output, helper_output], ignore_index=True)

# NZ: can we add units here? -> avoiding double code

# calculate emissions CO2_eq
'''
co2_eq = 28 x ch4 + 265 x n2o
"emi_ch4_f_ind", "emi_n2o_f_ind"
'''
sedos_results = functions.calculate_co2_eq(sedos_results)

# fill columns "scenario" and "id"

sedos_results.scenario = "test_o_steel_tokio_v3"
sedos_results["id"] = range(len(sedos_results))

# change datatype of certain columns from string to string-array

functions.change_values_to_string_array(sedos_results, columns=["input_groups", "output_groups", "groups"])

'''
# create random units for testing
import random
energy_units = ["MWh", "kWh", "PJ", "Mt", "Mt/a", "kg"]
power_units = ["W", "kW", "MW", "GW"]
all_units = energy_units + power_units
# Generate random units for each row
sedos_results["unit"] = [random.choice(all_units) for _ in range(len(sedos_results))]
'''

# functions.check_units(sedos_results) -> not needed at the moment

# --------------------------------------------------------------------------------------------------------------------->

# save data as csv

sedos_results.to_csv(pathlib.Path(__file__).parent / "results" / "dashboard_results" / "sedos_results.csv",
                        sep=";", index=False)

# alternative
'''
sedos_results.to_csv("results/dashboard_results/sedos_results.csv",
              sep=";", index=False)
'''
