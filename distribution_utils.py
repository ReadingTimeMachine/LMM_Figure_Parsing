import numpy as np

######### "RAW" DISTRIBUTIONS ##########

def get_random(xmin,xmax,ymin=0,ymax=0, zmin=0,zmax=1,hmin=0,hmax=1,
               ndims=1,
               npoints=10,grid=False,
              function=np.random.uniform):
    """
    Generic random distribution
    ndims : 1-3, how many dimensions for the data
    xmin/xmax : ranges for dimension 1
    ymin/ymax : ranges for dimension 2
    zmin/zmax : ranges for dimension 3
    hmin/hmax : ranges for dimension 3, grid=True (3d "heatmap")
    npoints : number of random points (can be a tuple for different values)
    function : how to generate the random numbers
    grid : if ndim>1 and grid is set to True instead of individual points, 
           you will get a data on a uniform grid
    """
    if ndims == 1:
        #print(xmin)
        #print(xmax)
        #print(npoints)
        return function(low=xmin, high=xmax, size=npoints)
    elif ndims == 2:
        if not grid:
            return function(low=np.array([xmin,ymin]),
                            high=np.array([xmax,ymax]), size=[npoints,2])
        else:
            x = np.linspace(xmin,xmax,npoints[0])
            y = np.linspace(ymin,ymax,npoints[1])
            #grid = function(low=zmin,high=zmax,size=(npoints,npoints))
            grid = function(low=zmin,high=zmax,size=npoints) # npoints is a tuple (nx,ny)
            return {'x':x, 'y':y, 'z':grid.T} # .T for right shape
    elif ndims == 3:
        if not grid:
            return function(low=np.array([xmin,ymin,zmin]),
                            high=np.array([xmax,ymax,zmax]), size=[npoints,3])
        else:
            x = np.linspace(xmin,xmax,npoints[0])
            y = np.linspace(ymin,ymax,npoints[1])
            z = np.linspace(zmin,zmax,npoints[2])
            #grid = function(low=hmin,high=hmax,size=(npoints,npoints,npoints))
            grid = function(low=hmin,high=hmax,size=npoints) # tuple (nx,ny,nz)
            return {'x':x, 'y':y, 'z':z, 'h':grid.T} # .T for right shape

    else:
        print('ndims=', ndims, 'not supported for "get_random" function!')
        import sys; sys.exit()
        


##### SPECIFIC DISTRIBUTIONS #######
def get_random_data(plot_type,xmin,xmax,ymin=0,ymax=1,zmin=0,zmax=0,
                    prob_same_x=0.5, nlines=1, npoints=1,
                   cmin=0, cmax=1):
    """
    npoints : can be tuple if multi dimension
    """
    # do we have all the same x for all points?
    if plot_type == 'line':
        p = np.random.uniform(0,1)
        xs = []
        if p <= prob_same_x: # same x for all y
            x = get_random(xmin,xmax,ndims=1,npoints=npoints)
            x = np.sort(x)
            # repeat for all
            for i in range(nlines):
                xs.append(x)
        else: # different
            for i in range(nlines):
                x = get_random(xmin,xmax,ndims=1,npoints=npoints)
                x = np.sort(x)
                xs.append(x)
            
        ys = []
        for i in range(nlines):
            y = get_random(ymin[i],ymax[i],ndims=1,npoints=npoints)
            ys.append(y)
        return xs,ys
    elif plot_type == 'scatter':
        xs = get_random(xmin,xmax,ndims=1,npoints=npoints)
        ys = get_random(ymin,ymax,ndims=1,npoints=npoints)
        colors = get_random(cmin,cmax,ndims=1,npoints=npoints)
        return xs,ys,colors
    elif plot_type == 'histogram':
        x = get_random(xmin,xmax,ndims=1,npoints=npoints)
        return x
    elif plot_type == 'contour':
        data = get_random(xmin,xmax,ymin=ymin,ymax=ymax, ndims=2, grid=True, 
                         npoints=npoints, zmin=zmin,zmax=zmax) # {'x':x, 'y':y, 'z':grid}
        xs = data['x']; ys = data['y']
        colors = data['z']
        return xs,ys,colors


