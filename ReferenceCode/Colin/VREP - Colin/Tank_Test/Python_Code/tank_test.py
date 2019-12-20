import b0RemoteApi
import time
from msvcrt import getch

left_front_handle = None
left_back_handle = None
right_back_handle = None
right_front_handle = None

sj_l_1_handle = None
sj_l_2_handle = None
sj_l_3_handle = None
sj_l_4_handle = None
sj_l_5_handle = None
sj_l_6_handle = None

sj_r_1_handle = None
sj_r_2_handle = None
sj_r_3_handle = None
sj_r_4_handle = None
sj_r_5_handle = None
sj_r_6_handle = None

MaxVel = None
leftvelocity = None
rightvelocity = None
dVel = None

with b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient','b0RemoteApi') as client:    
    doNextStep=True

def simulationStepStarted(msg):
    simTime=msg[1][b'simulationTime']
    print('Simulation step started. Simulation time: ',simTime)
    
def simulationStepDone(msg):
    simTime=msg[1][b'simulationTime']
    print('Simulation step done. Simulation time: ',simTime)
    global doNextStep
    doNextStep=True

def sysCall_init():
    client.simxStartSimulation(client.simxDefaultPublisher())
    client.simxAddStatusbarMessage('Hello world!',client.simxDefaultPublisher())
    global left_front_handle
    global left_back_handle
    global right_back_handle
    global right_front_handle
    left_front_handle = client.simxGetObjectHandle('left_front', client.simxServiceCall())
    left_back_handle = client.simxGetObjectHandle('left_back', client.simxServiceCall())
    right_back_handle = client.simxGetObjectHandle('right_back', client.simxServiceCall())
    right_front_handle = client.simxGetObjectHandle('right_front', client.simxServiceCall())

    global sj_l_1_handle
    global sj_l_2_handle
    global sj_l_3_handle
    global sj_l_4_handle
    global sj_l_5_handle
    global sj_l_6_handle
    sj_l_1_handle = client.simxGetObjectHandle('sj_l_1', client.simxServiceCall())
    sj_l_2_handle = client.simxGetObjectHandle('sj_l_2', client.simxServiceCall())
    sj_l_3_handle = client.simxGetObjectHandle('sj_l_3', client.simxServiceCall())
    sj_l_4_handle = client.simxGetObjectHandle('sj_l_4', client.simxServiceCall())
    sj_l_5_handle = client.simxGetObjectHandle('sj_l_5', client.simxServiceCall())
    sj_l_6_handle = client.simxGetObjectHandle('sj_l_6', client.simxServiceCall())
    
    global sj_r_1_handle
    global sj_r_2_handle
    global sj_r_3_handle
    global sj_r_4_handle
    global sj_r_5_handle
    global sj_r_6_handle
    sj_r_1_handle = client.simxGetObjectHandle('sj_r_1', client.simxServiceCall())
    sj_r_2_handle = client.simxGetObjectHandle('sj_r_2', client.simxServiceCall())
    sj_r_3_handle = client.simxGetObjectHandle('sj_r_3', client.simxServiceCall())
    sj_r_4_handle = client.simxGetObjectHandle('sj_r_4', client.simxServiceCall())
    sj_r_5_handle = client.simxGetObjectHandle('sj_r_5', client.simxServiceCall())
    sj_r_6_handle = client.simxGetObjectHandle('sj_r_6', client.simxServiceCall())

    global MaxVel
    global leftvelocity
    global rightvelocity
    global dVel
    MaxVel = 10
    leftvelocity = 100
    rightvelocity = 0
    dVel = 0.5

    #client.simxSetJointTargetVelocity(left_front_handle,leftvelocity, client.simxServiceCall())
    client.simxSetJointTargetVelocity(left_back_handle,leftvelocity, client.simxServiceCall())
    client.simxSetJointTargetVelocity(right_back_handle,rightvelocity, client.simxServiceCall())
    #client.simxSetJointTargetVelocity(right_front_handle,rightvelocity, client.simxServiceCall())


