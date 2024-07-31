import logging
import pathlib

import pandas as pd
from data_adapter.databus import download_collection  # noqa
from data_adapter.preprocessing import Adapter  # noqa: E402
from data_adapter.structure import Structure  # noqa: E402
from data_adapter_oemof.build_datapackage import DataPackage  # noqa: E402
from oemof.solph import Model, processing
from oemof.solph._energy_system import EnergySystem
from oemof.solph.buses import Bus
from oemof.tabular.datapackage import building  # noqa F401
from oemof.tabular.datapackage.reading import (
    deserialize_constraints,
    deserialize_energy_system,
)
from oemof.tabular.facades import Commodity, Conversion, Excess, Load, Storage, Volatile
from oemof_industry.mimo_converter import MIMO

logger = logging.getLogger()

EnergySystem.from_datapackage = classmethod(deserialize_energy_system)

Model.add_constraints_from_datapackage = deserialize_constraints
"""
Download Collection

Some datasets must be adjusted due to wrong formatting in comments
    - x2x_import_hydrogen_renewable
    - x2x_p2gas_aec_1
    - x2x_p2gas_pemec_1
    - x2x_x2gas_mpyr_1


Also adjust Modelstructure:
    Delete lines:
        - helper sinks in HelperO1
        - red marked lines in ProcessO1 (not yet uploaded or deleted data)
"""

download_collection(
    "https://databus.openenergyplatform.org/felixmaur/collections/steel_industry_test/"
)
logger.info("Reading Structure")
structure = Structure(
    "SEDOS_Modellstruktur",
    process_sheet="Processes_O1",
    parameter_sheet="Parameter_Input-Output",
    helper_sheet="Helper_O1",
)

adapter = Adapter(
    "steel_industry_test_modified",
    structure=structure,
)

logger.info("Building Adapter Map")

# create dicitonary with all found in and outputs
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

