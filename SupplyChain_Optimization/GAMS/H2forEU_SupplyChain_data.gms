*$INCLUDE H2forEU_SupplyChain_setup.gms



Parameter p_production_limit_country(YEAR, COUNTRY, ENERGY_TYPE);
$gdxin gdx/p_production_limit_country.gdx
$load p_production_limit_country = p_production_limit_country
*$gdxin


Parameter p_production_limit_volume_node(YEAR, NODE_PRODUCTION, ENERGY_TYPE);
$gdxin gdx/p_production_limit_volume_node.gdx
$load p_production_limit_volume_node = p_production_limit_volume_node
$gdxin
*display p_production_limit_volume_node


Parameter p_production_limit_capacity_node(YEAR, NODE_PRODUCTION);
$gdxin gdx/p_production_limit_capacity_node.gdx
$load p_production_limit_capacity_node = p_production_limit_capacity_node
$gdxin
*display p_production_limit_capacity_node


Parameter p_production_area_available_node(NODE_PRODUCTION);
$gdxin gdx/p_production_area_available_node.gdx
$load p_production_area_available_node = p_production_area_available_node
$gdxin
*display p_production_area_available_node


Parameter p_production_energy_density(ENERGY_TYPE);
$gdxin gdx/p_production_energy_density.gdx
$load p_production_energy_density = p_production_energy_density
$gdxin
*display p_production_energy_density


Parameter p_production_land_dedication(ENERGY_TYPE);
$gdxin gdx/p_production_land_dedication.gdx
$load p_production_land_dedication = p_production_land_dedication
$gdxin
*display p_production_land_dedication



Parameter p_demand_eu(YEAR);
$gdxin gdx/p_demand_eu.gdx
$load p_demand_eu = p_demand_eu
$gdxin


Parameter p_production_volume(YEAR, H2_SYSTEM);
$gdxin gdx/p_production_volume.gdx
$load p_production_volume = p_production_volume
$gdxin


Parameter p_production_capacities(YEAR, H2_SYSTEM, ENERGY_TYPE);
$gdxin gdx/p_production_capacities.gdx
$load p_production_capacities = p_production_capacities
$gdxin
display p_production_capacities


Parameter p_production_cost(YEAR, H2_SYSTEM);
$gdxin gdx/p_production_cost.gdx
$load p_production_cost = p_production_cost
$gdxin


Parameter p_transport_national_cost_fixed(YEAR, TRANSPORT_NATIONAL);
$gdxin gdx/p_transport_national_cost_fixed.gdx
$load p_transport_national_cost_fixed = p_transport_national_cost_fixed
$gdxin


Parameter p_transport_national_cost_variable(YEAR, TRANSPORT_NATIONAL);
$gdxin gdx/p_transport_national_cost_variable.gdx
$load p_transport_national_cost_variable = p_transport_national_cost_variable
$gdxin


Parameter p_transport_national_distance(NODE_PRODUCTION, NODE_EXPORT,TRANSPORT_NATIONAL);
$gdxin gdx/p_transport_national_distance.gdx
$load p_transport_national_distance = p_transport_national_distance
$gdxin


Parameter p_transport_international_cost_fixed(YEAR, TRANSPORT_INTERNATIONAL);
$gdxin gdx/p_transport_international_cost_fixed.gdx
$load p_transport_international_cost_fixed = p_transport_international_cost_fixed
$gdxin


Parameter p_transport_international_cost_variable(YEAR, TRANSPORT_INTERNATIONAL);
$gdxin gdx/p_transport_international_cost_variable.gdx
$load p_transport_international_cost_variable = p_transport_international_cost_variable
$gdxin


Parameter p_transport_international_capacity(YEAR, NODE_EXPORT, NODE_IMPORT, TRANSPORT_INTERNATIONAL);
$gdxin gdx/p_transport_international_capacity.gdx
$load p_transport_international_capacity = p_transport_international_capacity
$gdxin


Parameter p_transport_international_import_capacity(YEAR, NODE_IMPORT, TRANSPORT_INTERNATIONAL);
$gdxin gdx/p_transport_international_import_capacity.gdx
$load p_transport_international_import_capacity = p_transport_international_import_capacity
$gdxin


Parameter p_transport_international_distance(NODE_EXPORT, NODE_IMPORT, TRANSPORT_INTERNATIONAL);
$gdxin gdx/p_transport_international_distance.gdx
$load p_transport_international_distance = p_transport_international_distance
$gdxin


Parameter p_transport_conversion_cost(YEAR, TRANSPORT_CONVERSION);
$gdxin gdx/p_transport_conversion_cost.gdx
$load p_transport_conversion_cost = p_transport_conversion_cost
$gdxin

