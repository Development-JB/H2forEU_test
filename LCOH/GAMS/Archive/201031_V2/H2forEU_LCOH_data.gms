
Parameter p_res_profile(TIMESTEP, ENERGY_TYPE);
$gdxin gdx/p_res_profile.gdx
$load p_res_profile = p_res_profile
$gdxin

Parameter p_timestep_weighting(TIMESTEP);
$gdxin gdx/p_timestep_weighting.gdx
$load p_timestep_weighting = p_timestep_weighting
$gdxin

Parameter p_wacc(YEAR);
$gdxin gdx/p_wacc.gdx
$load p_wacc = p_wacc
$gdxin

Parameter p_capex(YEAR, TECHNOLOGY);
$gdxin gdx/p_capex.gdx
$load p_capex = p_capex
$gdxin

Parameter p_opex(YEAR, TECHNOLOGY);
$gdxin gdx/p_opex.gdx
$load p_opex = p_opex
$gdxin

Parameter p_lifetime(YEAR, TECHNOLOGY);
$gdxin gdx/p_lifetime.gdx
$load p_lifetime = p_lifetime
$gdxin


Parameter p_capacity(ENERGY_TYPE);
Parameter p_LCOH