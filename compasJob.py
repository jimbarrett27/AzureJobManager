import numpy as np
from azureJob import AzureJob

class CompasJob(AzureJob):

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

    def initialise(self, compasCommand, outputPath, compasPath):
    
        # add an extra command to make a text file when COMPAS finishes
        self._compasCommand = compasCommand + '; echo completed >> completed.txt;' 
        self._outputPath = outputPath
        self._compasPath = compasPath
        
    def activate(self, virtualMachine):
    
        self._vm = virtualMachine
        
        self._vm.uploadFile(self._compasPath)
        
        #a short python script which gets run directly by bash
        command = " python -c '"
        command += "import subprocess;"
        command += "subprocess.Popen([" + self._compasCommand + "],"
        command += "stdin=None, stdout=None, stderr=None, close_fds=True)"
        command += "'"
        
        print command
        
        self._vm.sendCommand(command)
        
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
       
       
        
    
         
        
        
    
        
