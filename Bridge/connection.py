from Extern import b0RemoteApi as vrep
from Bridge import configuration as cf
import time
import numpy as np

class clientsever:
    def __init__(self, control_mode= 'position', client_name='b0RemoteApi_pythonClient', server_name = 'b0RemoteApiAddOn'):
        self.mode =control_mode
        self.client = vrep.RemoteApiClient(client_name, server_name)
        self.doNextStep = True
        self.q = np.array(np.zeros(cf.dof))
        self.qdot = np.array(np.zeros(cf.dof))
        
    def getMotorHandle(self):
        self.motorHandle = []
        for i in range(0, cf.dof):
            _, motor = self.client.simxGetObjectHandle('redundantRob_joint'+str(i+1), self.client.simxServiceCall())
            self.motorHandle.append(motor)
 
    def getMotorState(self):
        def jointCallback(msg):
            a = 1.0
            True
        
        for i in range(0, cf.dof):
            self.client.simxGetJointPosition(self.motorHandle[i], self.client.simxDefaultSubscriber(jointCallback))
        
        return self.q, self.qdot

    def setMotorState(self, qdes):
        if self.mode == 'position':
            for i in range(0, cf.dof):
                self.client.simxSetJointTargetPosition(self.motorHandle[i], qdes[i], self.client.simxDefaultPublisher())

