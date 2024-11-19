import pandas as pd

# Testet, ob im "name" am Ende eine Zahl steht
def split_name(name):
    '''
    :param name: (string) Entry in the “name” column of result.csv
    :return: (list) of strings
    :logik: divide a "_"-seperated string into a list of strings
    '''
    a = name.split('_')
    if len(a) == 1:
        return a
    if len(a) > 1:
        parts = name.rsplit('_', 1)  # Trennt den String in zwei Teile
        if parts[1].isdigit():  # Überprüft, ob der letzte Teil eine Zahl ist
            return parts[0].split('_') + [int(parts[1])]
        else:
            return name.split('_')

# Teilt die Einträge in Spalte "name" von data und entsprechende Zuordnung in Spalten von results
def name_function(data,output):
    for i in data.index:
        a = split_name(data.loc[i, "name"])
        # verschiedene verzweigungen, abhängig von den Einträgen in der Spalte "name"
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
    energy_units = ["MWh","kWh","PJ"]
    weighted_units = ["Mt","Mt/a","kg"]
    for i in data.index:
        a = data.loc[i, "var_name"].split('_')
        # verschiedene verzweigungen, abhängig von den Einträgen in der Spalte "var_name"
        # invest - Verzweigung
        if a[0] == "invest":
            if data.loc[i,"unit"] in energy_units:
                output.loc[i, "parameter"] = "capacity_p_inst"
                continue
            if data.loc[i,"unit"] in weighted_units:
                output.loc[i, "parameter"] = "capacity_w_inst"
                continue
        # flow - Verzweigung
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
        # system - Verzweigung
        else:
            output.loc[i, "process"] = '_'.join(a[:2])
            output.loc[i, "parameter"] = a[-1]