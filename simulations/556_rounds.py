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
caliber = 0.224
bc      = 0.250
XM193   = Cartridge(name, mass, caliber, mv, bc, traj=0.0) 

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

# array of cartridges :
#carts   = array([XM855, XM193])
carts   = array([XM855])

# Ballistics model for round 
# (cart, intMethod, t0, tf, dt, intDt) :
ball    = Ballistics(carts, 'Predictor', t0=0.0, tf=0.168, 
                     dt=0.001, intDt=0.001)

# Zero the rifle :
ball.hit_target(300)

# Plot the results :
ball.plot_all(units='i')



