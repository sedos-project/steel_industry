import logging
import pathlib
import shutil
from pathlib import Path

import pandas as pd
from data_adapter.databus import download_collection  # noqa
from data_adapter.preprocessing import Adapter  # noqa: E402
from data_adapter.structure import Structure  # noqa: E402
from data_adapter_oemof.build_datapackage import DataPackage  # noqa: E402
from data_adapter_oemof.utils import load_yaml
from oemof.solph import Model, processing
from oemof.solph._energy_system import EnergySystem
from oemof.solph.buses import Bus
from oemof.tabular.datapackage import building  # noqa F401
from oemof.tabular.datapackage.reading import (
    deserialize_constraints,
    deserialize_energy_system,
)
from oemof.tabular.facades import (
    Commodity,
    Conversion,
    Excess,
    Load,
    Volatile,
    Storage,
    ConversionGHG,
    CommodityGHG,
)
from oemof_industry.mimo_converter import MIMO
from oemof_industry.emission_constraint import CO2EmissionLimit

from steel_industry.parameter_map import PARAMETER_MAP_STEEL
from steel_industry import postprocessing

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

EnergySystem.from_datapackage = classmethod(deserialize_energy_system)

Model.add_constraints_from_datapackage = deserialize_constraints

DEBUG = True  # set to False for full run. DEBUG reduces to 5 time steps per period

"""
Download Collection

Also adjust Modelstructure:
    Delete lines:
        - helper sinks in HelperO1
        - red marked lines in ProcessO1 and Helper_O1(not yet uploaded or deleted data)
"""

download_collection(
    "https://databus.openenergyplatform.org/felixmaur/collections/steel_industry_test/"
)

logger.info("Reading Structure\n")
structure = Structure(
    "SEDOS_Modellstruktur_sh_test_steel_repo",
    # "SEDOS_Modellstruktur",
    process_sheet="Processes_O1",
    parameter_sheet="Parameter_Input-Output",
    helper_sheet="Helper_O1",
)

adapter = Adapter(
    "steel_industry_test",
    # "steel_industry_test_modified",
    structure=structure,
)

logger.info("Building Adapter Map\n")

# create dictionary with all found in- and outputs
process_adapter_map = pd.concat(
    [
        pd.read_excel(
            io=structure.structure_file,
            sheet_name="Processes_O1",
            usecols=("process", "facade adapter (oemof)"),
            index_col="process",
        ),
        pd.read_excel(
            io=structure.structure_file,
            sheet_name="Helper_O1",
            usecols=("process", "facade adapter (oemof)"),
            index_col="process",
        ),
    ]
).to_dict(orient="dict")["facade adapter (oemof)"]

logger.info("Building datapackage...\n")
dp = DataPackage.build_datapackage(
    adapter=adapter,
    process_adapter_map=process_adapter_map,
    parameter_map=PARAMETER_MAP_STEEL,
    debug=DEBUG,  # set DEBUG to False for full run. DEBUG reduces to 5 time steps per period
    bus_map=load_yaml(Path(__file__).parent / "mappings" / "BUS_MAP.yaml"),
)
datapackage_path = pathlib.Path(__file__).parent / "datapackage"

# delete datapackage before saving it as otherwise old elements are kept
shutil.rmtree(datapackage_path)

dp.save_datapackage_to_csv(str(datapackage_path))


logger.info("Building EnergySystem\n")
es = EnergySystem.from_datapackage(
    path="datapackage/datapackage.json",
    typemap={
        "bus": Bus,
        "excess": Excess,
        "commodity": Commodity,
        "conversion": Conversion,
        "load": Load,
        "volatile": Volatile,
        "mimo": MIMO,
        "storage": Storage,
        "conversion_ghg": ConversionGHG,
        "commodity_ghg": CommodityGHG,
    },
)

logger.info("Building Model...\n")
m = Model(es)
logger.info("Solving Model...\n")
m.solve(solver="cbc")

termination_condition = m.solver_results["Solver"][0]["Termination condition"]
if m.solver_results["Solver"][0]["Termination condition"] == "infeasible":
    logger.warning(f"termination condition is '{termination_condition}'\n")
else:
    logging.info(f"Problem solved. (termination condition '{termination_condition}')\n")

logger.info("Processing Results")
es.results = postprocessing.get_results(m)
es.params = postprocessing.get_inputs(m)
# dump energy system to read results again
es.dump(es_dump_path)
else:
es = EnergySystem()
es.restore(es_dump_path)
# process and save results
file_name = pathlib.Path(__file__).parent / "results" / "test" / "results.csv"
postprocessing.process_results(es, file_name)
logger.info("Writing Results and Goodbye :)")
