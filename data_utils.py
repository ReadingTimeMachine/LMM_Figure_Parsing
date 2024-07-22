import numpy as np
import json

from importlib import reload

import distribution_utils
reload(distribution_utils)
from distribution_utils import get_random_data, get_random, \
   get_linear, get_linear_data#, get_data


# for saving numpy arrays
# https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return 'non serializable entry'
        return json.JSONEncoder.default(self, obj)

##########################################
############## CONTOUR DATA ###############
##########################################

def get_contour_data(plot_params, distribution = 'random',
                     verbose=True):
    """
    plot_params : directory with plot params
    """
    data_params = {}
    nx = int(round(np.random.uniform(low=plot_params['npoints']['nx']['min'], 
                                          high=plot_params['npoints']['nx']['max'])))
    ny = int(round(np.random.uniform(low=plot_params['npoints']['ny']['min'], 
                                          high=plot_params['npoints']['ny']['max'])))
    
    xmin,xmax = plot_params['xmin'],plot_params['xmax']
    ymin,ymax = plot_params['ymin'],plot_params['ymax']

    x1 = np.random.uniform(low=xmin, high=xmax)
    x2 = np.random.uniform(low=xmin, high=xmax)
    if x1<x2:
        xmin = x1; xmax = x2
    else:
        xmin=x2; xmax=x1
    y1 = np.random.uniform(low=ymin, high=ymax)
    y2 = np.random.uniform(low=ymin, high=ymax)
    if y1<y2:
        ymin = y1; ymax = y2
    else:
        ymin=y2; ymax=y1
    c1 = np.random.uniform(low=plot_params['colors']['min'], 
                           high=plot_params['colors']['max'])
    c2 = np.random.uniform(low=plot_params['colors']['min'], 
                           high=plot_params['colors']['max'])
    if c1<c2:
        cmin = c1; cmax = c2
    else:
        cmin=c2; cmax=c1

    if distribution == 'random':
        #print(xmin,xmax)
        xs,ys,colors = get_random_data('contour',xmin,xmax,ymin,ymax,
                                  npoints=(nx,ny),
                                  zmin=cmin, zmax=cmax) 
    elif distribution == 'linear':
        xs,ys,colors, data_params = get_linear_data('contour',plot_params['distribution'][distribution],
                                                    xmin,xmax,ymin,ymax,
                                  npoints=(nx,ny))#,
                                  #zmin=cmin, zmax=cmax) 
    elif distribution == 'gmm':
        xs,ys,colors, data_params = get_gmm_data('contour',
                                                 plot_params['distribution'][distribution],
                                                    xmin,xmax,ymin,ymax,
                                  npoints=(nx,ny),
                                  zmin=cmin, zmax=cmax) 

    # do we have x/y error bars?
    hasXErr = False; hasYErr = False
    xerr,yerr = [],[] # x/y error maybe later

    # if np.random.uniform(0,1) <= plot_params['error bars']['x']['prob']: # yes
    #     hasXErr = True
    #     scale = xmax-xmin
    #     xerr = np.random.uniform(low=plot_params['error bars']['x']['size']['min']*scale, 
    #                              high=plot_params['error bars']['x']['size']['max']*scale,
    #                              size=npoints)
    # if np.random.uniform(0,1) <= plot_params['error bars']['y']['prob']: # yes
    #     hasYErr = True
    #     scale = ymax-ymin
    #     yerr = np.random.uniform(low=plot_params['error bars']['y']['size']['min']*scale, 
    #                              high=plot_params['error bars']['y']['size']['max']*scale,
    #                              size=npoints)

    #print(xerr)
    #print(yerr)
    return xs, ys, colors, xerr, yerr, data_params


############################################################
######################## LINES DATA ########################
############################################################

