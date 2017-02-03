import subprocess as sp
import numpy as np
from virtualMachine import VirtualMachine
import warnings
import time


class AzureJobManager(object):

    @property
    def idleJobs(self):
        """The array of jobs to be run
        
        """
        
        return self._idleJobs
        
    @property
    def activeJobs(self):
        """The array of jobs currently running
        
        """
        
        return self._activeJobs
        
    @property
    def completedJobs(self):
        """The array of jobs that have completed
        
        """
        
        return self._completedJobs
        
    @property
    def verbose(self):
        """Whether or not we're printing a load of stuff about the job. Useful for debugging
        
        """
        
        return self._verbose
        
    @property
    def virtualMachines(self):
        """The array of virtual machines
        
        """
        
        return self._virtualMachines
        
    @property  
    def publicSSHKeyPath(self):
        """The public SSH key to be given to the VM as a trusted user
        
        """
        
        return self._publicSSHKeyPath
        
    @property
    def nJobs(self):
        """The number of jobs initially submitted to the manager
        
        """
        
        return self._nJobs
        
    @property
    def sleepTime(self):
        """The amount of time to sleep between checking job statuses
        
        """
        
        return self._sleepTime
        
        

    def __init__(self, resourceGroupName, nVirtualMachines, jobs, sshKeyPath = '~/.ssh/id_rsa.pub', verbose = False, \
                sleepTime = 300):
    
        
        self._resourceGroupName = resourceGroupName
        self._publicSSHKeyPath = sshKeyPath
        self._verbose = verbose
        self._sleepTime = sleepTime
        
        self._virtualMachines = []
        self._idleJobs = jobs
        self._activeJobs = []
        self._completedJobs = []
        
        self._nJobs = len(jobs)
        
        if self._nJobs < nVirtualMachines:
            warnings.warn("requested more VMs than jobs, reducing the number of VMs")
            nVirtualMachines = self._nJobs
            
        
        self.makeResourceGroup()
        
        self.constructVirtualMachines(nVirtualMachines)
        
    
    def makeResourceGroup(self):
        """Make the azure resource group
        
        """
        
        command = 'az group create --name ' + self._resourceGroupName + ' -l centralus'
        
        self.verbosePrint('Now creating a resource group with command ' + command)
        
        sp.call(command,shell=True)
        
    def constructVirtualMachines(self, nVirtualMachines):
        """Construct the VirtualMachine objects with the necessary information
        
        """
    
        for i in range(nVirtualMachines):
        
            vmName = self._resourceGroupName + 'vm' + str(i)
            
            vm = VirtualMachine(vmName, self._resourceGroupName, sshKeyPath = self._publicSSHKeyPath, \
                                verbose = self._verbose)
                                
            self._virtualMachines.append(vm)
            
    def run(self):
        """Launches all of the virtual machines, then monitors the progress of the jobs, until they're all done,
        finally destroying the VMs and the resource group once everything's done
        
        """
        
        assert self._nJobs == len(self._idleJobs)
        assert self._nJobs >= len(self._virtualMachines)
        
        #initally launch the virtual machines, putting one job on each of them
        for vm in self._virtualMachines:
            
            vm.launch()
            self._activeJobs.append(self._idleJobs[0])
            self._idleJobs[0].activate(vm)
            self._idleJobs = self._idleJobs[1:]
            
        #wait before starting the checking loop
        time.sleep(self._sleepTime)
        
        while self.completed() == False:
        
            self.updateJobs()
            
            time.sleep(self._sleepTime)
            
            
        self.cleanUp()
                
    
    def updateJobs(self):
        """Checks all of the active jobs for completion, and moves them to the completed queue,
        before replacing them with one from the idle queue
        
        """
        
        remainingActiveJobs = []
        availableVms = []

        for jobToCheck in self._activeJobs:

            if jobToCheck.checkCompleted() == True:
            
                jobToCheck.postProcess()
                availableVms.append(jobToCheck._vm)
                self._completedJobs.append(jobToCheck)
                
            else:
            
                remainingActiveJobs.append(jobToCheck)
                
        self._activeJobs = remainingActiveJobs

        for vm in availableVms:
        
            vm.clean()

            if len(self._idleJobs) == 0:
                
                break
             
            else:

                self._activeJobs.append(self._idleJobs[0])
                self._idleJobs[0].activate(vm)
                self._idleJobs = self._idleJobs[1:]
            
    def cleanUp(self):
        """Cleans up everything: currently simply deletes the resource group
        
        """
        
        command = 'az group delete --force --name ' + self._resourceGroupName
        
        sp.call(command,shell=True)
        

    def completed(self):
        """returns True if all of the jobs are completed
        
        """
        
        assert len(self._idleJobs) + len(self._activeJobs) + len(self._completedJobs) == self._nJobs
        
        return len(self._completedJobs) == self._nJobs
     
        
    def verbosePrint(self,message):
        """Only print the message if we have the verbose flag on
        
        """
         
        if self._verbose:
            print message
