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

*option
*    limrow = 12;   
    

**********************************
*** LOAD FILES and MODEL
**********************************
$INCLUDE H2forEU_SupplyChain_setup.gms
$INCLUDE H2forEU_SupplyChain_data.gms
$INCLUDE H2forEU_SupplyChain_model.gms


loop(ITERATION,

    i_YEAR(YEAR)$LINK_ITERATION_YEAR(ITERATION,YEAR) = yes;
    i_YEAR(YEAR)$(NOT LINK_ITERATION_YEAR(ITERATION,YEAR)) = no;


    display i_YEAR
    
    solve H2forEU_SupplyChain using lp minimizing v_CostSupply;
 
    r_CostTotal(i_YEAR) = v_CostTotal.l(i_YEAR);
    r_CostTransport(i_YEAR) = v_CostTransport.l(i_YEAR);
    r_CostTransportNational(i_YEAR) = v_CostTransportNational.l(i_YEAR);
    r_CostTransportInternational(i_YEAR) = v_CostTransportInternational.l(i_YEAR);
    r_CostTransportConversion(i_YEAR) = v_CostTransportConversion.l(i_YEAR);
    r_CostProduction(i_YEAR) = v_CostProduction.l(i_YEAR);
    r_CostTotalDummy(i_YEAR) = v_CostTotalDummy.l(i_YEAR);

    r_SupplyZoneDemand(i_YEAR, ZONE_DEMAND) = v_SupplyZoneDemand.l(i_YEAR, ZONE_DEMAND);
    r_TransportEU(i_YEAR, ZONE_IMPORT, ZONE_DEMAND, TRANSPORT_EU) = v_TransportEU.l(i_YEAR, ZONE_IMPORT, ZONE_DEMAND, TRANSPORT_EU);
    r_SupplyZoneImport(i_YEAR, ZONE_IMPORT) = v_SupplyZoneImport.l(i_YEAR, ZONE_IMPORT);
    r_TransportInternational(i_YEAR, ZONE_EXPORT, ZONE_IMPORT, TRANSPORT_INTERNATIONAL) = v_TransportInternational.l(i_YEAR, ZONE_EXPORT, ZONE_IMPORT, TRANSPORT_INTERNATIONAL);
    r_SupplyZoneExport(i_YEAR, ZONE_EXPORT) = v_SupplyZoneExport.l(i_YEAR, ZONE_EXPORT);
    r_SupplyNodeExport(i_YEAR, NODE_EXPORT) = v_SupplyNodeExport.l(i_YEAR, NODE_EXPORT);
    r_TransportNational(i_YEAR, NODE_PRODUCTION, NODE_EXPORT, TRANSPORT_NATIONAL) = v_TransportNational.l(i_YEAR, NODE_PRODUCTION, NODE_EXPORT, TRANSPORT_NATIONAL);
    r_SupplyNodeProduction(i_YEAR, NODE_PRODUCTION) = v_SupplyNodeProduction.l(i_YEAR, NODE_PRODUCTION);

    r_ConversionNodeProduction(i_YEAR,NODE_PRODUCTION,TRANSPORT) = v_ConversionNodeProduction.l(i_YEAR,NODE_PRODUCTION,TRANSPORT);
    r_ReconversionNodeProduction(i_YEAR,NODE_PRODUCTION,TRANSPORT) = v_ReconversionNodeProduction.l(i_YEAR,NODE_PRODUCTION,TRANSPORT);
    r_ConversionZoneExport(i_YEAR,ZONE_EXPORT,TRANSPORT) = v_ConversionZoneExport.l(i_YEAR,ZONE_EXPORT,TRANSPORT);
    r_ReconversionZoneExport(i_YEAR,ZONE_EXPORT,TRANSPORT) = v_ReconversionZoneExport.l(i_YEAR,ZONE_EXPORT,TRANSPORT);
    r_ConversionZoneImport(i_YEAR,ZONE_IMPORT,TRANSPORT) = v_ConversionZoneImport.l(i_YEAR,ZONE_IMPORT,TRANSPORT);
    r_ReconversionZoneImport(YEAR,ZONE_IMPORT,TRANSPORT) = v_ReconversionZoneImport.l(YEAR,ZONE_IMPORT,TRANSPORT);
    r_ConversionZoneDemand(i_YEAR,ZONE_DEMAND,TRANSPORT) = v_ConversionZoneDemand.l(i_YEAR,ZONE_DEMAND,TRANSPORT);
    r_ReconversionZoneDemand(i_YEAR,ZONE_DEMAND,TRANSPORT) = v_ReconversionZoneDemand.l(i_YEAR,ZONE_DEMAND,TRANSPORT);

    r_ProductionDummyDemandZone(i_YEAR, ZONE_DEMAND) = v_ProductionDummyDemandZone.l(i_YEAR, ZONE_DEMAND);
    r_ProductionH2System(i_YEAR, H2_SYSTEM) = v_ProductionH2System.l(i_YEAR, H2_SYSTEM);
)


$INCLUDE H2forEU_SupplyChain_output.gms

