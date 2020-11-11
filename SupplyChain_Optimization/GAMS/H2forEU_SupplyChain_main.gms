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
    
    r_CostTotal(i_YEAR) = v_CostTotal.l(i_YEAR);
    r_CostTransport(i_YEAR) = v_CostTransport.l(i_YEAR);
    r_CostTransportNational(i_YEAR) = v_CostTransportNational.l(i_YEAR);
    r_CostTransportInternational(i_YEAR) = v_CostTransportInternational.l(i_YEAR);
    r_CostTransportConversion(i_YEAR)= v_CostTransportConversion.l(i_YEAR);
    r_CostProduction(i_YEAR) = v_CostProduction.l(i_YEAR);
    r_CostTotalDummy(i_YEAR) = v_CostTotalDummy.l(i_YEAR);
    r_Path(i_YEAR, PATH) = v_Path.l(i_YEAR, PATH);
    r_ProductionNode(i_YEAR, NODE_PRODUCTION) = v_ProductionNode.l(i_YEAR, NODE_PRODUCTION);
    r_ProductionH2System(i_YEAR, H2_SYSTEM) = v_ProductionH2System.l(i_YEAR, H2_SYSTEM);
    r_ProductionDummy(i_YEAR, NODE_IMPORT) = v_ProductionDummy.l(i_YEAR, NODE_IMPORT);
    
*    r_capacity(i_KEY_SCENARIO, TECHNOLOGY) = v_Capacity.l(i_KEY_SCENARIO,TECHNOLOGY);

)


$INCLUDE H2forEU_SupplyChain_output.gms

