#    Copyright (C) <2012>  <cummings.evan@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
sys.path.append("../../ode_solvers/src")

from Predictor            import *
from RungeKutta           import *
from EulerRichardson      import *
from Euler                import *
from EulerCromer          import *
from scipy.integrate._ode import *
from scipy.interpolate    import interp1d
from Cartridge            import *
from numpy                import *

import functions as func
import random
import matplotlib.pyplot as plt

class Ballistics:

  def __init__(self, cart, intMethod, t0, tf, dt, intDt, y0=0.0,
               model='g', rho=1.225):
    '''
    Purpose:
      Initialize the variables and data.
    INPUT:
      cart      - a Cartridge object.
      intMethod - string name of integration method choices are:
                  {RungeKutta, Predictor, EulerRichardson, Euler,
                   EulerCromer}
      traj      - trajectory choice {s, l}
      t0        - initial time in seconds
      tf        - end time in seconds
      dt        - time step to call integrator in seconds
      intDt     - time step for integrator to integrate in seconds
      y0        - initial height of bullet
      model     - model to use {g or e}
      rho       - density of fluid (air) in kg/m^3
    '''
    self.n            = len(cart)
    self.cart         = cart    # array of cartridge objects
    self.g            = 32.174  # ft/sec for model coefficients
    self.intDt        = intDt
    self.t0           = t0
    self.dt           = dt
    self.times        = arange(t0,tf,dt)
    self.intMethod    = intMethod
    self.model        = model
    self.rho          = rho
    self.vx           = zeros(self.n)
    self.vy           = zeros(self.n)
    self.x0           = []
    self.y0           = y0


  def model_integrate(self, cart):
    '''
    PURPOSE:
      Integrate through the model using the initialized parameters.
    INPUTS:
      model - {g,e} g = G model , e = Evan's model
    '''
    if self.model == 'g':
      i = ode(func.fbar_gmodel)
      i.set_f_params(self.g, cart.bc, cart.model)
    elif self.model == 'e':
      i = ode(func.fbar_emodel)
      i.set_f_params(self.g, cart.mass, self.rho, cart.A)
    
    i.set_integrator(self.intMethod, dt=self.intDt)
    i.set_initial_value(cart.y0, self.t0)
    cart.y.append(cart.y0)
    for t in self.times:
      i.integrate(i.t + self.dt)
      cart.y.append(i.y)
    cart.y = array(cart.y)


  def find_theta(self, cart, rng, tol, zero):
    '''
    PURPOSE:
      Find the optimal theta to range in the rifle.
    INPUTS:
      Theta - angle (begins with 0.0 rad)
      dist  - target range in meters
      zero  - distance from zero (default 0.0)
    OUTCOME:
      Ballistics.theta is changed to optimal theta (err < 0.01 inches)
    '''
    cart.y = []  # initialize the history for (new) shot
    vx, vy  = func.vel_comp(cart.mv, cart.theta)
    cart.y0 = [0.0, vx, cart.traj[0], vy]
    self.model_integrate(cart)
    
    x = cart.y[:,0]           # x-position
    y = cart.y[:,2]           # y-position
    f = interp1d(x, y)
    xint = array([rng])
    yint = f(xint)
    print 'yErr:', yint[0], '\ttheta:', cart.theta, '\tzero:', zero
    yErr = yint[0]
    
    if (yErr < zero and yErr > zero - tol) or \
       (yErr > zero and yErr < zero + tol):
      None
    elif yErr > zero + tol:
      cart.theta = cart.theta - math.atan( (abs(yErr) + zero) / rng ) / 1.15
      self.find_theta(cart, rng, tol, zero)
    elif yErr < zero - tol:
      cart.theta = cart.theta + math.atan( (abs(yErr) + zero) / rng ) / 1.15
      self.find_theta(cart, rng, tol, zero)


  def hit_target(self, rng, tol=1e-5, zero=0.0):
    '''
    PURPOSE:
      Method to begin zero the rifle on desired range and model trajectory.
    INPUT:
      rng  - the zeroed range in yards you want to hit.
      zero - distance from zero (default 0.0)
    OUTCOME:
      trajectory saved to Ballistics.x as a numpy array [x, vx, y, vy]
    '''
    for i in range(self.n):
      self.find_theta(self.cart[i], rng, tol, zero)
  
  
  def calc_error(self, cart):
    
    # model results:   
    x = cart.y[:,0]           # x-position
    y = cart.y[:,2]           # y-position
    v = sqrt(cart.y[:,1]**2 + cart.y[:,3]**2)  # velocity
    
    if len(cart.traj) > 1:
      # for quantitative analysis:
      f = interp1d(x, y)
      xint = array(cart.x)
      yint = f(xint)
      # compute mean square error:
      yErr = sqrt(sum((yint - cart.traj)**2/len(yint)))
    else:
      yErr = 0

    if cart.vel != None and len(cart.traj) > 1:
      f = interp1d(x, v)
      xint = array(cart.vel_x)
      vint = f(xint)
      # compute mean square error:
      vErr = sqrt(sum((vint - cart.vel)**2/len(vint)))
    else:
      vErr = 0
    
    return x, y, v, yErr, vErr


  def plot(self, cart, units='m'):
    '''
    Purpose:
      plot the trajectory and velocity for the data and model given.
    '''
    x, y, v, yErr, vErr = self.calc_error(cart)
        
    fig = plt.figure(figsize=(14,10))
    ax = fig.add_subplot(211)
    
    if units != 'm':
      x = func.m_to_yards(x)
      y = func.m_to_inches(y)
      v = func.m_to_ft(v)
      traj_x = func.m_to_yards(traj_x)
      traj   = func.m_to_inches(traj)
      xunit = 'yards'
      yunit = 'inches'
      vunit = 'feet/s'
    else:
      xunit = 'm'
      yunit = 'm'
      vunit = 'm/s'

    if len(cart.traj) > 1:
      plt.plot(cart.traj_x, 
               cart.traj, 'r.', label='Data')
    plt.plot(x, y, label=self.intMethod, lw=2)
    plt.text(min(x) + 10, min(y) + (max(y) - min(y))/10.0, 
             'Mean-Squared Err: %f m' % yErr)
    plt.text(min(x) + 10, min(y) + (max(y) - min(y))/100.0, 
             'Muzzle Velocity: %.0f m/s' % cart.mv)
    leg = plt.legend(loc='lower left')
    leg.get_frame().set_alpha(0.5)
    plt.xlabel('Distance (%s)' % xunit)
    plt.ylabel('Drop (%s)' % yunit)
    plt.title('Trajectory for ' + cart.name)
    plt.grid()
    
    ax = fig.add_subplot(212)
    
    if cart.vel != None:
      plt.plot(cart.vel_x, 
               cart.vel, 'r.', label='Data')
      plt.text(min(x)+10, min(v)+10 , 'Mean-Squared Err: %f m/s' % (vErr))
    
    plt.plot(x, v, label=self.intMethod, lw=2)
    plt.xlabel('Distance (%s)' % xunit)
    plt.ylabel('Velocity (%s)' % vunit)
    plt.title('Velocity for ' + cart.name)
    plt.grid()
    
    plt.show()


  def plot_all(self, units='m'):
    '''
    Purpose:
      plot the trajectory and velocity for the data and model given.
    '''
    fig = plt.figure(figsize=(12,6))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    
    for i in range(self.n):
      x, y, v, yErr, vErr = self.calc_error(self.cart[i])
    
      if units != 'm':
        x = func.m_to_yards(x)
        y = func.m_to_inches(y)
        v = func.m_to_ft(v)
        traj_x = func.m_to_yards(self.cart[i].x)
        traj   = func.m_to_inches(self.cart[i].traj)
        xunit = 'yards'
        yunit = 'inches'
        vunit = 'feet/s'
      else:
        xunit = 'm'
        yunit = 'm'
        vunit = 'm/s'
      
      if len(self.cart[i].traj) > 1:
        ax1.plot(traj_x, traj,
                 'r.', label='%s Data' % self.cart[i].name)
      ax1.plot(x, y, lw=2, 
               label=self.cart[i].name)
    
      if self.cart[i].vel != None:
        ax2.plot(self.cart[i].vel_x, self.cart[i].vel,
                 'r.', label='%s Data' % self.cart[i].name)
      ax2.plot(x, v, lw=2, 
               label=self.cart[i].name)
    
    leg = ax1.legend(loc='lower left')
    leg.get_frame().set_alpha(0.5)
    ax1.set_xlabel('Distance (%s)' % xunit)
    ax1.set_ylabel('Drop (%s)' % yunit)
    ax1.grid()
    leg = ax2.legend()
    leg.get_frame().set_alpha(0.5)
    ax2.set_xlabel('Distance (%s)' % xunit)
    ax2.set_ylabel('Velocity (%s)' % vunit)
    ax2.grid()
    
    plt.show()


  def test_model_plot(self, G):
    '''
    Purpose:
      Plot random numbers on the plot of model G to test accurate
      interpolation.
    '''
    rand = []
    for i in range(200):
      num = random.uniform(G[0,0], G[-1,0])
      a, m = func.g_param(G, num)
      rand.append([num,a,m])
    rand = array(rand)
    
    fig = plt.figure()
    ax = fig.add_subplot(211, 
                         autoscale_on=False, 
                         xlim=(min(G[:,0]), max(G[:,0])), 
                         ylim=(min(G[:,1]), max(G[:,1])) )
    
    plt.plot(G[:,0], G[:,1], 'r-', label='A' )
    plt.plot(rand[:,0], rand[:,1], 'k.', label='Interpolations')
    
    plt.legend()
    plt.xlabel('Velocity (ft/s)')
    plt.ylabel('A ()')
    plt.title('Random Velocity Interpolations of Ballistics Model')
    plt.grid()
    
    ax = fig.add_subplot(212, 
                         autoscale_on=False, 
                         xlim=(min(G[:,0]), max(G[:,0])),
                         ylim=(min(G[:,2]), max(G[:,2])) )
    
    plt.plot(G[:,0], G[:,2], 'r-', label='M' )
    plt.plot(rand[:,0], rand[:,2], 'k.', label='Interpolations')
    
    plt.legend()
    plt.xlabel('Velocity (ft/s)')
    plt.ylabel('M ()')
    plt.grid()
    
    plt.show()



