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
        data_line = {}
        for i in range(nlines):
            #y = get_random(ymin[i],ymax[i],ndims=1,npoints=npoints)
            y, data = get_linear(xs[i],ndims=1,npoints=npoints,
                          a1=dist_params['intersect'],
                          m1=dist_params['slope'],
                          noise1=dist_params['noise'])
            ##y = data['y']
            ys.append(y)
            data_line['line'+str(i)] = data.copy()
        return xs,ys, data_line
    elif plot_type == 'scatter':
        # x/y
        xs = get_random(xmin,xmax,ndims=1,npoints=npoints) # this will be random still
        ys, data_points = get_linear(xs,ndims=1,npoints=npoints,
                      a1=dist_params['intersect'],
                      m1=dist_params['slope'],
                      noise1=dist_params['noise'])    
        # colors linear?
        if np.random.uniform(0,1) <= dist_params['color noise prob']:
            colors, data_color = get_linear(xs,ys,ndims=2, 
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
            data_color = 'random'

        #ys = get_random(ymin,ymax,ndims=1,npoints=npoints)
        #colors = get_random(cmin,cmax,ndims=1,npoints=npoints)
        # is color linear?
        data = {'points':data_points, 'colors':data_color}
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



########################################################################
############################# GMM (in progress!) ############################
#######################################################################

from sklearn.datasets import make_blobs
from scipy.stats import binned_statistic_2d

def get_gmm(xmin,xmax,ymin=0,ymax=1,zmin=0,zmax=1,
            cmin=0,cmax=1, ndims=1, 
            nclusters = {'min':1,'max':10}, 
            cluster_std = {'min':0.01, 'max':1.0},
            nsamples = {'min':10,'max':1000},
            noise = {'min':0, 'max':1.0},
            grid=False,
           function=np.random.uniform, 
           small_data_params = True, 
           down_sample_max=None, fit_to_bounds = True):

    """
    small_data_params : won't save X array and y_true for contour plots (big stuffs)
    """

    if type(nsamples) == type({}): # will pull randomly
        nsamples1 = np.random.randint(nsamples['min'],nsamples['max'])
    elif type(nsamples) == type([]) or type(nsamples) == type(()):
        nsamples1 = nsamples[0]
    else:
        nsamples1 = nsamples # if fixed
    # number of clusters
    nclusters1 = np.random.randint(nclusters['min'],nclusters['max'])
    if ndims > 1:
        cluster_std1 = np.random.uniform(cluster_std['min'],cluster_std['max'], (nclusters1,ndims))
        # power
        cluster_std1 = np.power(10,cluster_std1)
    else:
        cluster_std1 = np.random.uniform(cluster_std['min'],cluster_std['max'], nclusters1)
        cluster_std1 = np.power(10,cluster_std1)
        cluster_std1 *= (xmax-xmin)
        
    data_params = {'nsamples':nsamples1, 'nclusters':nclusters1}#,
                  #'cluster_std':cluster_std1}

    # n_features = n_dim
    # centers : int or array-like of shape (n_centers, n_features), default=None
    #    The number of centers to generate, or the fixed center locations.
    # center_box : tuple of float (min, max), default=(-10.0, 10.0)
    if ndims == 1: # along a line 
        centers_x = np.random.uniform(xmin,xmax,nclusters1).reshape(-1, 1)
        X, y_true,centers_ret = make_blobs(n_samples=nsamples1, n_features=1,
                               cluster_std=cluster_std1, centers=centers_x,
                              center_box=(xmin,xmax),
                                      return_centers=True)
        # labeling starts at 0
        y_true += 1
        
        noise_level = function(noise['min'],noise['max'])
        noise1 = np.random.normal(0,1,nsamples1)*noise_level
                                    
        # multiply
        Xout = X.flatten()*(1+noise1.flatten())
        # drop outside
        if fit_to_bounds:
            mask = (Xout > xmax) | (Xout < xmin)
            y_true_out = y_true.copy()[~mask]
            Xout = Xout[~mask]

        if not small_data_params:
            data_params['X'] = X
            data_params['Xout'] = Xout
            data_params['labels'] = y_true
        data_params['centers'] = centers_x
        data_params['cluster_std'] = cluster_std1
        data_params['noise level'] = noise_level
        
        return Xout, data_params 
    elif ndims > 1: # multi-d
        if ndims > 1:
            mi = np.min([xmin,ymin])
            ma = np.max([xmax,ymax])
        if ndims > 2:
            mi = np.min([mi,zmin])
            ma = np.max([ma,zmax])
        if ndims > 3:
            print('ndims > 3 not supported!')
            import sys; sys.exit()

        centers_x = np.random.uniform(xmin,xmax,nclusters1)
        centers_y = np.random.uniform(ymin,ymax,nclusters1)
        centers = np.zeros((nclusters1,ndims))
        centers[:,0] = centers_x
        centers[:,1] = centers_y
        if ndims > 2:
            centers_z = np.random.uniform(zmin,zmax,nclusters1)
            centers[:,2] = centers_z
        X, y_true,centers_ret = make_blobs(n_samples=nsamples1, n_features=ndims,
                               cluster_std=cluster_std1*(ma-mi), centers=centers,
                              center_box=(mi,ma),
                                      return_centers=True)
        
        noise_level = function(noise['min'],noise['max'])
        noise1 = np.random.normal(0,1,(nsamples1,ndims))*noise_level
        # starts at 0
        y_true += 1
                                    
        # multiply
        Xout = X*(1+noise1)
        # drop outside
        mask = (Xout[:,0] > xmax) | (Xout[:,0] < xmin) | (Xout[:,1] > ymax) | (Xout[:,1] < ymin)
        Xout = Xout[~mask]
        y_true_out = y_true.copy()[~mask]
        mask = (X[:,0] > xmax) | (X[:,0] < xmin) | (X[:,1] > ymax) | (X[:,1] < ymin)
        X = X[~mask]
        y_true = y_true[~mask]

        if not small_data_params:
            data_params['X'] = X
            data_params['labels'] = y_true
        data_params['centers'] = centers
        data_params['cluster_std'] = cluster_std1
        data_params['noise level'] = noise_level

        if not grid:
            # colors
            if nclusters1 > 1 and np.max(y_true_out) != np.min(y_true_out):
                colors = (y_true_out-np.min(y_true_out))/(np.max(y_true_out)-np.min(y_true_out))*(cmax-cmin)+cmin
            else:
                colors = (y_true_out)*(cmax-cmin)+cmin # ytrue = 1 now
            # noise here as well
            noise2 = np.random.normal(0,1,len(y_true_out))*noise_level
            colors = colors*(1+noise2)

            # downsample if needed
            if down_sample_max is not None:
                if len(colors) > down_sample_max:
                    ints = np.random.choice(np.arange(0,len(colors)),
                                            size=down_sample_max,
                                            replace=False)
                    Xout = Xout[ints,:]
                    colors = colors[ints]
            return Xout, colors, data_params
        else: # we have more work to do (contours)
            # just the shape
            y_true[:] = 1
            nbinsx,nbinsy = nsamples[1],nsamples[2]
            
            binx = np.linspace(xmin,xmax, nbinsx)
            biny = np.linspace(ymin,ymax, nbinsy)
                
            ret = binned_statistic_2d(X[:,1], X[:,0], y_true, 
                                    'sum', bins=[biny,binx], 
                expand_binnumbers=True)
            
            colors = ret.statistic
            # renorm
            if np.max(colors) != np.min(colors):
                div1 = np.max(colors)-np.min(colors)
            else:
                div1 = 1
            colors = (colors-np.min(colors))/div1*(cmax-cmin)+cmin
            # noise here as well
            noise2 = np.random.normal(0,1,colors.shape)*noise_level
            colors = colors*(1+noise2)
            
            #Xout[0,:] = 
            xs = (binx[:-1] + binx[1:]) / 2
            #Xout[1,:] = 
            ys = (biny[:-1] + biny[1:]) / 2

            return xs,ys, colors, data_params


def get_gmm_data(plot_type, dist_params,
                 xmin,xmax,ymin=0,ymax=1,zmin=0,zmax=0,
                    prob_same_x=0.5, nlines=1, npoints=1,
                   cmin=0, cmax=1, 
                   function=np.random.uniform, small_data_params = True):
    """
    npoints : can be tuple if multi dimension
    """
        
    if plot_type == 'line':
        p = np.random.uniform(0,1)
        xs = []
        isSameX = False
        if p <= prob_same_x: # same x for all y
            x = function(low=xmin, high=xmax, size=npoints) # x-values
            x = np.sort(x)
            # repeat for all
            for i in range(nlines):
                xs.append(x)
            isSameX = True
        else: # different
            for i in range(nlines):
                x = function(low=xmin, high=xmax, size=npoints) # x-values
                x = np.sort(x)
                xs.append(x)

        # histograms actually but as line plot?
        isHisto = False
        if np.random.uniform(0,1) <= dist_params['histogram as line']['prob']:
            isHisto = True
        ys = []
        data_params = {}
        for i in range(nlines):
            if not isHisto:
                y, data_params1 = get_gmm(ymin[i],ymax[i],
                                         ndims=1,
                              nclusters=dist_params['nclusters'],
                              nsamples=len(xs[i]), # keep same # of x values
                              cluster_std=dist_params['cluster std'],
                                        noise=dist_params['noise'],
                                        function=function,
                                         small_data_params = small_data_params,
                                         fit_to_bounds = not isSameX)
                if not isSameX and len(y) != len(xs[i]):
                    inds = np.random.choice(np.arange(0,len(xs[i])),len(y),replace=False)
                    inds = np.sort(inds)
                    xs[i] = xs[i][inds]
            else:
                ypoints, data_params1 = get_gmm(np.min(xs[i]),np.max(xs[i]),
                                             ndims=1,
                                  nclusters=dist_params['nclusters'],
                                  nsamples=len(xs[i])*dist_params['histogram as line']['factor'],
                                  cluster_std=dist_params['cluster std'],
                                            noise=dist_params['noise'],
                                            function=function,
                                         small_data_params = small_data_params)
                # repeat from centers to edges
                y,bin_edges = np.histogram(ypoints, bins=xs[i]) 
                xs[i] = (bin_edges[:-1] + bin_edges[1:]) / 2 # update bins
                # rescale
                y = y.astype('float')
                y = (y-np.min(y))/(np.max(y)-np.min(y))*(float(ymax[i])-float(ymin[i]))+ymin[i]

            ys.append(y)
            data_params['line'+str(i)] = data_params1.copy()
        return xs,ys, data_params
    elif plot_type == 'scatter':
        # x/y
        npoints = np.random.uniform(dist_params['upsample factor log']['min'], 
                                    dist_params['upsample factor log']['max'])
        npoints = int(np.max(npoints+1)*round(np.power(10,npoints)))

        X, colors_dist, data_params = get_gmm(xmin,xmax,ymin=ymin,ymax=ymax,
                                     ndims=2,
                          nclusters=dist_params['nclusters'],
                          nsamples=npoints,#dist_params['nsamples'], # keep same # of x values
                          cluster_std=dist_params['cluster std'],
                                    noise=dist_params['noise'],
                                    function=function,
                                                 cmin=cmin,
                                                 cmax=cmax,
                                             down_sample_max=dist_params['max points'],
                                         small_data_params = small_data_params)  
        xs = X[:,0]
        ys = X[:,1]
        # colors linear?
        if np.random.uniform(0,1) <= dist_params['color noise prob']: 
            colors = colors_dist
        else:
            colors = get_random(cmin,cmax,ndims=1,npoints=len(colors_dist))

        return xs,ys,colors, data_params
    elif plot_type == 'histogram': # I feel like this doesn't make too 
                                   # much sense for histograms, but lets just do it
        y, data_params = get_gmm(xmin,xmax,
                                     ndims=1,
                          nclusters=dist_params['nclusters'],
                          nsamples=dist_params['nsamples'], # keep same # of x values
                          cluster_std=dist_params['cluster std'],
                                    noise=dist_params['noise'],
                                    function=function,
                                         small_data_params = small_data_params)

        return y, data_params
    elif plot_type == 'contour':
        # upsample the number of points per grid
        nx = npoints[0] # silly reformatting stuffs
        ny = npoints[1]
        npoints = np.random.uniform(dist_params['upsample factor log']['min'], 
                                    dist_params['upsample factor log']['max'])
        npoints = int(np.max(npoints+1)*round(np.power(10,npoints)))

        xs,ys, colors, data_params = get_gmm(xmin,xmax,ymin=ymin,ymax=ymax,
                                     ndims=2,
                          nclusters=dist_params['nclusters'],
                          nsamples=(npoints,nx,ny), # keep same # of x values
                          cluster_std=dist_params['cluster std'],
                                    noise=dist_params['noise'],
                                    function=function,
                                                 cmin=cmin,
                                                 cmax=cmax, 
                                        grid=True,
                                         small_data_params = small_data_params)  
        
        return xs,ys,colors,data_params


