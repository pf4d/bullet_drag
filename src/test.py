#!/usr/bin/env python
from Cartridge import *
import model
from Ballistics import *
from functions import array_list_convert, m_to_ft, mm_to_inches, m_to_yards
from numpy import array

# Initial Conditions
name = 'XM193 5.56x45 mm 55 grain bullet'
mass       = 55
vel        = [3290, 
              2827, 
              2409, 
              2028, 
              1686, 
              1394, 
              1170, 
              1029, 
              939, 
              872, 
              815]
vel_x      = [0,
              100,
              200,
              300,
              400,
              500,
              600,
              700,
              800,
              900,
              1000]
s_x = l_x = vel_x
s_traj1    = [0.0, 
              -0.5, 
              -2.2, 
              -5.9, 
              -12.5, 
              -23.9, 
              -42.5, 
              -71.7, 
              -114.7, 
              -174.3, 
              -253.1]
s_traj2    = [0.0, 
              -1.79, 
              -7.96, 
              -20.19, 
              -40.98, 
              -74.15, 
              -125.37, 
              -201.96, 
              -311.26, 
              -460.00, 
              -654.59]
l_traj     = [-1.5, 
              1.4, 
              0.0, 
              -7.5, 
              -23.6, 
              -52.0, 
              -98.5, 
              -170.3, 
              -274.9, 
              -418.9, 
              -608.8]
caliber    = 0.224
bc         = 0.250

# Cartridge Object :
XM193 = Cartridge(name, 
                  mass, 
                  s_traj2,
                  s_x, 
                  caliber,
                  vel[0],
                  bc,
                  units = 'i',
                  velocity = vel, 
                  vel_x = vel_x,
                  long_traj = l_traj, 
                  l_x = l_x)

name   = "0.338 Lapua Mag no. 4 PL 8013 300 grain"
mass   = 300
vel    = [2723,
          2600,
          2482,
          2367,
          2042,
          1842,
          1653]
vel_x  = [0,
          100,
          200,
          300,
          600,
          800,
          1000]
s_x = l_x = vel_x
s_traj = [-1.6,
          0,
          -4,
          -13,
          -80,
          -165,
          -291]
l_traj = [-1.6,
          4,
          5,
          0,
          -54,
          -131,
          -249]
caliber = 0.338
bc      = 0.736

# Cartridge Object :
lapua = Cartridge(name, 
                  mass, 
                  s_traj2,
                  s_x, 
                  caliber,
                  vel[0],
                  bc,
                  units = 'i',
                  velocity = vel, 
                  vel_x = vel_x,
                  long_traj = l_traj, 
                  l_x = l_x)

name   = ".338 Win. Mag. PRC338WA 225 grain bullet"
mass   = 225
vel    = [2780,
          2582,
          2392,
          2210,
          2036,
          1871]
vel_x  = [0,
          100,
          200,
          300,
          400,
          500]
s_traj = [-1.5,
          0.2,
          0.8,
          0.0,
          -2.2,
          -5.9,
          -11.2]
s_x    = [0,
          50,
          100,
          150,
          200,
          250,
          300]
l_traj = [-1.5,
          1.9,
          1.7,
          0.0,
          -3.2,
          -7.9,
          -23.0,
          -46.5]
l_x    = [0,
          100,
          150,
          200,
          250,
          300,
          400,
          500]
caliber = 0.338
bc      = 0.456

# Cartridge Object :
winMag = Cartridge(name, 
                   mass, 
                   s_traj2,
                   s_x, 
                   caliber,
                   vel[0],
                   bc,
                   units = 'i',
                   velocity = vel, 
                   vel_x = vel_x,
                   long_traj = l_traj, 
                   l_x = l_x)



# Ballistics model for round :
ball1 = Ballistics(XM193, 'Predictor', 0.0, 2.2121, 0.001, 0.001, 
                   traj='l', model='g')
ball2 = Ballistics(lapua, 'Predictor', 0.0, 1.5, 0.001, 0.001, 
                   traj='l', model='g')
ball3 = Ballistics(winMag, 'Predictor', 0.0, 1.5, 0.001, 0.001, 
                   traj='l', model='g')

# Set the deisred model :
ball1.set_g(model.G1)
ball2.set_g(model.G1)
ball3.set_g(model.G1)

# Zero the rifle :
ball1.hit_target(yards_to_m(200))
ball2.hit_target(yards_to_m(300))
ball3.hit_target(yards_to_m(200))

# Plot the results :
ball1.plot()
ball2.plot()
ball3.plot()


