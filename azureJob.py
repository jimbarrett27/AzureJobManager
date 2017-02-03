import numpy as np

class AzureJob(object):

    @property
    def vm(self):
        """The virtual machine associated with this job
        
        """
        
        return self._vm
     

    def __init__(self):
    
        self._vm = None
        
    def initialise(self):
        
        raise NotImplementedError("This is the base class, you should have implemented the initialise() method")
        
    def activate(self, virtualMachine):
    
        raise NotImplementedError("This is the base class, you should have implemented the activate() method")
        
    def checkCompleted(self):
    
        raise NotImplementedError("This is the base class, you should have implemented the checkCompleted() method")
        
    def postProcess(self):
    
        raise NotImplementedError("This is the base class, you should have implemented the postProcess() method")
        
    
    
