
$gdxin gdx/set.gdx
SET TIMESTEP_HOUR;
$load TIMESTEP_HOUR
display TIMESTEP_HOUR

Parameter p_onshore_profile(TIMESTEP_HOUR);
$gdxin gdx/p_onshore_profile.gdx
$load p_onshore_profile = p_onshore_profile
$gdxin

Parameter p_pv_profile(TIMESTEP_HOUR);
$gdxin gdx/p_pv_profile.gdx
$load p_pv_profile = p_pv_profile
$gdxin

Parameter p_wacc;
$gdxin gdx/p_wacc.gdx
$load p_wacc = p_wacc
$gdxin

Parameter p_pv_capex;
$gdxin gdx/p_pv_capex.gdx
$load p_pv_capex = p_pv_capex
$gdxin

Parameter p_pv_opex;
$gdxin gdx/p_pv_opex.gdx
$load p_pv_opex = p_pv_opex
$gdxin

Parameter p_pv_lifetime;
$gdxin gdx/p_pv_lifetime.gdx
$load p_pv_lifetime = p_pv_lifetime
$gdxin

Parameter p_onshore_capex;
$gdxin gdx/p_onshore_capex.gdx
$load p_onshore_capex = p_onshore_capex
$gdxin

Parameter p_onshore_opex;
$gdxin gdx/p_onshore_opex.gdx
$load p_onshore_opex = p_onshore_opex
$gdxin

Parameter p_onshore_lifetime;
$gdxin gdx/p_onshore_lifetime.gdx
$load p_onshore_lifetime = p_onshore_lifetime
$gdxin

Parameter p_electrolyer_capex;
$gdxin gdx/p_electrolyer_capex.gdx
$load p_electrolyer_capex = p_electrolyer_capex
$gdxin

Parameter p_electrolyer_opex;
$gdxin gdx/p_electrolyer_opex.gdx
$load p_electrolyer_opex = p_electrolyer_opex
$gdxin

Parameter p_electrolyer_lifetime;
$gdxin gdx/p_electrolyer_lifetime.gdx
$load p_electrolyer_lifetime = p_electrolyer_lifetime
$gdxin

execute_unload 'gdx/00_results.gdx'
TIMESTEP_HOUR
p_onshore_profile
p_pv_profile
p_wacc
p_pv_capex
p_pv_opex
p_pv_lifetime
p_onshore_capex
p_onshore_opex
p_onshore_lifetime
p_electrolyer_capex
p_electrolyer_opex
p_electrolyer_lifetime