########################################################################
############################# LINEAR ############################
#######################################################################


def get_linear(x,y=[],z=[],h=[],
               ndims=1,
                    a1=(-1,1), a2=(-1,1), a3=(-1,1), a4=(-1,1), # mx + a
                    m1=(-1,1), m2=(-1,1), m3=(-1,1), m4=(-1,1), # mx + a
                    noise1=(0,1), noise2=None,noise3=None, noise4=None,
               npoints=10,grid=False,
              function=np.random.uniform):
    """
    a1-a4 : the "a's" in mx + a, will be randomly selected from range
    m1-m4 : the "m's" in mx + a, will be randomly selected from range
    noise1-noise4 : noise as a % of calculated "y", will be randomly selected from range
    """
    if ndims == 1:
        a = function(a1[0],a1[1])
        m = function(m1[0],m1[1])
        y = m*x + a
        # now add noise --> I think maybe multiply?
        noise_level = function(noise1[0],noise1[1])
        noise = np.random.normal(0,1,npoints)*noise_level
        y = y*(1+noise)
        data = {'m':m, 'a':a, 'noise level':noise_level}
        return y, data
    if ndims == 2:
        if not grid:
            a11 = function(a1[0],a1[1])
            m11 = function(m1[0],m1[1])
            a22 = function(a2[0],a2[1])
            m22 = function(m2[0],m2[1])
            #noise_level1 = function(noise1[0],noise1[1])
#            if len(x.shape)>1 and len(y.shape)>1: # have 2d x/y
            noise_level1 = function(noise1[0],noise1[1])
            #print('noise level shape', noise_level1)
#            elif len(x) == len(y):
#                noise_level1 = 
                
            noise1 = np.random.normal(0,1,npoints[0])*noise_level1
            #print('noise1 shape', noise1.shape)
            if noise2 is not None: # different noise in different directions
                noise_level2 = function(noise2[0],noise2[1])
                noise2 = np.random.normal(0,1,npoints[1])*noise_level2
                z = (m11*x + a11)*(1+noise1) + (m22*y + a22)*(1+noise2)
            else:
                if len(x) == len(y):
                    noise1 = np.random.normal(0,1,npoints[0])*noise_level1
                else:
                    noise1 = np.random.normal(0,1,npoints)*noise_level1
                    
                #print('noise1 shape here', noise1.shape)
                z = (m11*x + a11 + m22*y + a22)*(1+noise1)

            #print('z shape', z.shape)
                
            data = {'m1':m11, 'a1':a11, 
                    'm2':m22, 'a2':a22, 
                   'noise level 1':noise_level1}
            if noise2 is not None: 
                data['noise level 2'] = noise_level2
            return z, data
        else:
            a11 = function(a1[0],a1[1])
            m11 = function(m1[0],m1[1])
            a22 = function(a2[0],a2[1])
            m22 = function(m2[0],m2[1])
            noise_level1 = function(noise1[0],noise1[1],len(x))
            grid = np.zeros([len(x),len(y)])
            # repeat x/y
            xr = np.repeat(x[:,np.newaxis], len(y), axis=1).T
            yr = np.repeat(y[:,np.newaxis], len(x), axis=1)
            if noise2 is not None:
                noise_level2 = function(noise2[0],noise2[1],len(y))
                nxr = np.repeat(noise_level1[:,np.newaxis], len(y), axis=1).T
                nyr = np.repeat(noise_level2[:,np.newaxis], len(x), axis=1)
                grid = (m11*xr + a11)*(1+nxr) + (m22*yr + a22)*(1+nyr)
            else:
                noise_level1 = function(noise1[0],noise1[1],npoints)
                #print('shape1:', noise_level1.shape)
                noise1 = np.random.normal(0,1,npoints)*noise_level1
                grid = (m11*xr + a11 + m22*yr + a22)*(1+noise1.T)
                
            data = {'m1':m11, 'a1':a11, 
                    'm2':m22, 'a2':a22, 
                   'noise level 1':noise_level1}
            if noise2 is not None:
                   data['noise level 2'] = noise_level2
            zout = {'x':x, 'y':y, 'z':grid}
            return zout, data



