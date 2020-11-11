**********************************
*** Variables
**********************************
Variables
v_CostSupply
;

Positive Variables
v_CostTotal(YEAR)
v_CostTransport(YEAR)
v_CostProduction(YEAR)
v_CostTotalDummy(YEAR)
v_Path(YEAR, PATH)
v_ProductionNode(YEAR, NODE_PRODUCTION)
v_ProductionH2System(YEAR, H2_SYSTEM)
v_ProductionDummy(YEAR, NODE_IMPORT)

v_CostTransportNational(YEAR)
v_CostTransportInternational(YEAR)
v_CostTransportConversion(YEAR)
;


**********************************
*** Equation
**********************************
Equations
e_Objective
e_CostTotal(YEAR)
e_CostProduction(YEAR)
e_CostDummy(YEAR)
e_CostTransport(YEAR)

e_CostTransportNational(YEAR)
e_CostTransportInternational(YEAR)
e_CostTransportConversion(YEAR)

    

e_Demand(YEAR, NODE_IMPORT)

e_LinkNodeProductionPath(YEAR, NODE_PRODUCTION)
e_LinkH2SystemNodeProduction(YEAR, NODE_PRODUCTION)

*e_Production(YEAR, NODE_PRODUCTION)
e_ProductionLimitVolumesNode(YEAR, NODE_PRODUCTION, ENERGY_TYPE)
e_ProductionLimitAreaNode(YEAR, NODE_PRODUCTION)
e_ProductionLimitCountry(YEAR, COUNTRY, ENERGY_TYPE)

*e_Transport(YEAR)
e_TransportLimitImport(YEAR, NODE_IMPORT, TRANSPORT_INTERNATIONAL)
e_TransportLimitInternational(YEAR, NODE_EXPORT, NODE_IMPORT, TRANSPORT_INTERNATIONAL)

;

    
**********************************
*** OBJECTIVE & COSTS
**********************************
e_Objective..
    v_CostSupply
    =e=
    sum((i_YEAR(YEAR)), v_CostTotal(YEAR))
;

*** Cost functions
e_CostTotal(i_YEAR(YEAR))..
    v_CostTotal(YEAR)
    =e=
    + v_CostTransport(YEAR)
    + v_CostProduction(YEAR)
    + v_CostTotalDummy(YEAR)
;

e_CostDummy(i_YEAR(YEAR))..
    v_CostTotalDummy(YEAR)
    =e=
    sum((NODE_IMPORT), v_ProductionDummy(YEAR, NODE_IMPORT)*1000000)
;

e_CostProduction(i_YEAR(YEAR))..
    v_CostProduction(YEAR)
    =e=
    sum((H2_SYSTEM), v_ProductionH2System(YEAR, H2_SYSTEM) * p_production_cost(YEAR, H2_SYSTEM))
;
    
e_CostTransport(i_YEAR(YEAR))..
    v_CostTransport(YEAR)
    =e=
    + v_CostTransportNational(YEAR)
    + v_CostTransportInternational(YEAR)
    + v_CostTransportConversion(YEAR)
*    + sum((PATH, NODE_PRODUCTION, TRANSPORT_NATIONAL, NODE_EXPORT)
*         $(LINK_PATH_NODE_PRODUCTION(PATH,NODE_PRODUCTION) and LINK_PATH_TRANSPORT_NATIONAL(PATH,TRANSPORT_NATIONAL) and LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)),
*         v_Path(YEAR, PATH)*p_transport_national_cost_variable(YEAR, TRANSPORT_NATIONAL)+p_transport_national_distance(NODE_PRODUCTION, NODE_EXPORT,TRANSPORT_NATIONAL)*p_transport_national_cost_fixed(YEAR, TRANSPORT_NATIONAL))
*    + sum((PATH, NODE_EXPORT, TRANSPORT_INTERNATIONAL, NODE_IMPORT)
*         $(LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL)and LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT)),
*         v_Path(YEAR, PATH)*p_transport_international_cost_variable(YEAR, TRANSPORT_INTERNATIONAL)+p_transport_international_distance(NODE_EXPORT, NODE_IMPORT,TRANSPORT_INTERNATIONAL)*p_transport_international_cost_fixed(YEAR, TRANSPORT_INTERNATIONAL))
*    + sum((PATH, TRANSPORT_CONVERSION)
*         $(LINK_PATH_CONVERSION(PATH,TRANSPORT_CONVERSION)),
*         v_Path(YEAR, PATH)*p_transport_conversion_cost(YEAR, TRANSPORT_CONVERSION))
;

