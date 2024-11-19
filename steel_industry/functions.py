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