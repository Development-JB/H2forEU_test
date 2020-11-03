from gams import *
from gams import execution as ex
import os
import sys


print(sys.argv)

ws = GamsWorkspace(working_directory = 'C:\\Users\\Johannes\\Desktop\\GAMS_test')

print(ws)


t1 = ws.add_job_from_file("C:\\Users\\Johannes\\Desktop\\GAMS_test\\trnsport.gms")
t1.run()
print("Ran with Default:")

for rec in t1.out_db["x"]:
    print("x(" + rec.key(0) + "," + rec.key(1) + "): level=" + str(rec.level) + " marginal=" + str(rec.marginal))
