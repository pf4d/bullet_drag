import sys
src_directory = '../'
sys.path.append(src_directory)

from src.Cartridge  import *
from src.Ballistics import *
from src.functions  import *
from numpy          import array
import src.model

# Initial Conditions
name    = 'XM193 5.56x45 mm 55 grain bullet'
mass    = 55
mv      = ft_to_m(3310)
x       = arange(0, 401, 25)
traj    = [-2.57,
           -0.39,
            1.51,
            3.13,
            4.54,
            5.76,
            6.33,
            6.65,
            6.68,
            6.35,
            5.05,
            3.55,
            1.61,
            -0.95,
            -4.15,
            -8.18,
            -12.52]
traj    = inches_to_m(array(traj))
caliber = 0.224
bc      = 0.250
XM193   = Cartridge(name, mass, caliber, mv, bc, traj=traj, x=x) 

name    = 'XM855 5.56x45 mm 62 grain bullet'
mass    = 62
mv      = ft_to_m(3090)
x       = arange(0, 401, 25)
traj    = [-2.57,
           -0.39,
           1.49,
           3.06,
           4.31,
           5.21,
           5.73,
           5.88,
           5.58,
           4.90,
           3.72,
           2.14,
           -0.04,
           -2.83,
           -6.11,
           -10.09,
           -14.77]
traj    = inches_to_m(array(traj))
caliber = 0.224
bc      = 0.307
XM855   = Cartridge(name, mass, caliber, mv, bc, traj=traj, x=x)

# Ballistics model for round 
# (cart, intMethod, t0, tf, dt, intDt, traj='s', model='g', rho=1.225) :
ball1 = Ballistics(XM855, 'Predictor', 0.0, 0.175, 0.001, 0.001, traj='s')
ball2 = Ballistics(XM193, 'Predictor', 0.0, 0.175, 0.001, 0.001, traj='s')

# Set the deisred model :
ball1.set_g(model.G1)
ball2.set_g(model.G1)

# Zero the rifle :
ball1.hit_target(25, zero=inches_to_m(-0.39))
ball2.hit_target(25, zero=inches_to_m(-0.39))

# Plot the results :
ball1.plot()
ball2.plot()


