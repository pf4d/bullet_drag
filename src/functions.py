from numpy import *
from functions import *

def g_param(G, v):
    '''
    PURPOSE:
      Interpolate between model data points.
    INPUTS:
      G - {G1, G2, G5, G6, G7, G9} - ballistics model to use.
      v - float - current velocity of the bullet.
    OUTPUTS:
      A - 
      M - 
    '''
    Gvel = G[:,0]        # Velocity from G model
    vh = where(Gvel>=v)  # Indicies with greater velocity than v
    vl = where(Gvel<=v)  # Indicies with lower velocity than v
    ih = vh[0][-1]       # first index of velocity in G above v
    il = vl[0][0]        # first index of velocity in G below v
    
    #if v corresponds to velocity in G, use values in table
    if  ih == il:
        A = G[ih,1]
        M = G[ih,2]
    
    #if v is intermediate value, linearly interploate between G values
    else:
        vl = G[il,0]
        vh = G[ih,0]
        ah = G[ih,1]
        al = G[il,1]
        mh = G[ih,2]
        ml = G[il,2]
        
        # y = mx + b where 
        # m = (ah-al) / (vh-vl)
        # x = v-vl and
        # b = al.
        A = (v-vl) * (ah-al) / (vh-vl) + al
        M = (v-vl) * (mh-ml) / (vh-vl) + ml
    
    return A, M


def vel_comp(v, theta):
    '''
    PURPOSE:
      Compute the x- and y-components of a velocity vector.
    INPUTS:
      v     - float - Current bullet velocity.
      theta - float - Angle of bullet with respect to +x axis.
    OUTPUT:
      vx    - float - x-component velocity.
      vy    - float - y-component velocity.
    '''
    vx = v*cos(theta)
    vy = v*sin(theta)
    return vx, vy


def fbar_gmodel(t, x, g, bc, G):
    """
    PURPOSE:
      Apply the model's predicted drag force on the bullet's
      acceleration.
    INPUTS:
      t time, only used in non-autonomous systems.
      x[0]  - float - the x-position
      x[1]  - float - the x-component velocity
      x[2]  - float - the y-position
      x[3]  - float - the y-component velocity
      g     - gravitational acceleration
      bc    - float - Ballistics coefficient.
      G     - {G1, G2, G5, G6, G7, G9} - ballistics model to use.
    OUTPUTS:
      An array [vx, ax, vy, ay] where:
        vx - x-component velocity
        ax - x-component acceleration
        vy - y-component velocity
        ay - y-component acceleration
    """
    vx = m_to_ft(x[1])
    vy = m_to_ft(x[3])
    v = sqrt(vx**2 + vy**2)
    A, M = g_param(G, v)
    
    ax = -vx*(A/bc)*v**(M-1)
    ay = -g - vy*(A/bc)*v**(M-1)
    
    return array( [vx, ax, vy, ay] )


def get_cd(v):
    """
    PURPOSE:
      Give a drag coefficient for a velocity v.
    INPUT:
      v - velocity in ft/sec
    OUTPUT:
      cd - drag coefficient
      16*sqrt(v)/v
      2.6/log(v)
    """
    if v > 1000:
      return 16*sqrt(v)/v
    else:
      return 0.15


def fbar_emodel(t, x, g, m, rho, A):
    """
    PURPOSE:
      Model the path of a bullet using mathematical functions.
    INPUTS:
      t     - time, only used in non-autonomous systems.
      x[0]  - float - the x-position            (ft)
      x[1]  - float - the x-component velocity  (ft/s)
      x[2]  - float - the y-position            (ft)
      x[3]  - float - the y-component velocity  (ft/s)
      g     - gravitational acceleration        (ft/s^2)
      m     - mass of the bullet                (lbs)
      rho   - density of fluid (air)            (lbs/ft^3)
      A     - sectional area of bullet in       (ft^2)
    OUTPUTS:
      An array [vx, ax, vy, ay] where:
        vx - x-component velocity               (ft/s)
        ax - x-component acceleration           (ft/s^2)
        vy - y-component velocity               (ft/s)
        ay - y-component acceleration           (ft/s^2)
    NOTES:
      D = (1/2) rho v^2 Cd A
      D(y) - Fg = ma_y
      (1/2) rho vy^2 Cd A - mg = ma_y
    """
    vx = x[1]
    vy = x[3]
    v = sqrt(vx**2 + vy**2)
    cd = get_cd(v)
    
    ax = -((1/2.)*rho*vx**2*cd*A)/m
    ay = -g - ((1/2.)*rho*vy**2*cd*A)/m
    
    return array( [vx, ax, vy, ay] )


def array_list_convert(f, l):
    l = array(l)
    l = f(l)
    l = list(l)
    return l

def grains_to_g(grains):
    return grains * 0.06479891

def grains_to_lbs(grains):
    return grains / 7000.0

def sqin_to_sqm(sqin):
    return sqin * 0.00064516

def lbs_to_kg(lbs):
    return lbs / 2.20462262

def lbs_to_g(lbs):
    return lbs * 453.59237

def ft_to_yards(ft):
    return ft / 3.0

def ft_to_inches(ft):
    return ft * 12.0

def ft_to_m(ft):
    return ft * 0.3048

def inches_to_ft(inches):
    return inches / 12.0

def inches_to_m(inches):
    return inches * 0.0254

def yards_to_ft(yards):
    return yards * 3.0

def yards_to_m(yards):
    return yards * 0.9144

def cm_to_m(cm):
    return cm / 100.0

def m_to_ft(m):
    return m * 3.2808399

def m_to_yards(m):
    return m * 1.0936133

def mm_to_inches(mm):
    return mm * 0.0393700787

def m3_to_ft3(m):
    return m * 3.2808399 * 3.2808399 * 3.2808399

def kg_to_lbs(kg):
    return kg * 2.20462262

def degrees_to_rad(deg):
    return deg * pi / 180.0

def convert_bc(bc):
    return bc * lbs_to_g(1) / sqin_to_sqm(1)

