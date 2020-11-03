**********************************
*** Variables
**********************************
Variables
v_LCOH
;

Positive Variables
v_Capacity(KEY_SCENARIO,TECHNOLOGY)
v_TotalCost(KEY_SCENARIO)
v_TotalProductionH2(KEY_SCENARIO)
v_GenerationEleSurplus(KEY_SCENARIO, TIMESTEP)
v_GenerationEleInfeed(KEY_SCENARIO, TIMESTEP)
v_TotalGenerationEleInfeed(KEY_SCENARIO)
;
v_Capacity.fx(KEY_SCENARIO,ELECTROLYSER) = 1

**********************************
*** Equation
**********************************
Equations
e_Objective
e_TotalCost(KEY_SCENARIO)
e_TotalProductionH2(KEY_SCENARIO)
e_TotalGenerationEleInfeed(KEY_SCENARIO)
e_GenerationEle(KEY_SCENARIO,TIMESTEP)
e_InfeedLimitEle(KEY_SCENARIO,TIMESTEP)
;

    
**********************************
*** OBJECTIVE & COSTS
**********************************
e_Objective..
    v_LCOH
    =e=
    sum(i_KEY_SCENARIO(KEY_SCENARIO), v_TotalCost(i_KEY_SCENARIO)/(v_TotalProductionH2(i_KEY_SCENARIO)+1))
;


e_TotalCost(i_KEY_SCENARIO(KEY_SCENARIO))..
    v_TotalCost(KEY_SCENARIO)
    =e=
    +sum((YEAR, COUNTRY, TECHNOLOGY)$(LINK_KEY_COUNTRY(i_KEY_SCENARIO,COUNTRY) and LINK_KEY_YEAR(i_KEY_SCENARIO,YEAR) and LINK_KEY_TECHNOLOGY(i_KEY_SCENARIO, TECHNOLOGY)), v_Capacity(KEY_SCENARIO,TECHNOLOGY)*((p_opex(YEAR, TECHNOLOGY) + p_capex(YEAR,TECHNOLOGY)) *(p_wacc(YEAR,COUNTRY) / (1- (1+ p_wacc(YEAR,COUNTRY))**(-1*p_lifetime(YEAR, TECHNOLOGY))))))

*    +sum((YEAR, COUNTRY, TECHNOLOGY)$(LINK_KEY_COUNTRY(i_KEY_SCENARIO,COUNTRY) and LINK_KEY_YEAR(i_KEY_SCENARIO,YEAR) and LINK_KEY_TECHNOLOGY(i_KEY_SCENARIO, TECHNOLOGY)), v_Capacity(KEY_SCENARIO,TECHNOLOGY)*(p_capex(YEAR,TECHNOLOGY)/(1-(1/(1+p_wacc(YEAR,COUNTRY))**p_lifetime(YEAR, TECHNOLOGY)))/p_wacc(YEAR,COUNTRY)+p_opex(YEAR, TECHNOLOGY)))
;


e_TotalProductionH2(i_KEY_SCENARIO(KEY_SCENARIO))..
    v_TotalProductionH2(KEY_SCENARIO)
    =e=
    sum((YEAR, ELECTROLYSER)$(LINK_KEY_TECHNOLOGY(i_KEY_SCENARIO, ELECTROLYSER) and LINK_KEY_YEAR(i_KEY_SCENARIO,YEAR)),v_TotalGenerationEleInfeed(KEY_SCENARIO)*p_efficiency(YEAR, ELECTROLYSER)*1000/33.33)
*    sum((CELL, SYSTEMS, TIMESTEP)$(LINK_KEY_CELL(i_KEY_SCENARIO,CELL) and LINK_KEY_SYSTEM(i_KEY_SCENARIO,SYSTEMS) and LINK_KEY_TIMESTEP(i_KEY_SCENARIO,TIMESTEP)), v_GenerationEle(KEY_SCENARIO, TIMESTEP)*0.67)*30.03
;

e_GenerationEle(i_KEY_SCENARIO(KEY_SCENARIO), TIMESTEP)$LINK_KEY_TIMESTEP(i_KEY_SCENARIO,TIMESTEP)..
    v_GenerationEleInfeed(KEY_SCENARIO, TIMESTEP)+v_GenerationEleSurplus(KEY_SCENARIO, TIMESTEP)
    =e=
    sum((ENERGY_TYPE,CELL,SYSTEMS)$(LINK_KEY_ENERGY_TYPE(i_KEY_SCENARIO,ENERGY_TYPE) and LINK_KEY_CELL(i_KEY_SCENARIO,CELL)and LINK_KEY_SYSTEM(i_KEY_SCENARIO,SYSTEMS)), v_Capacity(KEY_SCENARIO,ENERGY_TYPE)*p_res_profile(TIMESTEP, CELL,SYSTEMS, ENERGY_TYPE))
;

e_TotalGenerationEleInfeed(i_KEY_SCENARIO(KEY_SCENARIO))..
    v_TotalGenerationEleInfeed(KEY_SCENARIO)
    =e=
    sum((CELL, SYSTEMS, TIMESTEP)$(LINK_KEY_CELL(i_KEY_SCENARIO,CELL) and LINK_KEY_SYSTEM(i_KEY_SCENARIO,SYSTEMS) and LINK_KEY_TIMESTEP(i_KEY_SCENARIO,TIMESTEP)), v_GenerationEleInfeed(KEY_SCENARIO, TIMESTEP)*p_timestep_weighting(TIMESTEP,CELL,SYSTEMS))
;

e_InfeedLimitEle(i_KEY_SCENARIO(KEY_SCENARIO),TIMESTEP)$LINK_KEY_TIMESTEP(i_KEY_SCENARIO,TIMESTEP)..
    v_GenerationEleInfeed(KEY_SCENARIO, TIMESTEP)
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
            e_TotalGenerationEleInfeed,
            e_InfeedLimitEle
            /;