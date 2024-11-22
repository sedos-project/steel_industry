import pandas as pd
import pathlib

from steel_industry import functions

# Arbeitsverzeichnis festlegen
import os
os.chdir("/home/norman/RLI_Mounts/usershare/SEDOS/steel_industry2/steel_industry")

# Preparation Output

# create dataframe for results
columns = ["id", "scenario", "process", "parameter", "sector", "category",
           "specification", "new", "groups", "input_groups", "output_groups",
           "year", "unit", "value"]

output = pd.DataFrame(columns= columns)

helper_output = pd.DataFrame(columns= columns)

# Preparation Input

'''
data = pd.read_csv(pathlib.Path(__file__).parent / "results" / "test" / "results.csv",
                        sep=",")
'''

# alternative

data = pd.read_csv("results/test/results.csv",
                   sep=",")

# Applies a string replacement to each value in the name column.
data["name"] = data["name"].str.replace(r"--\d+$", "", regex=True)

# pick selected helpe_processes
'''
helper_import_electricity_from_plug
helper_source_exo_steel
helper_pow_ind_grid_elec
helper_sink_exo_steel

notes:
helper only with var_name flow_...
'''
helper_processes = ["helper_import_electricity_from_plug", "helper_source_exo_steel",
                    "helper_pow_ind_grid_elec", "helper_sink_exo_steel"]

helper = functions.filter_rows_by_helper(data, helper_processes)

# Remove all rows where the entries in the “name” column begin with “helper”
data = data[~data["name"].str.startswith("helper")]
data.reset_index(drop=True)

# concat remaining data with selected helper
#data = pd.concat([data,helper], ignore_index=True)

# --------------------------------------------------------------------------------------------------------------------->

# fill the output dataframe with data
output.value = data.var_value
output.year = data.year

functions.name_function(data,output)

functions.var_name_function(data,output)

'''
# todo getting the units will be part of data_adapter_industry, when result_data_adapter is a function
from oemof.solph._energy_system import EnergySystem
es = EnergySystem()
es.restore(pathlib.Path(__file__).parent / "results" / "energysystem")
units = es.units
functions.add_units(output, units)
'''

functions.change_values_to_string_array(output, columns=["input_groups", "output_groups", "groups"])

output = output[columns] # ? Wozu ?

# fill the helper_output with data

functions.helper_results(helper,helper_output)

helper_output["value"] = helper["var_value"]

# concat results

sedos_results = pd.concat([output, helper_output], ignore_index=True)

sedos_results.scenario = "test_o_steel_tokio_v2"

sedos_results["id"] = range(len(sedos_results))

# --------------------------------------------------------------------------------------------------------------------->

# save data as csv

# save data as excel sheet
output.to_csv(pathlib.Path(__file__).parent / "results" / "dashboard_results" / "sedos_results.csv",
                        sep=";", index=False)

output.to_csv("results/dashboard_results/sedos_results.csv",
              sep=";", index=False)

# with pd.ExcelWriter("results/dashboard_results/SEDOS_output.xlsx") as writer:
#     output.to_excel(writer, sheet_name="SEDOS_output", index=False)
#
# # Lade die erstellte Excel-Datei mit openpyxl
# wb = load_workbook("results/dashboard_results/SEDOS_output.xlsx")
#
# # Funktion zum Anpassen der Spaltenbreite
# def adjust_column_width(sheet):
#     for col_index, column_cells in enumerate(sheet.columns, start=1):
#         # Berechne die maximale Länge der Werte in der Spalte
#         max_length = max(len(str(cell.value) or "") for cell in column_cells)  # Handle None values
#         column_letter = get_column_letter(col_index)
#         # Setze die Spaltenbreite basierend auf der maximalen Länge der Zelleninhalte
#         sheet.column_dimensions[column_letter].width = max_length + 5
#
#     # Passe die Spaltenbreite an
# sheet = wb["SEDOS_output"]
# adjust_column_width(sheet)
#
