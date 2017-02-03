import subprocess as sp

class VirtualMachineException(Exception):
    
    pass


class VirtualMachine(object):
    """Class to handle all of the details of an azure virtual machine, creating the VM, submitting commands to it, 
    monitoring it
    
    """

    @property
    def ipAddress(self):
        """The IP address of the associated VM
        
        """
        return self._ipAddress
      
    @property  
    def publicSSHKeyPath(self):
        """The public SSH key to be given to the VM as a trusted user
        
        """
        
        return self._publicSSHKeyPath
        
    @property
    def vmOptions(self):
        """The options to be used when  making the VM
        
        """
        
        return self._vmOptions
        
    @property
    def name(self):
        """The name of the job, which will also be the name of the VM and 
        everything else which requires a name.
        
        """
        
        return self._name
        
    @property
    def verbose(self):
        """Whether or not we're printing a load of stuff about the job. Useful for debugging
        
        """
        
        return self._verbose
        
    @property
    def resourceGroup(self):
        """The resource group to which the job is associated
        
        """
        
        return self._resourceGroup
            
    
    def getSSHAddress(self):
        """Convenience method to return a string of the form user@ipaddress
        
        """
    
        return self._vmOptions['--admin-username'] + '@' + self._ipAddress

    def __init__(self, name, resourceGroup, sshKeyPath = '~/.ssh/id_rsa.pub', verbose = False):
    
        self._name = name
        self._resourceGroup = resourceGroup
        self._verbose = verbose
        
        self._publicSSHKeyPath = sshKeyPath
        
        self._vmOptions = {
        
            '--image' : 'UbuntuLTS',
            '--admin-username' : 'ops',
            '--ssh-key-value' : self._publicSSHKeyPath,
            '--resource-group' : self._resourceGroup,
            '--location' : 'centralus',
            '--name' : self._name,
            '--size' : 'Basic_A0',
            '--storage-sku' : 'Standard_LRS'
        
        }
    
    def launch(self):
        """Launches the VM and parses the returned info
        
        """
        
        self.verbosePrint('now launching VM with name' + self._name)
        
        try:
            command = 'az vm create '
            for key in self.vmOptions.keys():
                command += key + ' ' + self._vmOptions[key] + ' '
                
            self.verbosePrint('now launching VM with the command;')
            self.verbosePrint(command)
                
            vmDetails = sp.check_output(command,shell=True)
            vmDetails = vmDetails.split('\n')
            
        except sp.CalledProcessError:
            
            raise VirtualMachineException('There was an error generating the virtual machine with name ' + self.name)
        
        self.verbosePrint('VM launched with name' + self.name)
        
        for line in vmDetails:
            if not 'publicIpAddress' in line:
                continue
            else:
                s = line.split('"')
                self._ipAddress = s[3]
                break
                
        self.verbosePrint('found public IP address: ' + self.ipAddress)
        
    def uploadFile(self,filePath, remoteDestination='.'):
    
        command = 'scp ' + filePath + ' ' + self.getSSHAddress() + ':' + remoteDestination
        
        self.verbosePrint('copying file with command ' + command)
        
        sp.call(command,shell=True)
        
    def getFile(self,remotePath, localDestination = '.'):
    
        command = 'scp ' + self.getSSHAddress() + ':' + remotePath + ' ' + localDestination
        
        self.verbosePrint('copying file with command ' + command)
        
        sp.call(command, shell=True)
        
    def sendCommand(self,command):
    
        fullCommand = "ssh " + self.getSSHAddress() + " \"" + command + "\""
        
        self.verbosePrint('sending command via the full command ' + fullCommand)
        
        sp.call(fullCommand,shell=True)
        
        
    def clean(self):
    
        command = 'rm -r ~/*'
        
        self.sendCommand(command)
            
    def verbosePrint(self,message):
        """Only print the message if we have the verbose flag on
        
        """
         
        if self._verbose:
            print message
        
        
        

        
    
            
    
        