def get_line_data(plot_params, npoints,nlines,xmin=0, xmax=1, ymin=0, ymax=1, 
                  prob_same_x=0.1,
                  xordered=True, verbose=True,
                 pick_xrange=True, pick_yrange=True,
                 distribution='random'):
    """
    ymin/ymax : can be a number of a list, if list, needs to be matched up with number of nlines
    xordered : do we want to put the x-points in a monotonic order?
    """
    data_params = {}
    if (type(ymin) not in [list, np.ndarray]) and (type(ymax) not in [list, np.ndarray]):
        pass
    elif ((type(ymin) not in [list, np.ndarray]) and (type(ymax) in [list, np.ndarray])):
        if verbose: print('type of ymin and ymax must be the same!  Will fall back on ints')
        ymax = ymax[0]
    elif ((type(ymin) in [list, np.ndarray]) and (type(ymax) not in [list, np.ndarray])):
        if verbose: print('type of ymin and ymax must be the same!  Will fall back on ints')
        ymin = ymin[0]
    elif len(ymin) != nlines or len(ymax) != nlines:
        if verbose: print('length of ymax, ymin not the same as "nlines", falling back on ints')
        ymin = ymin[0]; ymax = ymax[0]

    nlines = int(round(np.random.uniform(low=nlines['min'], high=nlines['max'])))
    npoints = int(round(np.random.uniform(low=npoints['min'], high=npoints['max'])))

    # pick randomly
    if pick_xrange:
        x1 = np.random.uniform(low=xmin, high=xmax)
        x2 = np.random.uniform(low=xmin, high=xmax)
        if x1<x2:
            xmin = x1; xmax = x2
        else:
            xmin=x2; xmax=x1
    if pick_yrange:
        y1 = np.random.uniform(low=ymin, high=ymax)
        y2 = np.random.uniform(low=ymin, high=ymax)
        if y1<y2:
            ymin = y1; ymax = y2
        else:
            ymin=y2; ymax=y1

    # into arrays
    if (type(ymin) not in [list, np.ndarray]) and (type(ymax) not in [list, np.ndarray]):
        ymin = np.repeat(ymin,nlines)
        ymax = np.repeat(ymax,nlines)

    if distribution == 'random':
        xs,ys = get_random_data('line',xmin,xmax,ymin,ymax,
                    prob_same_x=prob_same_x, 
                            nlines=nlines, npoints=npoints)
    elif distribution == 'linear':
        #print("HI IN GET LINE DATA")
        xs,ys,data_params = get_linear_data('line', plot_params['distribution'][distribution],
                                xmin,xmax,ymin,ymax,
                    prob_same_x=prob_same_x, 
                            nlines=nlines, npoints=npoints)
    elif distribution == 'gmm': # gaussian mixture model
        xs,ys,data_params = get_gmm_data('line', plot_params['distribution'][distribution],
                                xmin,xmax,ymin,ymax,
                    prob_same_x=prob_same_x, 
                            nlines=nlines, npoints=npoints)
        # have to update for binning
        npoints = len(xs[0])
    else:
        print("don't know how to deal with this line distribution!")
        import sys; sys.exit()

    # do we have x/y error bars?
    hasXErr = False; hasYErr = False
    xerrs,yerrs = [],[]

    # for error rate
    #scale = 
    if np.random.uniform(0,1) <= plot_params['error bars']['x']['prob']: # yes
        hasXErr = True
        scale = np.max(xmax)-np.min(xmin)
        for i in range(nlines):
            xerr = np.random.uniform(low=plot_params['error bars']['x']['size']['min']*scale, 
                                 high=plot_params['error bars']['x']['size']['max']*scale,
                                 size=len(xs[i]))
            xerrs.append(xerr)
    if np.random.uniform(0,1) <= plot_params['error bars']['y']['prob']: # yes
        hasYErr = True
        scale = np.max(ymax)-np.min(ymin)
        for i in range(nlines):
            yerr = np.random.uniform(low=plot_params['error bars']['y']['size']['min']*scale, 
                                 high=plot_params['error bars']['y']['size']['max']*scale,
                                 size=len(xs[i]))
            yerrs.append(yerr)
    
    return xs, ys, xerrs, yerrs, data_params


