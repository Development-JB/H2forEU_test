**********************************
*** MODEL SETTINGS
**********************************

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


**********************************
*** LOAD FILES and MODEL
**********************************
$INCLUDE H2forEU_LCOH_setup.gms
$INCLUDE H2forEU_LCOH_data.gms

$INCLUDE H2forEU_LCOH_model.gms

solve H2forEU_LCOH using nlp minimizing v_LCOH;

p_capacity(ENERGY_TYPE) = v_Capacity.l(ENERGY_TYPE);
p_LCOH = v_LCOH.l;
*display v_Capacity.l, v_GenerationEle.l, v_TotalCost.l

$INCLUDE H2forEU_LCOH_output.gms
