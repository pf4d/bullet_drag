class IntegratorBase(object):
 
    runner = None            # runner is None => integrator is not available
    success = None           # success==1 if integrator was called successfully
    supports_run_relax = None
    supports_step = None
    integrator_classes = []
    scalar = float
 
    def reset(self,n,has_jac):
        """Prepare integrator for call: allocate memory, set flags, etc.
        n - number of equations.
        has_jac - if user has supplied function for evaluating Jacobian.
        """
 
    def run(self,f,jac,y0,t0,t1,f_params,jac_params):
        """Integrate from t=t0 to t=t1 using y0 as an initial condition.
        Return 2-tuple (y1,t1) where y1 is the result and t=t1
        defines the stoppage coordinate of the result.
        """
        raise NotImplementedError,\
        'all integrators must define run(f,jac,t0,t1,y0,f_params,jac_params)'
 
    def step(self,f,jac,y0,t0,t1,f_params,jac_params):
        """Make one integration step and return (y1,t1)."""
        raise NotImplementedError,'%s does not support step() method' %\
              (self.__class__.__name__)
 
    def run_relax(self,f,jac,y0,t0,t1,f_params,jac_params):
        """Integrate from t=t0 to t>=t1 and return (y1,t)."""
        raise NotImplementedError,'%s does not support run_relax() method' %\
              (self.__class__.__name__)
