#!/usr/bin/python                                                                                                                                                                                                                     
import numpy
import matplotlib
import re

from matplotlib import pyplot as plt

#Current Input
#1.000000e+00    ((1.460676e+04 -1.948520e+02 9.535164e+02) (2.508036e-02 -6.720399e-05 -3.082446e-04) (0.000000e+00 0.000000e+00 0.000000e+00)) ((1.140514e+04 1.153182e+05 -1.730316e+05) (-3.153913e-03 1.658614e-01 -2.916495e-01\
#) (0.000000e+00 0.000000e+00 0.000000e+00)                                                                                                                                                                                            

#forceRegex=r"([0-9.Ee\-+]+)\s+\(+([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)+\)+\s+\(+([0-9.Ee\-+]+)"
forceRegex=r"([0-9.Ee\-+]+)\s+\(+([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)+\)+\s+\(+([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)+\)+\s+\(+([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)+\)+\s+\(+([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)+\)+\s+\(+([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)+\)+\s+\(+([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)\s([0-9.Ee\-+]+)+\)"

rhoNorm = 1.4
rhoReal = 1.13
vNorm = 1.1 
vReal = 345
muNorm = 5.45e-08
muReal = 1.8e-05
scaling = -(rhoReal/rhoNorm) * (vReal/vNorm)**2
scalingViscous = -(muReal)/(muNorm) * (vReal/vNorm)

#setup arrays
t = []
fpx = []; fpy = []; fpz = []; #Pressure
fpx1 = []; fpy1 = []; fpz1 = []; #Pressure  
fvx = []; fvy = []; fvz = []; #Pressure                                                                                                                                                                                                                                                                                                                                                                                              
fvx1 = []; fvy1 = []; fvz1 = []; #Pressure                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
mpx = []; mpy = []; mpz = []; #Moment Pressure                                                                                                                                                                                        
mpx1 = []; mpy1 = []; mpz1 = []; #Moment Pressure                                                                                                                                                                                                                                                                                                                                                                                

#read the .dat files
pipefileDart=open('../Martlet3/turbulentM1p1A5/postProcessing/forcesCore/0/forces.dat','r')
pipefileCore=open('../Martlet3/turbulentM1p1A5/postProcessing/forcesDart/0/forces.dat','r')

linesDart = pipefileDart.readlines()
linesCore = pipefileCore.readlines()

#iterate through to match to the forceRegex pattern
lth=len(linesDart);print(lth)

for i in xrange(0, lth, lth/200):
	match=re.search(forceRegex, linesDart[i])
	if match:
		t.append(float(match.group(1)))
		fpx.append(float(match.group(2)))
		fpy.append(float(match.group(3)))
		fpz.append(float(match.group(4)))
		fvx.append(float(match.group(5)))
		fvy.append(float(match.group(6)))
		fvz.append(float(match.group(7)))
		mpx.append(float(match.group(11)))
		mpy.append(float(match.group(12)))
		mpz.append(float(match.group(13)))				   

	match1=re.search(forceRegex, linesCore[i])
	if match1:
		fpx1.append(float(match1.group(2)))
		fpy1.append(float(match1.group(3)))
		fpz1.append(float(match1.group(4)))
		fvx1.append(float(match.group(5)))
		fvy1.append(float(match.group(6)))
		fvz1.append(float(match.group(7)))
		mpx1.append(float(match.group(11)))
		mpy1.append(float(match.group(12)))
		mpz1.append(float(match.group(13)))

#scale the arrays, find the separation force
fpx = [x * scaling for x in fpx]
fpz = [x * scaling for x in fpz]
fpy = [x * scaling for x in fpy]
fvx = [x * scalingViscous for x in fvx]
fvy = [x * scalingViscous for x in fvy]
fvz = [x * scalingViscous for x in fvz]
mpx = [x * scaling for x in mpx]
mpy = [x * scaling for x in mpy]
mpz = [x * scaling for x in mpz]

fpy1 = [x * scaling for x in fpy1]
fvy1 = [x * scalingViscous for x in fvy1]
sep = numpy.subtract(fpy1, fpy)

#plot the forces
plt.figure()
plt.xlabel('Simulation time (sec)')
plt.ylabel('Forces (N)')
plt.plot(t, fpy,'g', label = "Force Pressure core y")
plt.plot(t, fpy1,'b', label = "Force Pressure dart y")
#plt.plot(t, mpz, 'c', label = "Restoring moment")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
		  ncol=3, fancybox=True, shadow=True)
output = "restoringMoment.pdf"
plt.savefig(output, format='PDF')

