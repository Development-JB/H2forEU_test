**********************************
*** MODEL SETTINGS
**********************************
$ontext
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
$offtext


**********************************
*** LOAD FILES and MODEL
**********************************
$INCLUDE H2forEU_SupplyChain_setup.gms
$INCLUDE H2forEU_SupplyChain_data.gms

$INCLUDE H2forEU_SupplyChain_model.gms


display p_production_limit_node

loop(ITERATION,

    i_YEAR(YEAR)$LINK_ITERATION_YEAR(ITERATION,YEAR) = yes;
    i_YEAR(YEAR)$(NOT LINK_ITERATION_YEAR(ITERATION,YEAR)) = no;


    display i_YEAR
    display p_production_limit_node
    
    solve H2forEU_SupplyChain using lp minimizing v_CostSupply;
    
*    display v_Path.l;
*    display v_ProductionH2System.l;
*    display v_ProductionDummy.l;
    
*    r_capacity(i_KEY_SCENARIO, TECHNOLOGY) = v_Capacity.l(i_KEY_SCENARIO,TECHNOLOGY);

)


$INCLUDE H2forEU_SupplyChain_output.gms

