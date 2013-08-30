from scipy.integrate.ode import IntegratorBase
from numpy import *
from pylab import *
 
class Predictor(IntegratorBase):
    runner = True
 
    def __init__(self,dt=.01):
        self.dt = dt
 
    def reset(self,n,has_jac):
        pass
 
    def run(self,f,jac,y0,t0,t1,f_params,jac_params):
         # this method is called to integrate from t=t0 to t=t1
         # with initial condition y0. f and jac are user-supplied functions
         # that define the problem. f_params,jac_params are additional
         # arguments to these functions.
 
        yo = array(y0) # Initial condition
 
        # Because the assumption is that method returns the values at a
        # particular time, we have to do some rejiggering of the time step.
        times = linspace(t0,t1,num=ceil((t1-t0)/self.dt)+1,endpoint=True)
        dt = times[1]-times[0]
        # Spin-up using RK4
        t = t0
        k1 = f(t,yo,*f_params) * dt
        k2 = f(t + dt,yo + k1/2,*f_params) * dt
        k3 = f(t + dt,yo + k2/2,*f_params) * dt
        k4 = f(t + dt,yo + k3,*f_params) * dt
        yn = yo + 1./6*(k1 + 2*k2 + 2*k3 + k4)
        ynm1 = yo
        
        # Predictor Method:
        for t in times[2:]:
            dyn = f(t,yn,*f_params)              # [vn,an]  
            yp = ynm1 +2*dyn*dt                  # [xp,vp]
            ap = f(t,yp,*f_params)[1]            # ap  
            vnp1 = dyn[0] + .5*(ap + dyn[1])*dt  # v_n+1
            xnp1 = yn[0] + .5*(vnp1 + yn[1])*dt  # x_n+1
            ynm1 = yn                            # new [x_n-1,v_n-1] value
            yn = array([xnp1, vnp1])             # new [xn,vn] value
        if isfinite(yn[-1]): self.success = True # Check for success
        return yn,t
    
 
if Predictor.runner:
    IntegratorBase.integrator_classes.append(Predictor)
