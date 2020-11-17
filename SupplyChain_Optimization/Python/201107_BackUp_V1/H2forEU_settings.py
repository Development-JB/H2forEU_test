# Settings file

# Import packages
from pathlib import Path
import pandas as pd

# Import files
import H2forEU_config_general

val_reference_year = 2016

val_path_settings = Path(str(H2forEU_config_general.wd_l1)+"//Data//01Input//Input_settings.xls")
val_path_data_general = Path(str(H2forEU_config_general.wd_l1)+"//Data//01Input//Input_data_general.xls")
val_path_inputs = str(H2forEU_config_general.wd_l1)+"//Data//01Input//"
# val_path_templates = str(H2forEU_config_general.wd_l3)+"//Data//00Templates//"
val_path_gdx_output = Path(str(H2forEU_config_general.wd_l1)+"//GAMS//gdx//")


df_set = pd.read_excel(val_path_settings, sheet_name='Sets')