e_CostTransportNational(i_YEAR(YEAR))..
    v_CostTransportNational(YEAR)
    =e=
    + sum((PATH, NODE_PRODUCTION, TRANSPORT_NATIONAL, NODE_EXPORT)
    $(LINK_PATH_NODE_PRODUCTION(PATH,NODE_PRODUCTION) and LINK_PATH_TRANSPORT_NATIONAL(PATH,TRANSPORT_NATIONAL) and LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)),
    v_Path(YEAR, PATH)*(p_transport_national_cost_variable(YEAR, TRANSPORT_NATIONAL)+p_transport_national_distance(NODE_PRODUCTION, NODE_EXPORT,TRANSPORT_NATIONAL)*p_transport_national_cost_fixed(YEAR, TRANSPORT_NATIONAL)))
;

e_CostTransportInternational(i_YEAR(YEAR))..
    v_CostTransportInternational(YEAR)
    =e=
    + sum((PATH, NODE_EXPORT, TRANSPORT_INTERNATIONAL, NODE_IMPORT)
    $(LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT)and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL)and LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT)),
    v_Path(YEAR, PATH)*(p_transport_international_cost_variable(YEAR, TRANSPORT_INTERNATIONAL)+p_transport_international_distance(NODE_EXPORT, NODE_IMPORT,TRANSPORT_INTERNATIONAL)*p_transport_international_cost_fixed(YEAR, TRANSPORT_INTERNATIONAL)))
;

e_CostTransportConversion(i_YEAR(YEAR))..
    v_CostTransportConversion(YEAR)
    =e=
    + sum((PATH, TRANSPORT_CONVERSION)
    $(LINK_PATH_CONVERSION(PATH,TRANSPORT_CONVERSION)),
    v_Path(YEAR, PATH)*p_transport_conversion_cost(YEAR, TRANSPORT_CONVERSION))
;

*** General
e_Demand(i_YEAR(YEAR), NODE_IMPORT)..
    sum((TRANSPORT_INTERNATIONAL),p_transport_international_import_capacity(YEAR, NODE_IMPORT, TRANSPORT_INTERNATIONAL))
    =e=
    v_ProductionDummy(YEAR, NODE_IMPORT)
    + sum((PATH)$LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT),v_Path(YEAR, PATH))
;

e_LinkNodeProductionPath(i_YEAR(YEAR), NODE_PRODUCTION)..
    v_ProductionNode(YEAR, NODE_PRODUCTION)
    =e=
    sum((PATH)$(LINK_PATH_NODE_PRODUCTION(PATH,NODE_PRODUCTION)),v_Path(YEAR, PATH))

;

e_LinkH2SystemNodeProduction(i_YEAR(YEAR), NODE_PRODUCTION)..
    v_ProductionNode(YEAR, NODE_PRODUCTION)
    =e=
    sum((H2_SYSTEM)$(LINK_H2_SYSTEM_NODE_PRODUCTION(H2_SYSTEM,NODE_PRODUCTION) and p_production_cost(YEAR, H2_SYSTEM)>0),v_ProductionH2System(YEAR, H2_SYSTEM))
;

