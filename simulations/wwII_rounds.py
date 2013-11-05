import sys
src_directory = '../'
sys.path.append(src_directory)

from src.Cartridge  import *
from src.Ballistics import *
from src.functions  import *
from numpy          import array
import src.model

# Initial Conditions
name    = '7.92 x 57 mm 198 gr Bullet'
mass    = 198 
mv      = 760
caliber = 0.32
bc      = 0.593
mauser  = Cartridge(name, mass, caliber, mv, bc)

name    = '.30-06 150 gr Bullet'
mass    = 150
mv      = ft_to_m(2910)
caliber = .308
bc      = .387
threeO  = Cartridge(name, mass, caliber, mv, bc)

name    = '.50 BMG 661 gr Bullet'
mass    = 661
mv      = ft_to_m(2750)
caliber = .51
bc      = .62
fifty   = Cartridge(name, mass, caliber, mv, bc)

name    = 'XM855 5.56x45 mm 62 grain bullet'
mass    = 62
mv      = ft_to_m(3090)
caliber = 0.224
bc      = 0.307
XM855   = Cartridge(name, mass, caliber, mv, bc)

name    = "0.338 Lapua Mag no. 4 PL 8013 300 grain"
mass    = 300
mv      = ft_to_m(2723)
caliber = 0.338
bc      = 0.736
lapua   = Cartridge(name, mass, caliber, mv, bc)

name    = ".338 Win. Mag. PRC338WA 225 grain bullet"
mass    = 225
mv      = ft_to_m(2780)
caliber = 0.338
bc      = 0.456
winMag  = Cartridge(name, mass, caliber, mv, bc)

# array of cartridges :
carts   = array([mauser, threeO, fifty, XM855, lapua, winMag])

# Ballistics model for round 
# (cart, intMethod, t0, tf, dt, intDt) :
ball    = Ballistics(carts, 'Predictor', 0.0, 1.0, 0.001, 0.001)

# Zero the rifle :
ball.hit_target(300)

# Plot the results :
ball.plot_all(units='i')


