#!/usr/bin/env python
from scipy.integrate.ode import *

import Euler as Euler
import EulerRichardson as EulerRichardson
import EulerCromer as EulerCromer

from numpy import arange,vstack,array
from pylab import plot,clf,show,xlabel,ylabel,title,grid,legend
 
# Function defining derivates as a function of the positions and velocities.
# This is the INTERACTION, the inputs to this function are OBSERVABLES.
def sho(t,y,k,m):
# INPUTS:
# t time, only used in non-autonomous systems.
# y[0] the x-position
# y[1] the velocity
# k Spring constant
# m Mass
# OUTPUTS:
# dxdt derivative of the position = velocity
# dvdt acceleration, Newton's second law, here for a spring a = -k/m x
    return array([y[1], -k/m*y[0]])
 
# Initial Conditions
y0, t0 = [1.,0.], 0.
 
# Model parameters these and the observables define the COMPONENT
k = 1.      # Spring constant
m = 9.      # Mass on the Spring



# CREATE ODE OBJECTS
i = ode(sho)

i.set_integrator('Euler',dt=.05)

i.set_initial_value(y0,t0)

i.set_f_params(k,m)

tf = 200.                  # Final time
dt = .2                    # Output interval

yfE = [array(y0)]
yfER = [array(y0)]
yfEC = [array(y0)]

time = arange(t0,tf,dt)    # Times to evaluate a solution. 
 
# Main loops for the integration
# Euler Method:
for t in time:
    i.integrate(i.t+dt)
    yfE.append(i.y)


# Euler-Richardson Method:
i.set_integrator('EulerRichardson',dt=.05)
i.set_initial_value(y0,t0)
i.set_f_params(k,m)
for t in time:
    i.integrate(i.t+dt)
    yfER.append(i.y)


# Euler-Cromer Method:
i.set_integrator('EulerCromer',dt=.05)
i.set_initial_value(y0,t0)
i.set_f_params(k,m)
for t in time:
    i.integrate(i.t+dt)
    yfEC.append(i.y)

 
# Convert return list to array:
yfE = array(yfE)
yfER = array(yfER)
yfEC = array(yfEC)
 
# Plot the results
clf()
plot(time,yfE[1:,0])   # The 0 column is position, 1 is velocity
plot(time,yfER[1:,0])
plot(time,yfEC[1:,0],'r--')
xlabel('Time (s)')
ylabel('Position (m)')
title('Simple Harmonic Motion')
legend(('Euler', 'Euler-Richardson', 'Euler-Cromer'), loc=2)
grid()
show()


