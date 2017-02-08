import sys
sys.path.remove ('/net/lnx0/export/local/debian/lib/python2.7/dist-packages')
sys.path.remove ('/usr/local/lib/python2.7/dist-packages')


from CompasAzure import prepareCommands
from azureJobManager import AzureJobManager
from compasJob import CompasJob
import os

commands = prepareCommands()

jobs = []
for i,command in enumerate(commands):

    dirname = '/data0/jbarrett/central/output'+str(i)
    
    os.makedirs(dirname)

    j = CompasJob()
    j.initialise(i,command,dirname,'/home/jbarrett/AzureJobManager/COMPAS')
    jobs.append(j)

ajm = AzureJobManager('lbvSigmaAlphaCentral',20,jobs,verbose=True,sleepTime=300,htmlPath = '/home/jbarrett/www_html')

try:
    ajm.run()

