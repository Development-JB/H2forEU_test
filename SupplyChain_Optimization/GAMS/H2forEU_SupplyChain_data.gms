*$INCLUDE H2forEU_SupplyChain_setup.gms



Parameter p_production_limit_country(YEAR, COUNTRY, ENERGY_TYPE);
$gdxin gdx/p_production_limit_country.gdx
$load p_production_limit_country = p_production_limit_country
*$gdxin

$ontext
Parameter p_production_limit_volume_node(YEAR, NODE_PRODUCTION, ENERGY_TYPE);
$gdxin gdx/p_production_limit_volume_node.gdx
$load p_production_limit_volume_node = p_production_limit_volume_node
$gdxin
*display p_production_limit_volume_node
$offtext

Parameter p_production_limit_feedstock_node(YEAR, NODE_PRODUCTION, ENERGY_TYPE);
$gdxin gdx/p_production_limit_feedstock_node.gdx
$load p_production_limit_feedstock_node = p_production_limit_feedstock_node
$gdxin
*display p_production_limit_feedstock_node


Parameter p_production_feedstock(YEAR, H2_SYSTEM);
$gdxin gdx/p_production_feedstock.gdx
$load p_production_feedstock = p_production_feedstock
$gdxin
*display p_production_feedstock


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



Parameter p_demand_zone(YEAR, ZONE_DEMAND);
$gdxin gdx/p_demand_zone.gdx
$load p_demand_zone = p_demand_zone
$gdxin
display p_demand_zone


Parameter p_production_volume(YEAR, H2_SYSTEM);
$gdxin gdx/p_production_volume.gdx
$load p_production_volume = p_production_volume
$gdxin


Parameter p_production_capacity(YEAR, H2_SYSTEM, ENERGY_TYPE);
$gdxin gdx/p_production_capacity.gdx
$load p_production_capacity = p_production_capacity
$gdxin
display p_production_capacity


Parameter p_production_cost(YEAR, H2_SYSTEM);
$gdxin gdx/p_production_cost.gdx
$load p_production_cost = p_production_cost
$gdxin


Parameter p_transport_national_cost_fixed(YEAR, TRANSPORT);
$gdxin gdx/p_transport_national_cost_fixed.gdx
$load p_transport_national_cost_fixed = p_transport_national_cost_fixed
$gdxin


Parameter p_transport_national_cost_variable(YEAR, TRANSPORT);
$gdxin gdx/p_transport_national_cost_variable.gdx
$load p_transport_national_cost_variable = p_transport_national_cost_variable
$gdxin


Parameter p_transport_national_distance(NODE_PRODUCTION, NODE_EXPORT,TRANSPORT);
$gdxin gdx/p_transport_national_distance.gdx
$load p_transport_national_distance = p_transport_national_distance
$gdxin


Parameter p_transport_international_cost_fixed(YEAR, TRANSPORT);
$gdxin gdx/p_transport_international_cost_fixed.gdx
$load p_transport_international_cost_fixed = p_transport_international_cost_fixed
$gdxin


Parameter p_transport_international_cost_variable(YEAR, TRANSPORT);
$gdxin gdx/p_transport_international_cost_variable.gdx
$load p_transport_international_cost_variable = p_transport_international_cost_variable
$gdxin


Parameter p_transport_international_import_capacity(YEAR, ZONE_IMPORT, TRANSPORT);
$gdxin gdx/p_transport_international_import_capacity.gdx
$load p_transport_international_import_capacity = p_transport_international_import_capacity
$gdxin


Parameter p_transport_international_distance(ZONE_EXPORT, ZONE_IMPORT, TRANSPORT);
$gdxin gdx/p_transport_international_distance.gdx
$load p_transport_international_distance = p_transport_international_distance
$gdxin


Parameter p_transport_eu_cost_fixed(YEAR, TRANSPORT);
$gdxin gdx/p_transport_eu_cost_fixed.gdx
$load p_transport_eu_cost_fixed = p_transport_eu_cost_fixed
$gdxin


Parameter p_transport_eu_cost_variable(YEAR, TRANSPORT);
$gdxin gdx/p_transport_eu_cost_variable.gdx
$load p_transport_eu_cost_variable = p_transport_eu_cost_variable
$gdxin


Parameter p_transport_eu_distance(ZONE_IMPORT, ZONE_DEMAND, TRANSPORT);
$gdxin gdx/p_transport_eu_distance.gdx
$load p_transport_eu_distance = p_transport_eu_distance
$gdxin


Parameter p_transport_conversion_cost(YEAR, TRANSPORT);
$gdxin gdx/p_transport_conversion_cost.gdx
$load p_transport_conversion_cost = p_transport_conversion_cost
$gdxin


Parameter p_transport_reconversion_cost(YEAR, TRANSPORT);
$gdxin gdx/p_transport_reconversion_cost.gdx
$load p_transport_reconversion_cost = p_transport_reconversion_cost
$gdxin

