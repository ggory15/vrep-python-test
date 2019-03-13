from Bridge import connection 
from Bridge import configuration as cf
import numpy as np
import time

vrep = connection.clientsever()
client = vrep.client

def simulationStepStarted(msg):
    simTime=msg[1][b'simulationTime'];
    
def simulationStepDone(msg):
    simTime=msg[1][b'simulationTime'];
    vrep.doNextStep=True

vrep.getMotorHandle()

client.simxSynchronous(True)
client.simxGetSimulationStepStarted(client.simxDefaultSubscriber(simulationStepStarted))
q, qdot =vrep.getMotorState()
client.simxGetSimulationStepDone(client.simxDefaultSubscriber(simulationStepDone))
client.simxStartSimulation(client.simxDefaultPublisher())

q, qdot =vrep.getMotorState()


startTime=time.time()
while time.time()<startTime+5: 
    if vrep.doNextStep:
        vrep.doNextStep=False        
        client.simxSynchronousTrigger()
        #q, qdot =vrep.getMotorState()
        vrep.setMotorState(np.array(np.ones(cf.dof)*1.0))   
    client.simxSpinOnce()
    #q, qdot =vrep.getMotorState()

client.simxStopSimulation(client.simxDefaultPublisher())

print "finished"