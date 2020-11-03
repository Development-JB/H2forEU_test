**********************************
*** Variables
**********************************
Variables
v_LCOH
;

Positive Variables
v_CapacityRes(ENERGY_TYPE)
v_TotalCost
v_TotalProductionH2
v_GenerationEle
;

**********************************
*** Equation
**********************************
Equations
e_Objective
e_TotalCost
e_TotalProductionH2
e_GenerationEle(TIMESTEP_HOUR)
e_GenerationLimitEle(TIMESTEP_HOUR)
;

    
**********************************
*** OBJECTIVE & COSTS
**********************************
e_Objective..
    v_LCOH
    =e=
    v_TotalCost/(v_TotalProductionH2+1)
;

e_TotalCost..
    v_TotalCost
    =e=
    +p_electrolyer_capex/(1-(1/((1+p_wacc)**p_electrolyer_lifetime)))/p_wacc+p_electrolyer_opex
    +sum((ENERGY_TYPE), v_CapacityRes(ENERGY_TYPE)*(p_res_capex(ENERGY_TYPE)/(1-(1/(1+p_wacc)**p_res_lifetime(ENERGY_TYPE)))/p_wacc+p_res_opex(ENERGY_TYPE)))
;

e_TotalProductionH2..
    v_TotalProductionH2/0.0333
    =e=
    sum((TIMESTEP_HOUR), v_GenerationEle(TIMESTEP_HOUR)*0.67)
;


e_GenerationEle(TIMESTEP_HOUR)..
    v_GenerationEle(TIMESTEP_HOUR)
    =e=
    sum((ENERGY_TYPE), v_CapacityRes(ENERGY_TYPE)*p_res_profile(TIMESTEP_HOUR,ENERGY_TYPE))
;

e_GenerationLimitEle(TIMESTEP_HOUR)..
    v_GenerationEle(TIMESTEP_HOUR)
    =l=
    1
;


**********************************
*** Model Definition
**********************************
model H2forEU_LCOH /
            e_Objective,
            e_TotalCost,
            e_TotalProductionH2,
            e_GenerationEle,
            e_GenerationLimitEle
            /;