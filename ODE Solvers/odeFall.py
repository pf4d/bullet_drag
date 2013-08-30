#!/usr/bin/env python
from scipy.integrate.ode import *
 
import Euler as Euler
import EulerRichardson as EulerRichardson
import EulerCromer as EulerCromer
import Predictor as Predictor
import RungeKutta as RungeKutta
 
from numpy import arange,vstack,array, sqrt
from pylab import *




# Function defining derivates as a function of the positions and velocities.
# This is the INTERACTION, the inputs to this function are OBSERVABLES.
def nugf(t, y, M, m, G, R):
  """
  INPUTS:
    t time, only used in non-autonomous systems.
    y[0] the x-position
    y[1] the velocity
    M - Earth's mass
    m - Mass of object
    G - Gravitational const
    R - Radius of Earth
  OUTPUTS:
    dxdt derivative of the position = velocity
    dvdt acceleration, Newton's second law a = F/m
      where F = (G*M*m)/(R + y[0])**2
  """
  F = -(G*M*m)/(R + y[0])**2
  return array( [y[1], F/m] )






# Initial Conditions
y0, t0 = [50.,0.], 0.
tf = 4.              # Final time
dt = .2              # Output interval
 
# Model parameters these and the observables define the COMPONENT
G = 6.67384e-11      # Gravitational constant
M = 5.9722e24        # Mass of Earth
R = 6.37e6           # Radius of Earth
m = 1.               # Falling mass


# Position arrays
yfE = [array(y0)]
yfEC = [array(y0)]
yfER = [array(y0)]
yfRK = [array(y0)]
yfPC = [array(y0)]

# Times to evaluate a solution. 
time = arange(t0,tf,dt)





# CREATE ODE OBJECTS
i = ode(nugf)

# Main loops for the integration
# Euler Method:
i.set_integrator('Euler',dt=.05)
i.set_initial_value(y0,t0)
i.set_f_params(M, m, G, R)
for t in time:
    i.integrate(i.t+dt)
    yfE.append(i.y)
yfE = array(yfE)

# Euler-Richardson Method:
i.set_integrator('EulerRichardson',dt=.05)
i.set_initial_value(y0,t0)
i.set_f_params(M, m, G, R)
for t in time:
    i.integrate(i.t+dt)
    yfER.append(i.y)
yfER = array(yfER)

# Euler-Cromer Method:
i.set_integrator('EulerCromer',dt=.05)
i.set_initial_value(y0,t0)
i.set_f_params(M, m, G, R)
for t in time:
    i.integrate(i.t+dt)
    yfEC.append(i.y) 
yfEC = array(yfEC)

# RungeKutta Method:
i.set_integrator('RungeKutta',dt=.05)
i.set_initial_value(y0,t0)
i.set_f_params(M, m, G, R)
for t in time:
    i.integrate(i.t+dt)
    yfRK.append(i.y)
yfRK = array(yfRK)

# Predictor-Corrector Method:
i.set_integrator('Predictor',dt=.05)
i.set_initial_value(y0,t0)
i.set_f_params(M, m, G, R)
for t in time:
    i.integrate(i.t+dt)
    yfPC.append(i.y)
yfPC = array(yfPC)




# analytic solution
g = 9.80665
yT = y0[0] - 0.5*g*time**2
yT2 = y0[0] - 0.5*( (G*M)/(R + y0[0])**2 )*time**2




# The discrepancy  between simulated and analytically calculated time at the
# last simulated position, x[-1]
disc = time[-1] - sqrt((yfE[-1][0] - y0[0])/(-.5*g))



# Plot the results
fig = figure()
ax = fig.add_subplot(111, 
                     autoscale_on=False, 
                     xlim=(0,3.5), 
                     ylim=(0,y0[0]+10))

text(0.5, 10, "discrepancy: %f" % (disc))
plot(time, yfE[1:,0], label='Euler')
plot(time, yfER[1:,0], label='Euler-Richardson')
plot(time, yfEC[1:,0], label='Euler-Cromer')
plot(time, yfRK[1:,0], label='Runge-Kutta')
plot(time, yfPC[1:,0], label='Predictor-Corrector')
plot(time,yT2, 'r--', label='Analytical')
#plot(time,yT)

legend()
xlabel('Time (s)')
ylabel('Position (m)')
title('Falling Body')
grid()
show()


