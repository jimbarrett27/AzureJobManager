import subprocess as sp
import numpy as np
from virtualMachine import VirtualMachine
import warnings
import time
import jinja2 as jj2

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
    def privateSSHKeyPath(self):
        """The private SSH key to be given to the VM
        
        """
        
        return self._privateSSHKeyPath
        
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
    
    @property    
    def htmlPath(self):
        """The path to the generated HTML page displaying progress
        
        """
        
        return self._htmlPath
        

    def __init__(self, resourceGroupName, nVirtualMachines, jobs, publicSshKeyPath = '~/.ssh/id_rsa.pub', privateSshKeyPath = '~/.ssh/id_rsa', verbose = False, \
                sleepTime = 300, htmlPath = None):
    
        
        self._resourceGroupName = resourceGroupName
        self._publicSSHKeyPath = publicSshKeyPath
        self._privateSSHKeyPath = privateSshKeyPath
        self._verbose = verbose
        self._sleepTime = sleepTime
        self._htmlPath = htmlPath
        
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
            
            vmOptions = {
        
                '--image' : 'UbuntuLTS',
                '--admin-username' : 'ops',
                '--ssh-key-value' : self._publicSSHKeyPath,
                '--resource-group' : self._resourceGroupName,
                '--location' : 'centralus',
                '--name' : vmName,
                '--size' : 'Basic_A0',
                '--storage-sku' : 'Standard_LRS',
                '--public-ip-address' : self._resourceGroupName + 'PublicIp',
                '--vnet-name' : self._resourceGroupName + 'VNet',
                '--nsg' : self._resourceGroupName + 'NSG',
                '--subnet' : self._resourceGroupName + 'Subnet'
            }
            
            if i>0:
                vmOptions['--public-ip-address'] = "\"\""  
#                vmOptions['--nsg'] = ""  
            
            vm = VirtualMachine(vmName, self._resourceGroupName, vmOptions, sshKeyPath = self._publicSSHKeyPath, \
                                verbose = self._verbose)
                                
            self._virtualMachines.append(vm)
            
    def run(self):
        """Launches all of the virtual machines, then monitors the progress of the jobs, until they're all done,
        finally destroying the VMs and the resource group once everything's done
        
        """
        
        assert self._nJobs == len(self._idleJobs)
        assert self._nJobs >= len(self._virtualMachines)
        
        headNodeIp = None
        
        #initally launch the virtual machines, putting one job on each of them
        for i,vm in enumerate(self._virtualMachines):
            
            try:
                vm.launch(headNodeIp)
                if i == 0:
                    command = 'scp -o  StrictHostKeyChecking=no ' + self._publicSSHKeyPath + ' ops@' + vm._publicIpAddress + ':.ssh/.'
                    sp.call(command,shell=True)
                    command = 'scp -o  StrictHostKeyChecking=no ' + self._privateSSHKeyPath + ' ops@' + vm._publicIpAddress + ':.ssh/.'
                    sp.call(command,shell=True)
                    
                    headNodeIp = vm._publicIpAddress
                    
            except:
                print "there was an error launching one of the VMs. we may have hit a usage limit..."
                print "making do with the ones already launched"
                self._virtualMachines = self._virtualMachines[:i]
                break
            if not self._htmlPath == None:
                try:
                    self.updateHtml()
                except:
                    print "there was an error writing the HTML page"
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

        if not self._htmlPath == None:
            try:
                self.updateHtml()
            except:
                print "there was an error writing the HTML page"
        
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

        if len(availableVms) > len(self._idleJobs):
            while len(availableVms) > len(self._idleJobs):
                availableVms[0].delete()
                availableVms = availableVms[1:]

        for vm in availableVms:
        
            vm.clean()
            
        for vm in availableVms:

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
            
    def updateHtml(self):
    
        runStatus = []
        
        for aJob in self._activeJobs:
        
            jobId = str(aJob._id)
            try:
                jobStatus = aJob.getStatusMessage()
            except:
                jobStatus = 'Error getting job status'
            jobVm = aJob._vm._privateIpAddress
            jobOutputPath = aJob._outputPath
            
            runStatus.append((jobId,jobStatus,jobVm,jobOutputPath))
    
        for iJob in self._idleJobs:
        
            jobId = str(iJob._id)
            jobStatus = "Job Inactive"
            jobVm = 'None'
            jobOutputPath = iJob._outputPath
            
            runStatus.append((jobId,jobStatus,jobVm,jobOutputPath))

        for cJob in self._completedJobs:
            
            jobId =  str(cJob._id)
            jobStatus = "job completed"
            jobVm = 'None'
            jobOutputPath = cJob._outputPath
            
            runStatus.append((jobId,jobStatus,jobVm,jobOutputPath))
            
        
        env = jj2.Environment(loader=jj2.FileSystemLoader('.'))
        template = env.get_template('progressMonitorTemplate.html')
        
        templateVars = {
            "title" : "jobs running under resource group " + self._resourceGroupName,
            "pagetitle" : "jobs running under resource group " + self._resourceGroupName,
            "runStatus" : runStatus
        }
        
        html = template.render(templateVars)
        htmlFile = open(self._htmlPath + '/AzureStatus-'+self._resourceGroupName+'.html', 'w')
        htmlFile.write(html)
        htmlFile.close()
