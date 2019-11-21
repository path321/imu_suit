import numpy as np

def linearMap(value,newMax,newMin,oldMax,oldMin):  #Map values to new limits
        return (value-oldMin)*(newMax-newMin)/(oldMax-oldMin)+newMin


def appendData(myList,val): #Update the graph line with new data
        lenList = len(myList)
        myList=np.append(myList,val)
        myList=myList[-lenList:]
        return myList
