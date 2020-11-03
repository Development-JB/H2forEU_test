**********************************
*** MODEL SETTINGS
**********************************
*$ontext
$TITLE    REDUCED OUTPUT 
$inlinecom /* */

/* Turn off the listing of the input file */
$offlisting

/* Turn off the listing and cross-reference of the symbols used */
$offsymxref offsymlist

option
    limrow = 0,     
    limcol = 0, 
    solprint = off,    
    sysout = off; 
*$offtext

**********************************
*** LOAD FILES and MODEL
**********************************
$INCLUDE H2forEU_LCOH_setup.gms
$INCLUDE H2forEU_LCOH_data.gms

$INCLUDE H2forEU_LCOH_model.gms

loop(ITERATION,

    i_KEY_SCENARIO(KEY_SCENARIO)$LINK_ITERATION_KEY(ITERATION,KEY_SCENARIO) = yes;
    i_KEY_SCENARIO(KEY_SCENARIO)$(NOT LINK_ITERATION_KEY(ITERATION,KEY_SCENARIO)) = no;


    display i_KEY_SCENARIO
    
    solve H2forEU_LCOH using nlp minimizing v_LCOH;
    
*    display v_Capacity.l, v_LCOH.l, v_TotalProductionH2.l, v_TotalGenerationEleInfeed.l, v_TotalCost.l;
    
    r_capacity(i_KEY_SCENARIO, TECHNOLOGY) = v_Capacity.l(i_KEY_SCENARIO,TECHNOLOGY);
    r_TotalProductionH2(i_KEY_SCENARIO) = v_TotalProductionH2.l(i_KEY_SCENARIO);
*    r_TotalCost(i_KEY_SCENARIO) = v_TotalCost.l(i_KEY_SCENARIO);
    r_LCOH(i_KEY_SCENARIO) = v_LCOH.l

)


$INCLUDE H2forEU_LCOH_output.gms

