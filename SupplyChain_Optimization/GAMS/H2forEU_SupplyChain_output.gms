Parameter
r_CostTotal(YEAR)
r_CostTransport(YEAR)
r_CostTransportNational(YEAR)
r_CostTransportInternational(YEAR)
r_CostTransportConversion(YEAR)

r_CostProduction(YEAR)
r_CostTotalDummy(YEAR)
r_Path(YEAR, PATH)
r_ProductionNode(YEAR, NODE_PRODUCTION)
r_ProductionH2System(YEAR, H2_SYSTEM)
r_ProductionDummy(YEAR, NODE_IMPORT)
;


r_CostTotal(YEAR) = v_CostTotal.l(YEAR);
r_CostTransport(YEAR) = v_CostTransport.l(YEAR);
r_CostTransportNational(YEAR) = v_CostTransportNational.l(YEAR);
r_CostTransportInternational(YEAR) = v_CostTransportInternational.l(YEAR);
r_CostTransportConversion(YEAR)= v_CostTransportConversion.l(YEAR);
r_CostProduction(YEAR) = v_CostProduction.l(YEAR);
r_CostTotalDummy(YEAR) = v_CostTotalDummy.l(YEAR);
r_Path(YEAR, PATH) = v_Path.l(YEAR, PATH);
r_ProductionNode(YEAR, NODE_PRODUCTION) = v_ProductionNode.l(YEAR, NODE_PRODUCTION);
r_ProductionH2System(YEAR, H2_SYSTEM) = v_ProductionH2System.l(YEAR, H2_SYSTEM);
r_ProductionDummy(YEAR, NODE_IMPORT) = v_ProductionDummy.l(YEAR, NODE_IMPORT);



execute_unload 'gdx/00_results.gdx'
r_CostTotal,
r_CostTransport,
r_CostTransportNational,
r_CostTransportInternational,
r_CostTransportConversion,
r_CostProduction,
r_CostTotalDummy,
r_Path,
r_ProductionNode,
r_ProductionH2System,
r_ProductionDummy
;