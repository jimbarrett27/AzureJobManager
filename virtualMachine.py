import subprocess as sp

class VirtualMachineException(Exception):
    
    pass


class VirtualMachine(object):
    """Class to handle all of the details of an azure virtual machine, creating the VM, submitting commands to it, 
    monitoring it
    
    """

    @property
    def privateIpAddress(self):
        """The private IP address of the associated VM
        
        """
        return self._privateIpAddress
        
    @property
    def publicIpAddress(self):
        """The public IP address of the cluster
        
        """
        return self._publicIpAddress
      
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
        
    @property
    def headNode(self):
        """The head node for this cluster
        
        """
        
        return self._headNode

    def __init__(self, name, resourceGroup, vmOptions, sshKeyPath = '~/.ssh/id_rsa.pub', verbose = False, publicIp = None):
    
        self._name = name
        self._resourceGroup = resourceGroup
        self._verbose = verbose
        
        self._publicSSHKeyPath = sshKeyPath
        
        self._vmOptions = vmOptions
       
        self._publicIpAddress = publicIp
        
    def launch(self,headNodeIp = None):
        """Launches the VM and parses the returned info
        
        """
        
        try:
            command = 'az vm create '
            for key in self.vmOptions.keys():
                command += key + ' ' + self._vmOptions[key] + ' '
                
            vmDetails = sp.check_output(command,shell=True)
            vmDetails = vmDetails.split('\n')
            
        except sp.CalledProcessError:
            
            raise VirtualMachineException('There was an error generating the virtual machine with name ' + self.name)

        
        for line in vmDetails:
            if 'privateIpAddress' in line:
                s = line.split('"')
                self._privateIpAddress = s[3]
        
        if headNodeIp == None:
            for line in vmDetails:
                if 'publicIpAddress' in line:
                    s = line.split('"')
                    self._publicIpAddress = s[3]
        else:
            self._publicIpAddress = headNodeIp
                
        self.verbosePrint('found private IP address: ' + self._privateIpAddress)
        self.verbosePrint('found public IP address: ' + self._publicIpAddress)
        
    def uploadFile(self,filePath, remoteDestination='.'):
    
        command = 'scp -o StrictHostKeyChecking=no -o ProxyCommand="ssh -W %h:%p -o StrictHostKeyChecking=no ' + \
                    self._vmOptions['--admin-username'] + '@' + self._publicIpAddress + '" ' + filePath + ' ' + \
                    self._vmOptions['--admin-username'] + '@' + self._privateIpAddress + ':' + remoteDestination
                 
        self.verbosePrint("uploading file with command:\n" + command)
        
        sp.call(command,shell=True)
        
    def getFile(self,remotePath, localDestination = '.'):
    
        command = 'scp -o StrictHostKeyChecking=no -o ProxyCommand="ssh -W %h:%p -o StrictHostKeyChecking=no ' + \
                    self._vmOptions['--admin-username'] + '@' + self._publicIpAddress + '" ' + \
                    self._vmOptions['--admin-username'] + '@' + self._privateIpAddress + ':' + remotePath + ' ' + \
                    localDestination
                   
        self.verbosePrint("downloading file with command:\n" + command)
        
        sp.call(command, shell=True)
        
    def sendCommand(self,command,waitToComplete=True):
    
        
        fullCommand = 'ssh ' + self._vmOptions['--admin-username'] + '@' + self._privateIpAddress + ' -o StrictHostKeyChecking=no -o ProxyCommand="ssh -W %h:%p -o StrictHostKeyChecking=no '\
                    + self._vmOptions['--admin-username'] + '@' + self._publicIpAddress + '" '\
                    + '\'' + command + '\''
                    
                    
        self.verbosePrint('sending a command with the command:\n' + fullCommand)

        output = sp.check_output(fullCommand,shell=True)
        
        if not waitToComplete:
            sp.Popen(command,shell=True,stdin=None,stdout=None,stderr=None,close_fds=True)
        
        self.verbosePrint('recieved the output:\n' + output)
        
        return output
       
        
    def clean(self):
    
        command = 'rm -r ~/*'
        
        self.sendCommand(command)
            
    def verbosePrint(self,message):
        """Only print the message if we have the verbose flag on
        
        """
         
        if self._verbose:
            print message
            
    def delete(self):
    
        command = 'az vm delete --force --name ' + self._name + ' --resource-group ' + self._resourceGroup
        
        sp.call(command,shell=True)
        
        
        

        
    
            
    
        
