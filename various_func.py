import numpy as np
from subprocess import run,PIPE


def linearMap(value,newMax,newMin,oldMax,oldMin):  #Map values to new limits
        return (value-oldMin)*(newMax-newMin)/(oldMax-oldMin)+newMin


def appendData(myList,val): #Update the graph line with new data
        lenList = len(myList)
        myList=np.append(myList,val)
        myList=myList[-lenList:]
        return myList


def runBash(inpt): #Run bash commands in terminal , get output and error
        # !! Security hazard, User beware of the input command !! 
        bashCommand = inpt 
        process = run(bashCommand,shell=True, stderr=PIPE, stdout=PIPE, universal_newlines=True)
        output = (process.stdout).strip()
        error = (process.stderr).strip()
        return output,error
