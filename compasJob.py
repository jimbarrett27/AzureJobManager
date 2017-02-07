import numpy as np
from azureJob import AzureJob

class CompasJob(AzureJob):

    @property
    def id(self):
        """A unique identifier for the job, used when creating unique names etc
        
        """
        
        return self._id

    @property
    def compasCommand(self):
        """The string of the command line call to COMPAS for this particular job
        
        """
        
        return self._compasCommand
        
    @property    
    def outputPath(self):
        """The path the where the output from this path should be stored
        
        """
        
        return self._outputPath
    
    @property   
    def compasPath(self):
        """The path to the statically linked COMPAS executable
        
        """
        
        return self._compasPath

    def initialise(self, ID, compasCommand, outputPath, compasPath):
    
        # add an extra command to make a text file when COMPAS finishes
        self._id = ID
        self._compasCommand = compasCommand  
        self._outputPath = outputPath
        self._compasPath = compasPath
        
    def activate(self, virtualMachine):
    
        self._vm = virtualMachine
        
        self._vm.uploadFile(self._compasPath)
        
        bashFileName = 'bashFile' + str(self._id) + '.bash'
        f = open(bashFileName,'w')
        f.write(self._compasCommand)
        f.write(" &>/dev/null\n")
        f.write("echo completed >> completed.txt\n")
        f.close()
        
        self._vm.uploadFile(bashFileName)
        self._vm.sendCommand("chmod 744 " + bashFileName)
        
        pythonFileName = 'pythonFile' + str(self._id) + '.py'
        f = open(pythonFileName,'w')
        f.write("import subprocess\n")
        f.write("subprocess.Popen([\"bash\",\"" + bashFileName + "\"],")
        f.write("stdin=None, stdout=None, stderr=None, close_fds=True)\n")
        f.close() 
        
        self._vm.uploadFile(pythonFileName)

        self._vm.sendCommand('python ' + pythonFileName,waitToComplete=False)
        
    def checkCompleted(self):
        """check if the 'completed.txt exists and contains the word completed
        
        """
        
        try:
            self._vm.getFile('~/completed.txt',self._outputPath)
            
            f = open(self._outputPath +'/completed.txt')
            f.close()
            
            return True
                
        except IOError:
        
            return False
            
        
        return False
        
    def postProcess(self):
    
       self._vm.getFile('~/initialParameters.txt', self._outputPath)
       self._vm.getFile('~/mergingParameters.txt', self._outputPath)
       self._vm.getFile('~/formationHistory.txt', self._outputPath)
       
    def getStatusMessage(self):
    
        op = self._vm.getOutputFromCommand('wc -l initialParameters.txt')
        
        nBinsSimulated = str(op.split(' ')[0])
        
        return 'simulated ' + nBinsSimulated + ' binaries'
         
        
        
    
        
