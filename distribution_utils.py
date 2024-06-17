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
