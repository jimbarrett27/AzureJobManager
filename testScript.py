from CompasAzure import prepareCommands
from azureJobManager import AzureJobManager
from compasJob import CompasJob
import os

commands = prepareCommands()

jobs = []
for i,command in enumerate(commands):

    dirname = './output'+str(i)
    
    os.makedirs(dirname)

    j = CompasJob()
    j.initialise(i,command,dirname,'/home/jbarrett/AzureJobManager/COMPAS')
    jobs.append(j)

ajm = AzureJobManager('qwerty1234567',3,jobs,verbose=True,sleepTime=10,htmlPath = '/home/jbarrett/public_html')

ajm.run()

ajm.cleanUp()