def get_linear_data(plot_type, dist_params, 
                    xmin,xmax,ymin=0,ymax=1,zmin=0,zmax=0,
                    prob_same_x=0.5, nlines=1, npoints=1,
                   cmin=0, cmax=1, 
                   function=np.random.uniform):

    """
    npoints : can be tuple if multi dimension
    """
    #print('in get_linear_data:', dist_params)
    # do we have all the same x for all points?
    if plot_type == 'line':
        p = np.random.uniform(0,1)
        xs = []
        if p <= prob_same_x: # same x for all y
            x = function(low=xmin, high=xmax, size=npoints) # x-values
            x = np.sort(x)
            # repeat for all
            for i in range(nlines):
                xs.append(x)
        else: # different
            for i in range(nlines):
                x = function(low=xmin, high=xmax, size=npoints) # x-values
                x = np.sort(x)
                xs.append(x)
            
        ys = []
        for i in range(nlines):
            #y = get_random(ymin[i],ymax[i],ndims=1,npoints=npoints)
            y, data = get_linear(xs[i],ndims=1,npoints=npoints,
                          a1=dist_params['intersect'],
                          m1=dist_params['slope'],
                          noise1=dist_params['noise'])
            ##y = data['y']
            ys.append(y)
        return xs,ys, data
    elif plot_type == 'scatter':
        # x/y
        xs = get_random(xmin,xmax,ndims=1,npoints=npoints) # this will be random still
        ys, data = get_linear(xs,ndims=1,npoints=npoints,
                      a1=dist_params['intersect'],
                      m1=dist_params['slope'],
                      noise1=dist_params['noise'])    
        # colors linear?
        if np.random.uniform(0,1) <= dist_params['color noise prob']:
            colors, data = get_linear(xs,ys,ndims=2, 
                               npoints=(npoints,npoints),
                      a1=dist_params['intersect'],
                      m1=dist_params['slope'],
                      noise1=dist_params['noise'])#,  
                      # a2=dist_params['intersect'],
                      # m2=dist_params['slope'],
                      # noise2=dist_params['noise'])  
            # colors is now 2D at each combo of x/y
            
        else:
            colors = get_random(cmin,cmax,ndims=1,npoints=npoints)

        #ys = get_random(ymin,ymax,ndims=1,npoints=npoints)
        #colors = get_random(cmin,cmax,ndims=1,npoints=npoints)
        # is color linear?
        return xs,ys,colors, data
    elif plot_type == 'histogram': # I feel like this doesn't make too 
                                   # much sense for histograms, but lets just do it
        x = get_random(xmin,xmax,ndims=1,npoints=npoints) 
        y, data = get_linear(x,ndims=1,npoints=npoints,
                      a1=dist_params['intersect'],
                      m1=dist_params['slope'],
                      noise1=dist_params['noise'])
        return y, data
    elif plot_type == 'contour':
        xs = get_random(xmin,xmax,ndims=1,npoints=npoints[0]) # this will be random still
        xs = np.sort(xs)
        ys = get_random(xmin,xmax,ndims=1,npoints=npoints[1]) # this will be random still
        ys = np.sort(ys)
        data, data_params = get_linear(xs,ys,ndims=2, 
                               npoints=npoints,
                      a1=dist_params['intersect'],
                      m1=dist_params['slope'],
                      noise1=dist_params['noise'],  
                      # a2=dist_params['intersect'],
                      # m2=dist_params['slope'],
                      # noise2=dist_params['noise'],
                                      grid=True)

        xs = data['x']; ys = data['y']
        colors = data['z']
        return xs,ys,colors,data_params
        