*** Transport constraints
e_TransportLimitImport(i_YEAR(YEAR), NODE_IMPORT, TRANSPORT_INTERNATIONAL)..
    p_transport_international_import_capacity(YEAR, NODE_IMPORT, TRANSPORT_INTERNATIONAL)
    =g=
    sum((PATH)$(LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT) and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL)),v_Path(YEAR, PATH))
;

e_TransportLimitInternational(i_YEAR(YEAR), NODE_EXPORT, NODE_IMPORT, TRANSPORT_INTERNATIONAL)..
    p_transport_international_capacity(YEAR, NODE_EXPORT, NODE_IMPORT, TRANSPORT_INTERNATIONAL)
    =g=
    sum((PATH)$(LINK_PATH_NODE_EXPORT(PATH,NODE_EXPORT) and LINK_PATH_TRANSPORT_INTERNATIONAL(PATH,TRANSPORT_INTERNATIONAL) and LINK_PATH_NODE_IMPORT(PATH,NODE_IMPORT)),v_Path(YEAR, PATH))
;

*** Production constraints
e_ProductionLimitVolumesNode(i_YEAR(YEAR), NODE_PRODUCTION, ENERGY_TYPE)..
    p_production_limit_node(YEAR, NODE_PRODUCTION, ENERGY_TYPE)
    =g=
    sum((H2_SYSTEM, SOURCE_NON_VRES)$(LINK_H2_SYSTEM_SOURCE(H2_SYSTEM, SOURCE_NON_VRES) and LINK_H2_SYSTEM_NODE_PRODUCTION(H2_SYSTEM,NODE_PRODUCTION) and LINK_H2_SYSTEM_ENERGY_TYPE(H2_SYSTEM,ENERGY_TYPE)), v_ProductionH2System(YEAR, H2_SYSTEM)*p_production_capacities(YEAR, H2_SYSTEM, ENERGY_TYPE)) 
;

e_ProductionLimitAreaNode(i_YEAR(YEAR), NODE_PRODUCTION)..
    p_production_area_available_node(NODE_PRODUCTION)
    =g=
    sum((H2_SYSTEM, ENERGY_TYPE, SOURCE_VRES)$(LINK_H2_SYSTEM_SOURCE(H2_SYSTEM, SOURCE_VRES)and LINK_H2_SYSTEM_NODE_PRODUCTION(H2_SYSTEM,NODE_PRODUCTION) and LINK_H2_SYSTEM_ENERGY_TYPE(H2_SYSTEM,ENERGY_TYPE)), v_ProductionH2System(YEAR, H2_SYSTEM)*p_production_capacities(YEAR, H2_SYSTEM, ENERGY_TYPE)*p_production_energy_density(ENERGY_TYPE)*p_production_land_dedication(ENERGY_TYPE)) 
;


e_ProductionLimitCountry(i_YEAR(YEAR), COUNTRY, ENERGY_TYPE)..
    p_production_limit_country(YEAR, COUNTRY, ENERGY_TYPE)
    =g=
    sum((H2_SYSTEM)$(LINK_H2_SYSTEM_COUNTRY(H2_SYSTEM,COUNTRY) and LINK_H2_SYSTEM_ENERGY_TYPE(H2_SYSTEM,ENERGY_TYPE)), v_ProductionH2System(YEAR, H2_SYSTEM)*p_production_capacities(YEAR, H2_SYSTEM, ENERGY_TYPE))
;



**********************************
*** Model Definition
**********************************
model H2forEU_SupplyChain /
                e_Objective,
                e_CostTotal,
                e_CostProduction,
                e_CostDummy,
                e_CostTransport,

                e_CostTransportNational,
                e_CostTransportInternational,
                e_CostTransportConversion,
                
                e_Demand,
                e_LinkNodeProductionPath,
                e_LinkH2SystemNodeProduction,
                e_ProductionLimitVolumesNode,
                e_ProductionLimitAreaNode,
                e_ProductionLimitCountry,
                e_TransportLimitImport,
                e_TransportLimitInternational
            /;