def sysCall_actuation():
    #message,auxiliaryData = sim.getSimulatorMessage()
    while (True):
        key = ord(getch())
        if (key == 32):
            # spacebar
            leftvelocity=0
            rightvelocity=0
            client.simxSetJointForce(left_front_handle, 0, client.simxServiceCall())
            client.simxSetJointForce(left_back_handle, 0, client.simxServiceCall())
            client.simxSetJointForce(right_back_handle, 0, client.simxServiceCall())
            client.simxSetJointForce(right_front_handle, 0, client.simxServiceCall())


            client.simxSetJointForce(sj_r_1_handle, 1000, client.simxServiceCall())
            client.simxSetJointForce(sj_r_2_handle, 1000, client.simxServiceCall())
            client.simxSetJointForce(sj_r_3_handle, 1000, client.simxServiceCall())
            client.simxSetJointForce(sj_r_4_handle, 1000, client.simxServiceCall())
            client.simxSetJointForce(sj_r_5_handle, 1000, client.simxServiceCall())
            client.simxSetJointForce(sj_r_6_handle, 1000, client.simxServiceCall())

            client.simxSetJointForce(sj_l_1_handle, 1000, client.simxServiceCall())
            client.simxSetJointForce(sj_l_2_handle, 1000, client.simxServiceCall())
            client.simxSetJointForce(sj_l_3_handle, 1000, client.simxServiceCall())
            client.simxSetJointForce(sj_l_4_handle, 1000, client.simxServiceCall())
            client.simxSetJointForce(sj_l_5_handle, 1000, client.simxServiceCall())
            client.simxSetJointForce(sj_l_6_handle, 1000, client.simxServiceCall())
            break
        else:
            #client.simxSetJointForce(left_front_handle, 10000, client.simxServiceCall())
            client.simxSetJointForce(left_back_handle, 10000, client.simxServiceCall())
            client.simxSetJointForce(right_back_handle, 10000, client.simxServiceCall())
            #client.simxSetJointForce(right_front_handle, 10000, client.simxServiceCall())

            client.simxSetJointForce(sj_r_1_handle, 0, client.simxServiceCall())
            client.simxSetJointForce(sj_r_2_handle, 0, client.simxServiceCall())
            client.simxSetJointForce(sj_r_3_handle, 0, client.simxServiceCall())
            client.simxSetJointForce(sj_r_4_handle, 0, client.simxServiceCall())
            client.simxSetJointForce(sj_r_5_handle, 0, client.simxServiceCall())
            client.simxSetJointForce(sj_r_6_handle, 0, client.simxServiceCall())

            client.simxSetJointForce(sj_l_1_handle, 0, client.simxServiceCall())
            client.simxSetJointForce(sj_l_2_handle, 0, client.simxServiceCall())
            client.simxSetJointForce(sj_l_3_handle, 0, client.simxServiceCall())
            client.simxSetJointForce(sj_l_4_handle, 0, client.simxServiceCall())
            client.simxSetJointForce(sj_l_5_handle, 0, client.simxServiceCall())
            client.simxSetJointForce(sj_l_6_handle, 0, client.simxServiceCall())
        
        if (key == 2007):
            # up key
            leftvelocity = (leftvelocity + rightvelocity) / 2
            rightvelocity = leftvelocity
            leftvelocity = leftvelocity + dVel
            rightvelocity = rightvelocity + dVel
        
        if (key == 2008):
            # down key
            leftvelocity=(leftvelocity+rightvelocity)/2
            rightvelocity=leftvelocity
            leftvelocity=leftvelocity-dVel
            rightvelocity=rightvelocity-dVel
        
        if (key == 2009):
            # left key
            leftvelocity=leftvelocity-dVel
            rightvelocity=rightvelocity+dVel
        
        if (key == 2010):
            # right key
            leftvelocity=leftvelocity+dVel
            rightvelocity=rightvelocity-dVel    
    
    if (leftvelocity > MaxVel):
        leftvelocity = MaxVel
    
    if (leftvelocity < -1*MaxVel):
        leftvelocity = -1*MaxVel
    
    
    if (rightvelocity > MaxVel):
        rightvelocity = MaxVel
    
    if (rightvelocity < -1*MaxVel):
        rightvelocity = -1*MaxVel
    
    
    #client.simxSetJointTargetVelocity(left_front_handle,leftvelocity, client.simxServiceCall())
    client.simxSetJointTargetVelocity(left_back_handle,leftvelocity, client.simxServiceCall())
    client.simxSetJointTargetVelocity(right_back_handle,rightvelocity, client.simxServiceCall())
    #client.simxSetJointTargetVelocity(right_front_handle,rightvelocity, client.simxServiceCall())


startTime=time.time()
while time.time()<startTime+60: 
    if doNextStep:
        doNextStep=False
        client.simxSynchronousTrigger()
    client.simxSpinOnce()
client.simxStopSimulation(client.simxDefaultPublisher())

if __name__ == "__main__":
    sysCall_init()
    while doNextStep:
        sysCall_actuation()