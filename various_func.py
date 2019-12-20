import numpy as np
from subprocess import run,PIPE


def linearMap(value,newMax,newMin,oldMax,oldMin):
        "Map values to new limits"
        return (value-oldMin)*(newMax-newMin)/(oldMax-oldMin)+newMin


def appendData(myList,val):
        '''Perfrom FIFO insertion in a list
           alternative : deque.append() deque.pop()'''
        lenList = len(myList)
        myList=np.append(myList,val)
        myList=myList[-lenList:]
        return myList
        
def lowPass(now,prev,a):
        "1st order low pass filter in 1D"
        return (a*now + (1-a)*prev)

def lowPass2(now,prev,prev2):
        "2nd order low pass filter in 1D"
        return (0.7*now + 0.2*prev+ 0.1*prev2)

def checkAz(inpt,limit):
        "Limit input in [limit,-limit)"
        if(inpt > limit):
                inpt -= limit*2
        elif(inpt <= -limit):
                inpt += limit*2
        return inpt

def runBash(inpt):
        '''Run bash commands in terminal , get output and error
        !! Security hazard, User beware of the input command !!
        '''
        bashCommand = inpt 
        process = run(bashCommand,shell=True, stderr=PIPE, stdout=PIPE, universal_newlines=True)
        output = (process.stdout).strip()
        error = (process.stderr).strip()
        return output,error



