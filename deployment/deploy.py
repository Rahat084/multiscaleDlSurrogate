import numpy as np

def local_project(v, V, u=None):
    """ 
    projects v on V with custom quadrature scheme dedicated to
    FunctionSpaces V of `Quadrature` type
        
    if u is provided, result is appended to u
    """
    dv = TrialFunction(V)
    v_ = TestFunction(V)
    a_proj = inner(dv, v_)*dxm
    b_proj = inner(v, v_)*dxm
    solver = LocalSolver(a_proj, b_proj)
    solver.factorize()
    if u is None:
        u = Function(V)
        solver.solve_local_rhs(u)
        return u
    else:
        solver.solve_local_rhs(u)
        return

def ANN2Phase(eps, modes_old):
    '''
    deploy surrogate ann with 2 defect phases
    '''
    zero = np.zeros((eps.shape[0], 1))
    output = np.zeros((eps.shape[0], 12))
    # Deformation Mode Prediction 
    modes = cls_model(eps[:, [0, 1, 3 ]]).numpy().argmax(axis=1)
    df_mask = (modes == 2) & (modes_old == 2)
    #disl_mask = (modes == 0) | (modes_old == 0)
    disl_mask = ~(df_mask)
    # Defect Free Stress Prediction
    output[df_mask] =df_model(eps[:, [0, 1, 3 ]][df_mask])
    # Dislocation Mode Prediction
    if disl_mask.any():
        output[disl_mask] =dl_model(eps[:, [0, 1, 3 ]][disl_mask])
    # Separate Stress and Tangent Operator
    sigma = np.hstack([output[:, 0:2], zero, output[:,2:3]])
    sigma_vm = output[:,0]**2 + output[:,1]**2 - output[:,0]*output[:,1]  + 3*output[:,2]**2 
    Ctan = np.hstack([output[:,3:5], zero, output[:,5:8], zero, output[:,8:9], \
                     zero, zero, zero, zero, \
                     output[:, 9:11], zero, output[:, 11:]])    
    return modes, sigma, sigma_vm, Ctan

def ANN3Phase(eps, modes_old):
    '''
    deploy surrogate ANN with 3 defect phases
    '''
    zero = np.zeros((eps.shape[0], 1))
    output = np.zeros((eps.shape[0], 12))
    #void_out = np.hstack([np.zeros((1, 3)), np.ones((1, 9))])
    void_out = np.hstack([np.zeros((1, 3)), np.random.randn(1, 9)])
    # Deformation Mode Prediction 
    modes = cls_model(eps[:, [0, 1, 3 ]]).numpy().argmax(axis=1)
    df_mask = (modes == 2) & (modes_old == 2)
    void_mask = (modes == 0) | (modes_old == 0)
    disl_mask = ~(df_mask | void_mask)
    # Defect Free Stress Prediction
    output[df_mask] =df_model(eps[:, [0, 1, 3 ]][df_mask])
    # Dislocation Mode Prediction
    if disl_mask.any():
        output[disl_mask] =dl_model(eps[:, [0, 1, 3 ]][disl_mask])
    # Void Mode Prediction
    if void_mask.any():
        output[void_mask] = void_out
    # Separate Stress and Tangent Operator
    sigma = np.hstack([output[:, 0:2], zero, output[:,2:3]])
    sigma_vm = output[:,0]**2 + output[:,1]**2 - output[:,0]*output[:,1]  + 3*output[:,2]**2 
    Ctan = np.hstack([output[:,3:5], zero, output[:,5:8], zero, output[:,8:9], \
                     zero, zero, zero, zero, \
                     output[:, 9:11], zero, output[:, 11:]])    
    return modes, sigma, sigma_vm, Ctan


