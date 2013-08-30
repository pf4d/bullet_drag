from scipy.integrate.ode import IntegratorBase
from numpy import array,arange,isfinite,ceil
from pylab import linspace
 
class EulerRichardson(IntegratorBase):
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
        # Integration loop
        for t in times[1:]:
            ymid = yo + f(t,yo,*f_params) * dt/2
            yn = yo + f(t+dt/2,ymid,*f_params) * dt
            yo = yn
 
        if isfinite(yn[-1]): self.success = True # Check for success
        return yn,t
 
if EulerRichardson.runner:
    IntegratorBase.integrator_classes.append(EulerRichardson)