parameter_map = {
    "DEFAULT": {"interest_rate": "wacc"},
    "StorageAdapter": {
        "capacity_potential": "expansion_limit",
        "capacity": "installed_capacity",
        "invest_relation_output_capacity": "e2p_ratio",
        "inflow_conversion_factor": "input_ratio",
        "outflow_conversion_factor": "output_ratio",
    },
    "CommodityAdapter": {},
    "x2x_import_biogas": {"amount": "capacity_w_inst_0", "marginal_cost": "cost_var_e"},
    "x2x_import_coal": {"amount": "capacity_w_inst_0", "marginal_cost": "cost_var_e"},
    "x2x_import_hydrogen_renewable": {
        "amount": "capacity_w_inst_0",
        "marginal_cost": "cost_var_e",
    },
    "x2x_other_biogas_treatment": {"marginal_cost": "cost_var_e"},
    "ind_source_steel_scrap_iron": {"amount": "capacity_w_inst_0"},
    "ind_steel_sinter_0": {"capacity": "capacity_w_inst_0"},
    "ind_steel_coke_plant_0": {"capacity": "capacity_e_inst_0"},
    "ind_steel_blafu_0": {"capacity": "capacity_w_inst_0"},
    "ind_steel_oxyfu_0": {"capacity": "capacity_w_inst_0"},
    "ind_steel_casting_0": {"capacity": "capacity_w_inst_0"},
    "ind_steel_elefu_0": {"capacity": "capacity_w_inst_0"},
    "x2x_delivery_methane_pipeline_0": {
        "capacity": "capacity_p_max",
        "marginal_cost": "cost_var_p",
    },
    "x2x_x2gas_sr_syngas_0": {
        "capacity": "capacity_p_inst",
        "capacity_cost": "cost_inv_p",
        "fixed_costs": "cost_fix_p",
    },
    "ind_steel_coke_plant_1": {
        "capacity_potential": "capacity_e_abs_new_max",
        "capacity_cost": "cost_inv_e",
        "fixed_costs": "cost_fix_e",
        "marginal_cost": "cost_var_e",
    },
    "ind_steel_sinter_1": {
        "capacity_potential": "capacity_w_abs_new_max",
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
        "marginal_cost": "cost_var_w",
    },
    "ind_steel_blafu_1": {
        "capacity_potential": "capacity_w_abs_new_max",
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
        "marginal_cost": "cost_var_w",
    },
    "ind_steel_blafu_cc_1": {
        "capacity_potential": "capacity_w_abs_new_max",
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
        "marginal_cost": "cost_var_w",
    },
    "ind_steel_oxyfu_1": {
        "capacity_potential": "capacity_w_abs_new_max",
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
        "marginal_cost": "cost_var_w",
        # "max":"availability_constant"
    },
    "ind_steel_casting_1": {
        "capacity_potential": "capacity_w_abs_new_max",
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
        "marginal_cost": "cost_var_w",
        # "max":"availability_constant"
    },
    "ind_steel_elefu_1": {
        "capacity_potential": "capacity_w_abs_new_max",
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
        "marginal_cost": "cost_var_w",
        # "max":"availability_constant"
    },
    "ind_steel_dirred_1": {
        "capacity_potential": "capacity_w_abs_new_max",
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
        "marginal_cost": "cost_var_w",
        # "max":"availability_constant"
    },
    "ind_steel_sponge_1": {
        "capacity_potential": "capacity_w_abs_new_max",
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
        "marginal_cost": "cost_var_w",
        # "max":"availability_constant"
    },
    "ind_steel_pellet_1": {
        "capacity_potential": "capacity_w_abs_new_max",
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
        "marginal_cost": "cost_var_w",
        # "max":"availability_constant"
    },
    "ind_steel_hyddri_1": {
        "capacity_potential": "capacity_w_abs_new_max",
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
        "marginal_cost": "cost_var_w",
        # "max":"availability_constant"
    },
    "x2x_delivery_hydrogen_pipeline_retrofit_1": {
        "capacity_potential": "capacity_p_max",
        "capacity_cost": "cost_inv_p",
        "fixed_costs": "cost_fix_p",
        "marginal_cost": "cost_var_p",
    },
    "x2x_delivery_hydrogen_pipeline_new_1": {
        "capacity_cost": "cost_inv_p",
        "fixed_costs": "cost_fix_p",
    },
    "x2x_g2p_pemfc_ls_1": {
        "capacity_cost": "cost_inv_p",
        "fixed_costs": "cost_fix_p",
    },
    "x2x_g2p_sofc_ls_1": {
        "capacity_cost": "cost_inv_p",
        "fixed_costs": "cost_fix_p",
    },
    "x2x_other_dac_ht_1": {
        "marginal_cost": "cost_var_w",
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
    },
    "x2x_other_dac_lt_1": {
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
    },
    "x2x_p2gas_aec_1": {
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
    },
    "x2x_p2gas_pemec_1": {
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
    },
    "x2x_p2gas_biom_1": {
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
    },
    "x2x_p2gas_sabm_1": {
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
    },
    "x2x_p2gas_soec_1": {
        "capacity_cost": "cost_inv_w",
        "fixed_costs": "cost_fix_w",
    },
    "x2x_x2gas_mpyr_1": {
        "capacity_cost": "cost_inv_p",
        "fixed_costs": "cost_fix_p",
        "marginal_cost": "cost_var_e",
    },
    "x2x_x2gas_sr_syngas_1": {
        "capacity_cost": "cost_inv_p",
        "fixed_costs": "cost_fix_p",
    },
    "x2x_storage_hydrogen_lohc_1": {
        "efficiency": "efficiency_sto_in",
        "loss_rate": "sto_self_discharge",
        "storage_capacity_cost": "cost_inv_e",
        "fixed_costs": "cost_fix_p",
        "marginal_cost": "cost_var_e",
    },
    "x2x_storage_hydrogen_new_1": {
        "efficiency": "efficiency_sto_in",
        "loss_rate": "sto_self_discharge",
        "storage_capacity_cost": "cost_inv_e",
        "fixed_costs": "cost_fix_p",
        "marginal_cost": "cost_var_e",
        "capacity_capacity_potential": "capacity_e_max",
    },
    "x2x_storage_hydrogen_retrofit_1": {
        "efficiency": "efficiency_sto_in",
        "fixed_costs": "cost_fix_p",
        "loss_rate": "sto_self_discharge",
        "storage_capacity_cost": "cost_inv_e",
        "marginal_cost": "cost_var_e",
        "capacity_capacity_potential": "capacity_e_max",
        "storage_capacity": "capacity_e_inst",
    },
    "x2x_storage_methane_0": {
        "efficiency": "efficiency_sto_in",
        "fixed_costs": "cost_fix_p",
        "loss_rate": "sto_self_discharge",
        "storage_capacity_cost": "cost_inv_e",
        "fixed_costs": "cost_fix_p",
        "marginal_cost": "cost_var_e",
        "capacity_capacity_potential": "capacity_e_max",
        "storage_capacity": "capacity_e_inst",
    },
    "helper_sink_exo_steel": {
        "profile": "demand_timeseries_fixed",
        "amount": "demand_annual",
    },
}
logger.info("Building datapackage...")
dp = DataPackage.build_datapackage(
    adapter=adapter,
    process_adapter_map=process_adapter_map,
    parameter_map=parameter_map,
)
datapackage_path = pathlib.Path(__file__).parent / "datapackage"
dp.save_datapackage_to_csv(str(datapackage_path))


logger.info("Building EnergySystem")
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
    },
)

logger.info("Building Model...")
m = Model(es)
logger.info("Solving Model...")
m.solve(solver="cbc")
logger.warning(m.solver_results["Solver"][0]["Termination condition"])
print(m.solver_results["Solver"][0]["Termination condition"])
logger.info("Reding Results")
results = processing.results(m)
logger.info("Writing Results and Goodbye :)")
