PARAMETER_MAP_STEEL = {
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
        "capacity": "capacity_p_inst",
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
        "fixed_costs": "cost_fix_w",
        "loss_rate": "sto_self_discharge",
        "storage_capacity_cost": "cost_inv_e",
        "fixed_costs": "cost_fix_p",
        "marginal_cost": "cost_var_e",
    },
    "x2x_storage_hydrogen_new_1": {
        "efficiency": "efficiency_sto_in",
        "loss_rate": "sto_self_discharge",
        "storage_capacity_cost": "cost_inv_e",
        "fixed_costs": "cost_fix_w",
        "fixed_costs": "cost_fix_p",
        "marginal_cost": "cost_var_e",
        "capacity_capacity_potential": "capacity_e_max",
    },
    "x2x_storage_hydrogen_retrofit_1": {
        "efficiency": "efficiency_sto_in",
        "fixed_costs": "cost_fix_p",
        "loss_rate": "sto_self_discharge",
        "storage_capacity_cost": "cost_inv_e",
        "fixed_costs": "cost_fix_p",
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
    "helper_source_exo_steel": {
        "marginal_cost": "cost_var_w",
    },
}
