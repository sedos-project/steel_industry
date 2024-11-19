
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import pandas as pd
from functions import name_function, var_name_function

# Preparation Output

# create dataframe for results
columns = ["scenario", "parameter", "process", "sector", "category",
               "specification", "groups", "new", "input_groups",
               "output_groups", "unit", "value"]

output = pd.DataFrame(columns= columns)

# Preparation Input

data = pd.read_csv("results/test/results_invested_capacity.csv",
                        sep=",")

# Applies a string replacement to each value in the name column.
data['name'] = data['name'].str.replace(r'--\d+$', '', regex=True)

# Remove all rows where the entries in the “name” column begin with “helper”
data = data[~data['name'].str.startswith('helper')]
data.reset_index(drop=True)
# --------------------------------------------------------------------------------------------------------------------->

# fill the output dataframe with data

name_function(data,output) 

var_name_function(data,output)

output.value = data.var_value

output.scenario = "o_steel_tokio"

# --------------------------------------------------------------------------------------------------------------------->

# save data as csv

# save data as excel sheet

with pd.ExcelWriter("results/dashboard_results/SEDOS_output.xlsx") as writer:
    output.to_excel(writer, sheet_name="SEDOS_output", index=False)

# Lade die erstellte Excel-Datei mit openpyxl
wb = load_workbook("results/dashboard_results/SEDOS_output.xlsx")

# Funktion zum Anpassen der Spaltenbreite
def adjust_column_width(sheet):
    for col_index, column_cells in enumerate(sheet.columns, start=1):
        # Berechne die maximale Länge der Werte in der Spalte
        max_length = max(len(str(cell.value) or "") for cell in column_cells)  # Handle None values
        column_letter = get_column_letter(col_index)
        # Setze die Spaltenbreite basierend auf der maximalen Länge der Zelleninhalte
        sheet.column_dimensions[column_letter].width = max_length + 5

    # Passe die Spaltenbreite an
sheet = wb["SEDOS_output"]
adjust_column_width(sheet)

