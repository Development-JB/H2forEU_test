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
*    r_Path(i_YEAR, PATH) = v_Path.l(i_YEAR, PATH);
    r_ProductionNode(i_YEAR, NODE_PRODUCTION) = v_ProductionNode.l(i_YEAR, NODE_PRODUCTION);
    r_ProductionH2System(i_YEAR, H2_SYSTEM) = v_ProductionH2System.l(i_YEAR, H2_SYSTEM);
    r_ProductionDummy(i_YEAR, NODE_IMPORT) = v_ProductionDummy.l(i_YEAR, NODE_IMPORT);
    
*    r_capacity(i_KEY_SCENARIO, TECHNOLOGY) = v_Capacity.l(i_KEY_SCENARIO,TECHNOLOGY);

    r_H2_system(i_YEAR, H2_SYSTEM, COUNTRY, NODE_PRODUCTION, SOURCE, ENERGY_TYPE, TECHNOLOGY)
                                          $(LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_NODE_PRODUCTION(H2_SYSTEM,NODE_PRODUCTION)
                                        and LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_TECHNOLOGY(H2_SYSTEM,TECHNOLOGY)
                                        and LINK_H2_SYSTEM_SOURCE(H2_SYSTEM,SOURCE)
                                        and LINK_H2_SYSTEM_ENERGY_TYPE(H2_SYSTEM,ENERGY_TYPE))
                                        = v_ProductionH2System.l(i_YEAR, H2_SYSTEM);
  
    r_Path(i_YEAR, PATH, Node_PRODUCTION, TRANSPORT_NATIONAL, NODE_EXPORT, TRANSPORT_INTERNATIONAL, NODE_IMPORT)
                                          $(LINK_PATH_NODE_PRODUCTION(PATH,NODE_PRODUCTION)
                                        and LINK_PATH_TRANSPORT_NATIONAL(PATH,TRANSPORT_NATIONAL)
                                        and LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)
                                        and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL)
                                        and LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT))
                                        = v_Path.l(i_YEAR, PATH);
    
    r_Supply(i_YEAR, H2_SYSTEM, PATH, COUNTRY, SOURCE, ENERGY_TYPE, TECHNOLOGY, Node_PRODUCTION, TRANSPORT_NATIONAL, NODE_EXPORT, TRANSPORT_INTERNATIONAL, NODE_IMPORT, TRANSPORT_CONVERSION)
                                          $(LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_NODE_PRODUCTION(H2_SYSTEM,NODE_PRODUCTION)
                                        and LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_TECHNOLOGY(H2_SYSTEM,TECHNOLOGY)
                                        and LINK_H2_SYSTEM_SOURCE(H2_SYSTEM,SOURCE)
                                        and LINK_H2_SYSTEM_ENERGY_TYPE(H2_SYSTEM,ENERGY_TYPE)
                                        and LINK_PATH_NODE_PRODUCTION(PATH,NODE_PRODUCTION)
                                        and LINK_PATH_TRANSPORT_NATIONAL(PATH,TRANSPORT_NATIONAL)
                                        and LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)
                                        and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL)
                                        and LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT)
                                        and LINK_PATH_CONVERSION(PATH,TRANSPORT_CONVERSION))
                                        = v_Path.l(i_YEAR, PATH)/v_ProductionNode.l(i_YEAR, NODE_PRODUCTION)*v_ProductionH2System.l(i_YEAR, H2_SYSTEM)*p_production_volume(i_YEAR, H2_SYSTEM);    

    r_Supply_TotalCostProduction(i_YEAR, H2_SYSTEM, PATH, COUNTRY, SOURCE, ENERGY_TYPE, TECHNOLOGY, Node_PRODUCTION, TRANSPORT_NATIONAL, NODE_EXPORT, TRANSPORT_INTERNATIONAL, NODE_IMPORT, TRANSPORT_CONVERSION)
                                          $(LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_NODE_PRODUCTION(H2_SYSTEM,NODE_PRODUCTION)
                                        and LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_TECHNOLOGY(H2_SYSTEM,TECHNOLOGY)
                                        and LINK_H2_SYSTEM_SOURCE(H2_SYSTEM,SOURCE)
                                        and LINK_H2_SYSTEM_ENERGY_TYPE(H2_SYSTEM,ENERGY_TYPE)
                                        and LINK_PATH_NODE_PRODUCTION(PATH,NODE_PRODUCTION)
                                        and LINK_PATH_TRANSPORT_NATIONAL(PATH,TRANSPORT_NATIONAL)
                                        and LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)
                                        and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL)
                                        and LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT)
                                        and LINK_PATH_CONVERSION(PATH,TRANSPORT_CONVERSION))
                                        = v_ProductionH2System.l(i_YEAR, H2_SYSTEM) * p_production_volume(i_YEAR, H2_SYSTEM) * p_production_cost(i_YEAR, H2_SYSTEM);    

    r_Supply_TotalCostTransportNational(i_YEAR, H2_SYSTEM, PATH, COUNTRY, SOURCE, ENERGY_TYPE, TECHNOLOGY, Node_PRODUCTION, TRANSPORT_NATIONAL, NODE_EXPORT, TRANSPORT_INTERNATIONAL, NODE_IMPORT, TRANSPORT_CONVERSION)
                                          $(LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_NODE_PRODUCTION(H2_SYSTEM,NODE_PRODUCTION)
                                        and LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_TECHNOLOGY(H2_SYSTEM,TECHNOLOGY)
                                        and LINK_H2_SYSTEM_SOURCE(H2_SYSTEM,SOURCE)
                                        and LINK_H2_SYSTEM_ENERGY_TYPE(H2_SYSTEM,ENERGY_TYPE)
                                        and LINK_PATH_NODE_PRODUCTION(PATH,NODE_PRODUCTION)
                                        and LINK_PATH_TRANSPORT_NATIONAL(PATH,TRANSPORT_NATIONAL)
                                        and LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)
                                        and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL)
                                        and LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT)
                                        and LINK_PATH_CONVERSION(PATH,TRANSPORT_CONVERSION))
                                        = v_ProductionH2System.l(i_YEAR, H2_SYSTEM) * p_production_volume(i_YEAR, H2_SYSTEM)*(p_transport_national_cost_variable(i_YEAR, TRANSPORT_NATIONAL)+p_transport_national_distance(NODE_PRODUCTION, NODE_EXPORT,TRANSPORT_NATIONAL)*p_transport_national_cost_fixed(i_YEAR, TRANSPORT_NATIONAL));

    r_Supply_TotalCostTransportInternational(i_YEAR, H2_SYSTEM, PATH, COUNTRY, SOURCE, ENERGY_TYPE, TECHNOLOGY, Node_PRODUCTION, TRANSPORT_NATIONAL, NODE_EXPORT, TRANSPORT_INTERNATIONAL, NODE_IMPORT, TRANSPORT_CONVERSION)
                                          $(LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_NODE_PRODUCTION(H2_SYSTEM,NODE_PRODUCTION)
                                        and LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_TECHNOLOGY(H2_SYSTEM,TECHNOLOGY)
                                        and LINK_H2_SYSTEM_SOURCE(H2_SYSTEM,SOURCE)
                                        and LINK_H2_SYSTEM_ENERGY_TYPE(H2_SYSTEM,ENERGY_TYPE)
                                        and LINK_PATH_NODE_PRODUCTION(PATH,NODE_PRODUCTION)
                                        and LINK_PATH_TRANSPORT_NATIONAL(PATH,TRANSPORT_NATIONAL)
                                        and LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)
                                        and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL)
                                        and LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT)
                                        and LINK_PATH_CONVERSION(PATH,TRANSPORT_CONVERSION))
                                        = v_ProductionH2System.l(i_YEAR, H2_SYSTEM) * p_production_volume(i_YEAR, H2_SYSTEM)*(p_transport_international_cost_variable(i_YEAR, TRANSPORT_INTERNATIONAL)+p_transport_international_distance(NODE_EXPORT, NODE_IMPORT,TRANSPORT_INTERNATIONAL)*p_transport_international_cost_fixed(i_YEAR, TRANSPORT_INTERNATIONAL));

    r_Supply_TotalCostTransportInternational(i_YEAR, H2_SYSTEM, PATH, COUNTRY, SOURCE, ENERGY_TYPE, TECHNOLOGY, Node_PRODUCTION, TRANSPORT_NATIONAL, NODE_EXPORT, TRANSPORT_INTERNATIONAL, NODE_IMPORT, TRANSPORT_CONVERSION)
                                          $(LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_NODE_PRODUCTION(H2_SYSTEM,NODE_PRODUCTION)
                                        and LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_TECHNOLOGY(H2_SYSTEM,TECHNOLOGY)
                                        and LINK_H2_SYSTEM_SOURCE(H2_SYSTEM,SOURCE)
                                        and LINK_H2_SYSTEM_ENERGY_TYPE(H2_SYSTEM,ENERGY_TYPE)
                                        and LINK_PATH_NODE_PRODUCTION(PATH,NODE_PRODUCTION)
                                        and LINK_PATH_TRANSPORT_NATIONAL(PATH,TRANSPORT_NATIONAL)
                                        and LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)
                                        and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL)
                                        and LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT)
                                        and LINK_PATH_CONVERSION(PATH,TRANSPORT_CONVERSION))
                                        = v_ProductionH2System.l(i_YEAR, H2_SYSTEM) * p_production_volume(i_YEAR, H2_SYSTEM)*p_transport_conversion_cost(i_YEAR, TRANSPORT_CONVERSION);


    r_Supply_CostProduction(i_YEAR, H2_SYSTEM, PATH, COUNTRY, SOURCE, ENERGY_TYPE, TECHNOLOGY, Node_PRODUCTION, TRANSPORT_NATIONAL, NODE_EXPORT, TRANSPORT_INTERNATIONAL, NODE_IMPORT, TRANSPORT_CONVERSION)
                                          $(LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_NODE_PRODUCTION(H2_SYSTEM,NODE_PRODUCTION)
                                        and LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_TECHNOLOGY(H2_SYSTEM,TECHNOLOGY)
                                        and LINK_H2_SYSTEM_SOURCE(H2_SYSTEM,SOURCE)
                                        and LINK_H2_SYSTEM_ENERGY_TYPE(H2_SYSTEM,ENERGY_TYPE)
                                        and LINK_PATH_NODE_PRODUCTION(PATH,NODE_PRODUCTION)
                                        and LINK_PATH_TRANSPORT_NATIONAL(PATH,TRANSPORT_NATIONAL)
                                        and LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)
                                        and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL)
                                        and LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT)
                                        and LINK_PATH_CONVERSION(PATH,TRANSPORT_CONVERSION)
                                        and v_ProductionH2System.l(i_YEAR, H2_SYSTEM)>0)
                                        = v_ProductionH2System.l(i_YEAR, H2_SYSTEM) * p_production_volume(i_YEAR, H2_SYSTEM) * p_production_cost(i_YEAR, H2_SYSTEM)
                                        / (v_ProductionH2System.l(i_YEAR, H2_SYSTEM) * p_production_volume(i_YEAR, H2_SYSTEM));    

    r_Supply_CostTransportNational(i_YEAR, H2_SYSTEM, PATH, COUNTRY, SOURCE, ENERGY_TYPE, TECHNOLOGY, Node_PRODUCTION, TRANSPORT_NATIONAL, NODE_EXPORT, TRANSPORT_INTERNATIONAL, NODE_IMPORT, TRANSPORT_CONVERSION)
                                          $(LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_NODE_PRODUCTION(H2_SYSTEM,NODE_PRODUCTION)
                                        and LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_TECHNOLOGY(H2_SYSTEM,TECHNOLOGY)
                                        and LINK_H2_SYSTEM_SOURCE(H2_SYSTEM,SOURCE)
                                        and LINK_H2_SYSTEM_ENERGY_TYPE(H2_SYSTEM,ENERGY_TYPE)
                                        and LINK_PATH_NODE_PRODUCTION(PATH,NODE_PRODUCTION)
                                        and LINK_PATH_TRANSPORT_NATIONAL(PATH,TRANSPORT_NATIONAL)
                                        and LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)
                                        and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL)
                                        and LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT)
                                        and LINK_PATH_CONVERSION(PATH,TRANSPORT_CONVERSION)
                                        and v_ProductionH2System.l(i_YEAR, H2_SYSTEM)>0)
                                        = v_ProductionH2System.l(i_YEAR, H2_SYSTEM) * p_production_volume(i_YEAR, H2_SYSTEM)*(p_transport_national_cost_variable(i_YEAR, TRANSPORT_NATIONAL)+p_transport_national_distance(NODE_PRODUCTION, NODE_EXPORT,TRANSPORT_NATIONAL)*p_transport_national_cost_fixed(i_YEAR, TRANSPORT_NATIONAL))
                                        / v_ProductionH2System.l(i_YEAR, H2_SYSTEM) * p_production_volume(i_YEAR, H2_SYSTEM);

    r_Supply_CostTransportInternational(i_YEAR, H2_SYSTEM, PATH, COUNTRY, SOURCE, ENERGY_TYPE, TECHNOLOGY, Node_PRODUCTION, TRANSPORT_NATIONAL, NODE_EXPORT, TRANSPORT_INTERNATIONAL, NODE_IMPORT, TRANSPORT_CONVERSION)
                                          $(LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_NODE_PRODUCTION(H2_SYSTEM,NODE_PRODUCTION)
                                        and LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_TECHNOLOGY(H2_SYSTEM,TECHNOLOGY)
                                        and LINK_H2_SYSTEM_SOURCE(H2_SYSTEM,SOURCE)
                                        and LINK_H2_SYSTEM_ENERGY_TYPE(H2_SYSTEM,ENERGY_TYPE)
                                        and LINK_PATH_NODE_PRODUCTION(PATH,NODE_PRODUCTION)
                                        and LINK_PATH_TRANSPORT_NATIONAL(PATH,TRANSPORT_NATIONAL)
                                        and LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)
                                        and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL)
                                        and LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT)
                                        and LINK_PATH_CONVERSION(PATH,TRANSPORT_CONVERSION)
                                        and v_ProductionH2System.l(i_YEAR, H2_SYSTEM)>0)
                                        = v_ProductionH2System.l(i_YEAR, H2_SYSTEM) * p_production_volume(i_YEAR, H2_SYSTEM)*(p_transport_international_cost_variable(i_YEAR, TRANSPORT_INTERNATIONAL)+p_transport_international_distance(NODE_EXPORT, NODE_IMPORT,TRANSPORT_INTERNATIONAL)*p_transport_international_cost_fixed(i_YEAR, TRANSPORT_INTERNATIONAL))
                                        / v_ProductionH2System.l(i_YEAR, H2_SYSTEM) * p_production_volume(i_YEAR, H2_SYSTEM);

    r_Supply_CostTransportInternational(i_YEAR, H2_SYSTEM, PATH, COUNTRY, SOURCE, ENERGY_TYPE, TECHNOLOGY, Node_PRODUCTION, TRANSPORT_NATIONAL, NODE_EXPORT, TRANSPORT_INTERNATIONAL, NODE_IMPORT, TRANSPORT_CONVERSION)
                                          $(LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_NODE_PRODUCTION(H2_SYSTEM,NODE_PRODUCTION)
                                        and LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY)
                                        and LINK_H2_SYSTEM_TECHNOLOGY(H2_SYSTEM,TECHNOLOGY)
                                        and LINK_H2_SYSTEM_SOURCE(H2_SYSTEM,SOURCE)
                                        and LINK_H2_SYSTEM_ENERGY_TYPE(H2_SYSTEM,ENERGY_TYPE)
                                        and LINK_PATH_NODE_PRODUCTION(PATH,NODE_PRODUCTION)
                                        and LINK_PATH_TRANSPORT_NATIONAL(PATH,TRANSPORT_NATIONAL)
                                        and LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)
                                        and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL)
                                        and LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT)
                                        and LINK_PATH_CONVERSION(PATH,TRANSPORT_CONVERSION)
                                        and v_ProductionH2System.l(i_YEAR, H2_SYSTEM)>0)
                                        = v_ProductionH2System.l(i_YEAR, H2_SYSTEM) * p_production_volume(i_YEAR, H2_SYSTEM)*p_transport_conversion_cost(i_YEAR, TRANSPORT_CONVERSION)
                                        / v_ProductionH2System.l(i_YEAR, H2_SYSTEM) * p_production_volume(i_YEAR, H2_SYSTEM);


)


$INCLUDE H2forEU_SupplyChain_output.gms