############################################################
######################## SCATTER DATA ########################
############################################################

def get_scatter_data(plot_params, distribution = 'random',
                     verbose=True):
    """
    plot_params : directory with plot params
    """

    data_params = {}
    npoints = int(round(np.random.uniform(low=plot_params['npoints']['min'], 
                                          high=plot_params['npoints']['max'])))
    
    xmin,xmax = plot_params['xmin'],plot_params['xmax']
    ymin,ymax = plot_params['ymin'],plot_params['ymax']


    x1 = np.random.uniform(low=xmin, high=xmax)
    x2 = np.random.uniform(low=xmin, high=xmax)
    if x1<x2:
        xmin = x1; xmax = x2
    else:
        xmin=x2; xmax=x1
    y1 = np.random.uniform(low=ymin, high=ymax)
    y2 = np.random.uniform(low=ymin, high=ymax)
    if y1<y2:
        ymin = y1; ymax = y2
    else:
        ymin=y2; ymax=y1
    c1 = np.random.uniform(low=plot_params['colors']['min'], 
                           high=plot_params['colors']['max'])
    c2 = np.random.uniform(low=plot_params['colors']['min'], 
                           high=plot_params['colors']['max'])
    if c1<c2:
        cmin = c1; cmax = c2
    else:
        cmin=c2; cmax=c1

    if distribution == 'random':
        xs,ys,colors = get_random_data('scatter',xmin,xmax,ymin,ymax,
                                  npoints=npoints,
                                  cmin=cmin, cmax=cmax)
    elif distribution == 'linear':
        xs,ys,colors,data_params = get_linear_data('scatter', 
                                    plot_params['distribution'][distribution],
                                    xmin,xmax,ymin,ymax,
                                    cmin=cmin,cmax=cmax,
                                    npoints=npoints)
    elif distribution == 'gmm':
        xs,ys,colors,data_params = get_gmm_data('scatter', 
                                    plot_params['distribution'][distribution],
                                    xmin,xmax,ymin,ymax,
                                    cmin=cmin,cmax=cmax,
                                    npoints=npoints)
        # have to update npoints based on how things where sampled??
        npoints = len(xs)
    else:
        print('no such distribution in "get_scatter_data"!')
        import sys; sys.exit()


    # do we have x/y error bars?
    hasXErr = False; hasYErr = False
    xerr,yerr = [],[]

    if np.random.uniform(0,1) <= plot_params['error bars']['x']['prob']: # yes
        hasXErr = True
        scale = xmax-xmin
        xerr = np.random.uniform(low=plot_params['error bars']['x']['size']['min']*scale, 
                                 high=plot_params['error bars']['x']['size']['max']*scale,
                                 size=len(xs))
    if np.random.uniform(0,1) <= plot_params['error bars']['y']['prob']: # yes
        hasYErr = True
        scale = ymax-ymin
        yerr = np.random.uniform(low=plot_params['error bars']['y']['size']['min']*scale, 
                                 high=plot_params['error bars']['y']['size']['max']*scale,
                                 size=len(xs))

    #print(xerr)
    #print(yerr)
    return xs, ys, colors, xerr, yerr, data_params



################################################
############ HISTOGRAM PLOTS: PLOT ############
################################################

