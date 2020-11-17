# Settings file

# Import packages
import pandas as pd
import numpy as np

# Import files
import H2forEU_settings


df_time_link = pd.DataFrame([])
df_time_link['Timestamp'] = pd.date_range(start='01/01/'+str(H2forEU_settings.val_reference_year)+' 00:00', end='31/12/'+str(H2forEU_settings.val_reference_year)+' 23:00', freq = 'H')
df_time_link['Year'] = df_time_link['Timestamp'].dt.year
df_time_link['Timestep_hour'] = list(range(1,len(df_time_link)+1,1))
df_time_link['Timestep_month'] = df_time_link['Timestamp'].dt.month
df_time_link['Timestep_week'] = (df_time_link['Timestep_hour']/168).apply(np.ceil).astype(int)
df_time_link['Timestep_day'] = (df_time_link['Timestep_hour']/24).apply(np.ceil).astype(int)
df_time_link['Weekday'] = df_time_link['Timestamp'].dt.weekday

df_time_link['Timestep_hour'] = df_time_link['Timestep_hour'].astype(str).str.zfill(4)
df_time_link['Timestep_month'] = df_time_link['Timestep_month'].astype(str).str.zfill(2)
df_time_link['Timestep_week'] = df_time_link['Timestep_week'].astype(str).str.zfill(2)
df_time_link['Timestep_day'] = df_time_link['Timestep_day'].astype(str).str.zfill(3)

df_time_link = df_time_link[['Timestamp','Year','Timestep_month','Timestep_week','Timestep_day','Timestep_hour','Weekday']]

lst_month = df_time_link['Timestep_month'].unique().tolist()
lst_week = df_time_link['Timestep_week'].unique().tolist()
lst_day = df_time_link['Timestep_day'].unique().tolist()
lst_hours = df_time_link['Timestep_hour'].unique().tolist()
