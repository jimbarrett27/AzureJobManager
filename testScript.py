from CompasAzure import prepareCommands
from azureJobManager import AzureJobManager
from compasJob import CompasJob

commands = prepareCommands()

jobs = []
for i,command in enumerate(commands):

    dirname = './output'+str(i)
    
    os.makedirs(dirname)

    j = CompasJob()
    j.initialise(i,command,dirname,'/home/jbarrett/AzureJobManager/COMPAS')
    jobs.append(j)

ajm = AzureJobManager('qwerty1234567',3,jobs,verbose=True,sleepTime=30)

ajm.run()

ajm.cleanUp()