def get_histogram_data(plot_params, distribution = 'random',
                     verbose=True):
    """
    plot_params : plot parameters
    """

    data_params = {}
    npoints = int(round(np.random.uniform(low=plot_params['npoints']['min'], 
                                          high=plot_params['npoints']['max'])))
    
    xmin,xmax = plot_params['xmin'],plot_params['xmax']

    x1 = np.random.uniform(low=xmin, high=xmax)
    x2 = np.random.uniform(low=xmin, high=xmax)
    if x1<x2:
        xmin = x1; xmax = x2
    else:
        xmin=x2; xmax=x1

    ys = []
    if distribution == 'random':
        xs = get_random_data('histogram',xmin,xmax,
                                  npoints=npoints)
    elif distribution == 'linear':
        xs, data_params = get_linear_data('histogram',plot_params['distribution'][distribution],
                                          xmin,xmax,
                                  npoints=npoints)
    elif distribution == 'gmm':
        xs, data_params = get_gmm_data('histogram',plot_params['distribution'][distribution],
                                          xmin,xmax,
                                  npoints=npoints)
    else:
        print('no distribution in "get_histogram_data"!')
        import sys; sys.exit()
    
    # do we have x/y error bars?
    hasXErr = False; hasYErr = False
    # xerr,yerr = [],[]

    if np.random.uniform(0,1) <= plot_params['error bars']['x']['prob']: # yes
        hasXErr = True
    #     #scale = xmax-xmin
    #     scale = xs
    #     xerr = np.random.uniform(low=plot_params['error bars']['x']['size']['min'], 
    #                              high=plot_params['error bars']['x']['size']['max'],
    #                              size=npoints)*scale
        
    if np.random.uniform(0,1) < plot_params['horizontal prob']: # probability that we have a horizontal bar plot
        # flip
        ys = xs.copy()
        #yerr = xerr.copy()
        #xs = []; ys = []
        hasYErr = True
        hasXErr = False

    return xs, ys, hasXErr, hasYErr, data_params # this is different than other plots!


###########################################################################
######################## MAIN GET DATA #######################
###########################################################################

##### GENERIC DATA AND PLOTS #####
def get_data(plot_params, plot_type='line', distribution='random', #npoints = 100, xmin=0, xmax=1, ymin=0, ymax=1, 
             #xordered=True, nlines=1, # line params
             verbose=True, xordered=True # general params
            ):
    if plot_type == 'line':
        xs, ys, xerrs,yerrs, data_params = get_line_data(plot_params,  
                                            plot_params['npoints'], # this bad coding, should just pass plot_params
                              plot_params['nlines'],
                              xmin=plot_params['xmin'], 
                              xmax=plot_params['xmax'], 
                              ymin=plot_params['ymin'], 
                              ymax=plot_params['ymax'], 
                              prob_same_x=plot_params['prob same x'],
                              xordered=xordered, 
                              verbose=verbose, 
                                            distribution=distribution)
        data = {'xs':xs, 'ys':ys}
        if len(xerrs) > 0:
            data['xerrs'] = xerrs
        if len(yerrs) > 0:
            data['yerrs'] = yerrs
        if data_params != {}:
            data['data params'] = data_params
        return data
    elif plot_type == 'scatter':
        xs, ys, colors_scatter,xerr,yerr, data_params = get_scatter_data(plot_params,
                                                           distribution=distribution)
        data = {'xs':xs, 'ys':ys, 'colors':colors_scatter}
        if len(xerr) > 0:
            data['xerrs'] = xerr
        if len(yerr) > 0:
            data['yerrs'] = yerr
        if data_params != {}:
            data['data params'] = data_params
        return data
    elif plot_type == 'histogram':
        xs,ys,hasXErr,hasYErr, data_params = get_histogram_data(plot_params,
                                                   distribution=distribution)
        data = {'xs':xs, 'ys':ys}
        #if len(xerr) > 0:
        if hasXErr:
            data['xerrs'] = hasXErr # different!
        #if len(yerr) > 0:
        if hasYErr:
            data['yerrs'] = hasYErr # different!
        if data_params != {}:
            data['data params'] = data_params
        return data
    elif plot_type == 'contour':
        xs, ys, color_grid,xerr,yerr, data_params = get_contour_data(plot_params,
                                                       distribution=distribution)
        data = {'xs':xs, 'ys': ys, 'colors':color_grid}
        if len(xerr) > 0:
            data['xerrs'] = xerr
        if len(yerr) > 0:
            data['yerrs'] = yerr
        if data_params != {}:
            data['data params'] = data_params
        return data
    else:
        print('not implement for this plot type!')
        import sys; sys.exit()



