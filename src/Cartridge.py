from numpy import *
from functions import *
from model import *

class Cartridge:
    """
    A data object representing a cartridge.

    __author__ = 'Jon-Michael Deldin and me'
    __date__   = '2012-02-13'
    """
    def __init__(self, name, mass, caliber, mv, bc, theta=0.0, traj=None, 
                 x=None, units='m', velocity=None, vel_x=None, model=None,
                 long_traj=None, l_x=None):
        """
        INPUTS:
          name       -- bullet name
          units      -- units - [m] = metric, [i] = imperial
          mass       -- weight of bullet in grains
          traj       -- array of short-range trajectories yard intervals
          x          -- list of s_traj x-positions
          caliber    -- diameter of bullet in inches
          mv         -- muzzle velocity
          bc         -- ballistics coefficent
          velocity   -- list of v's at 100 intervals
          vel_x      -- list of velocity x-positions
          long_traj  -- array of long-rage trajectories at yard intervals
          l_x        -- list of l_traj x-positions
        OUTPUTS:
          name       -- bullet name
          mass       -- weight of bullet in grams
          velocity   -- list of v's at 100 m intervals - m/s
          vel_x      -- list of velocity x-positions - m/s
          traj       -- array of short-range trajectories intervals - m
          x          -- list of traj x-positions - m
          l_traj     -- array of long-rage trajectories intervals - m
          l_x        -- list of l_traj x-positions - m
          caliber    -- diameter of bullet in inches
          mv         -- muzzle velocity - m/s
          theta      -- initial radian angle of bullet trajectory to +x axis
          A          -- cross-sectional area - m^2
          ff         -- ?
          y          -- trajectory info list [x, vx, y, vy]
        """
        self.name       = name
        self.mass       = grains_to_g(mass)
        self.cal        = caliber
        self.mv         = mv
        self.bc         = bc
        self.A          = pi * (inches_to_m(self.cal/2.0))**2
        self.ff         = self.A / self.bc
        self.y          = []
        self.theta      = theta
        self.y0         = []
        if model == None:
          self.model    = G1
        else:
          self.model    = model
        
        # if traject ry information is provided :
        if traj != None:
          if type(traj) == float or type(traj) == int:
            self.traj  = array([traj])
            self.x     = array([0.0])
          else:
            self.traj  = array(traj)
            self.x     = array(x)
        else:
          self.traj  = zeros(1)
          self.x     = zeros(1)
        
        # load initial values :
        vx, vy = vel_comp(self.mv, self.theta)
        self.y0 = [0.0, vx, self.traj[0], vy]

        # if velocity information is provided :
        if velocity != None:
          self.vel   = array(velocity)
          self.vel_x = array(vel_x)
        else:
          self.vel   = None
          self.vel_x = None
        
        # if long-range trajectory info is provided :
        if long_traj != None:
          self.l_traj = array(long_traj)
          self.l_x    = array(l_x)
        else:
          self.l_traj = None
          self.l_x    = None
        
        # convert to metric if needed :
        if units == 'i':
          self.mv     = ft_to_m(self.mv)
          self.vel    = ft_to_m(self.vel)
          self.vel_x  = yards_to_m(self.vel_x)
          self.traj   = inches_to_m(self.traj)
          self.x      = yards_to_m(self.x)
          self.l_traj = inches_to_m(self.l_traj)
          self.l_x    = yards_to_m(self.l_x)


