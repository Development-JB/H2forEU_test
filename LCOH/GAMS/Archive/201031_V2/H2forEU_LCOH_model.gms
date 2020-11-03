**********************************
*** Variables
**********************************
Variables
v_LCOH
;

Positive Variables
v_Capacity(TECHNOLOGY)
v_TotalCost
v_TotalProductionH2
v_GenerationEle
;
v_Capacity.fx(ELECTROLYSER) = 1

**********************************
*** Equation
**********************************
Equations
e_Objective
e_TotalCost
e_TotalProductionH2
e_GenerationEle(TIMESTEP)
e_GenerationLimitEle(TIMESTEP)
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
    +sum((YEAR, TECHNOLOGY), v_Capacity(TECHNOLOGY)*(p_capex(YEAR,TECHNOLOGY)/(1-(1/(1+p_wacc(YEAR))**p_lifetime(YEAR, TECHNOLOGY)))/p_wacc(YEAR)+p_opex(YEAR, TECHNOLOGY)))
;

e_TotalProductionH2..
    v_TotalProductionH2/0.0333
    =e=
    sum((TIMESTEP), v_GenerationEle(TIMESTEP)*0.67)
;


e_GenerationEle(TIMESTEP)..
    v_GenerationEle(TIMESTEP)
    =e=
    sum((ENERGY_TYPE), v_Capacity(ENERGY_TYPE)*p_res_profile(TIMESTEP,ENERGY_TYPE))*p_timestep_weighting(TIMESTEP)
;

e_GenerationLimitEle(TIMESTEP)..
    v_GenerationEle(TIMESTEP)
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