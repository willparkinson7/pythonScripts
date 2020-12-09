import re, sys, os, operator, csv
import pandas as pd
import plotly
import plotly.graph_objs as go
import numpy as np
floatRegArray = [256, 512, 1024, 2048, 4096]
instEntArray = [4, 8 ,16, 32, 64, 128, 256]
reorderEntArray = instEntArray
labels = ["sim_seconds", 
         "system.cpu.rename.IdleCycles", 
         "system.cpu.rename.ROBFullEvents",
         "system.cpu.iq.rate"]
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
header = ["floatReg","instEntry", "reorderEntry","simulation Seconds", "Idle Cycles from Register Renaming", "Rename block due to ROB", "instruction issue rate"]
append_list_as_row("hwk4.csv",header)
secSimRegex = re.compile(r"(sim_seconds) *([+-]?[0-9]*[.]?[0-9]+)") #grabs the sim_seconds and the number associated with it
idleCycRegex = re.compile(r"(system.cpu.rename.IdleCycles) *([+-]?[0-9]*[.]?[0-9]+)")
robFullRegex = re.compile(r"(system.cpu.rename.ROBFullEvents) *([+-]?[0-9]*[.]?[0-9]+)")
issueRateRegex = re.compile(r"(system.cpu.iq.rate) *([+-]?[0-9]*[.]?[0-9]+)")
simSecArray = []
issueRateArray=[]
numROBEntryArr =[]
numIQEntryArr = []
numPhysFloatRegArr = []
for numFloatReg in floatRegArray:
    for numInstEnt in instEntArray:
        for reorderInst in reorderEntArray:
            numROBEntryArr.append(reorderInst)
            numIQEntryArr.append(numInstEnt)
            numPhysFloatRegArr.append(numFloatReg)
            filename = "stats"+str(numFloatReg)+"_" + str(numInstEnt) + "_" + str(reorderInst) + ".txt"
            with open(filename) as f:
                for line in f:
                    line = line.strip()
                    secMatch = secSimRegex.match(line)
                    idleMatch = idleCycRegex.match(line)
                    robMatch = robFullRegex.match(line)
                    issueMatch = issueRateRegex.match(line)
                    if secMatch is not None:
                        simSec = secMatch.group(2)
                        simSecArray.append(simSec)
                    elif idleMatch is not None:
                        idleEntry = idleMatch.group(2)
                        
                    elif robMatch is not None:
                        robEntry = robMatch.group(2)
                    elif issueMatch is not None:
                        issueRate = issueMatch.group(2)
                        issueRateArray.append(issueRate)
            append_list_as_row("hwk4.csv", [numFloatReg,numInstEnt, reorderInst,simSec, idleEntry, robEntry, issueRate])
            f.close

data = pd.read_csv("hwk4.csv")
markercolor = data['instruction issue rate'].values.astype(float)

fig1 = go.Scatter3d(x=data['instEntry'],y=data['reorderEntry'],z=data['floatReg'],marker=dict(color=markercolor,
                                opacity=1,
                                reversescale=True,
                                colorscale='Viridis',
                                size=5, colorbar=dict(thickness=20)),
                    line=dict (width=0.02),
                    mode='markers', )

mylayout = go.Layout(scene=dict(xaxis=dict( title="Number of IQ Entries"),
                                yaxis=dict( title="Number of ROB Entries"),
                                zaxis=dict(title="Number of Phys Float Regs")),title="Instruction Issue Rate vs IQ, ROB, and Float Reg")

plotly.offline.plot({"data": [fig1],
                     "layout": mylayout},
                     auto_open=True,
                     filename=("InstIssueRatePlot.html"))


markercolor = data['simulation Seconds'].values.astype(float)

fig2 = go.Scatter3d(x=data['instEntry'],y=data['reorderEntry'],z=data['floatReg'],marker=dict(color=markercolor,
                                opacity=1,
                                reversescale=True,
                                colorscale='Viridis',
                                size=5, colorbar=dict(thickness=20)),
                    line=dict (width=0.02),
                    mode='markers', )

mylayout = go.Layout(scene=dict(xaxis=dict( title="Number of IQ Entries"),
                                yaxis=dict( title="Number of ROB Entries"),
                                zaxis=dict(title="Number of Phys Float Regs")),title="Simulation Seconds vs IQ, ROB, and Float Reg")

plotly.offline.plot({"data": [fig2],
                     "layout": mylayout},
                     auto_open=True,
                     filename=("SimSecondsPlot.html"))
