import pandas as pd

import H2forEU_config_general

df_init = pd.read_csv(str(H2forEU_config_general.wd_l1)+"//Data//05Input//06TreatedPreparedData//ProductionNonVRES.csv")

df_init = df_init.set_index(['Node_production','Energy_type','Technology'])
df_out = df_init.stack().reset_index(name='Value')
df_out = df_out.rename(columns={'level_3':'Year'})
df_out.to_csv(str(H2forEU_config_general.wd_l1)+"//Data//05Input//06TreatedPreparedData//ProductionNonVRES_converted.csv", index=False)



