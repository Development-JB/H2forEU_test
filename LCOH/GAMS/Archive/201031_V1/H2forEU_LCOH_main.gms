**********************************
*** MODEL SETTINGS
**********************************




**********************************
*** LOAD FILES and MODEL
**********************************
$INCLUDE H2forEU_LCOH_setup.gms
$INCLUDE H2forEU_LCOH_data.gms
$INCLUDE H2forEU_LCOH_model.gms


solve H2forEU_LCOH using nlp minimizing v_LCOH;

display v_CapacityRes.l, v_GenerationEle.l, v_TotalCost.l

$INCLUDE H2forEU_LCOH_output.gms