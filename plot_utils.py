# utilities to create plots of different kinds
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = r'\usepackage{amsmath} \usepackage{amssymb}' #for \text command
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from PIL import ImageColor

# for scatter plot markers
from matplotlib.lines import Line2D
marker_dir = Line2D.markers

markers = []
for m,mn in marker_dir.items():
    if type(m) == str:
        if 'None' not in m.lower() and 'nothing' not in mn.lower():
            #print(m, mn)
            markers.append(m)
    else:
        #print(m,mn)
        markers.append(m)

markers = np.array(markers,dtype=object)

# for line styles
from synthetic_fig_utils import get_line_styles
linestyles = get_line_styles()

# for colors
# how many random colors to generate?
# e.g. colors = colors_(6)
colors_ = lambda n: list(map(lambda i: "#" + "%06x" % np.random.randint(0, 0xFFFFFF),range(n)))


# LINES PLOT
def get_line_plot(plot_params, data, ax, linestyles=linestyles):
    datas = []
    linestyles_here = []; linethicks_here = []; markers_here = []
    marker_sizes_here = []
    xerrs = []; yerrs = []
    hasMarker = False
    p = np.random.uniform(0,1)
    colors_here = []
    if p <= plot_params['markers']['prob']:
        hasMarker = True

    elinewidth = int(round(np.random.uniform(low=plot_params['error bars']['elinewidth']['min'], 
                                            high=plot_params['error bars']['elinewidth']['max'])))
    # draw lines
    #xerrs = []; yerrs = []
    for i in range(len(data['ys'])):
        marker = np.random.choice(markers)
        lthick = np.random.uniform(low=plot_params['line thick']['min'], 
                                   high=plot_params['line thick']['max'])

        # choose random linestyle
        linestyle = np.random.choice(linestyles)
        if hasMarker:
            marker_size = int(round(np.random.uniform(low=plot_params['markers']['size']['min'],
                                            high=plot_params['markers']['size']['min'])))
            data_here, = ax.plot(data['xs'][i],data['ys'][i], linewidth=lthick, 
                                 linestyle = linestyle, marker=marker,
                                markersize=marker_size)
        else:
            data_here, = ax.plot(data['xs'][i],data['ys'][i], linewidth=lthick, 
                                 linestyle = linestyle)
            marker = ''
            marker_size = -1

        cols = []
        plt.draw()
        try:
            cols.append(ImageColor.getcolor(data_here.get_color(), "RGBA"))
        except:
            cols.append( (0,0,0) ) # I assume
        cols = np.array(cols)/255.

        if 'xerrs' in data:# and 'yerrs' not in data: # have x-errors
            (_, caps, bars) = ax.errorbar(data['xs'][i],data['ys'][i],xerr=data['xerrs'][i],
                                         linewidth=0,elinewidth=elinewidth,
                                         markersize=0, ecolor=cols, zorder=0)
            xerrs.append(bars)
        if 'yerrs' in data:# and 'xerrs' not in data: # have x-errors
            (_, caps, bars) = ax.errorbar(data['xs'][i],data['ys'][i],yerr=data['yerrs'][i],
                                         linewidth=0, elinewidth=elinewidth,
                                         markersize=0, ecolor=cols, zorder=0)
            yerrs.append(bars)
        
        linethicks_here.append(lthick)
        linestyles_here.append(linestyle)
        markers_here.append(marker)
        datas.append(data_here)
        marker_sizes_here.append(marker_size)
        colors_here.append(cols)

    data_out = {'data':datas, 'plot params':{'linethick':linethicks_here, 
                                            'linestyles':linestyles_here,
                                            'markers':markers_here,
                                            'marker size':marker_sizes_here,
                                            'colors':colors_here}
               }
    # add in x/y errors, if present
    if 'xerrs' in data:
        data_out['x error bars'] = xerrs
    if 'yerrs' in data:
        data_out['y error bars'] = yerrs
    return data_out, ax




# SCATTERS: PLOTS
def get_scatter_plot(plot_params, data, ax):
    p = np.random.uniform(0,1)
    cax = []; side = ''
    marker = np.random.choice(markers)
    marker_size = int(round(np.random.uniform(low=plot_params['markers']['size']['min'],
                                    high=plot_params['markers']['size']['min'])))
    if not p <= plot_params['colormap scatter']['prob']: # not have color map
        data_here = ax.scatter(data['xs'],data['ys'],marker=marker, s=marker_size) 
    else:
        data_here = ax.scatter(data['xs'],data['ys'], 
                               c=data['colors'],marker=marker, 
                              s=marker_size) # need to add color
        divider = make_axes_locatable(ax)

        # get probs
        probs = []; choices = []
        for k,v in plot_params['color bar']['location probs'].items():
            probs.append(v); choices.append(k)
        side = np.random.choice(choices, p=probs)
        size = np.random.uniform(low=plot_params['color bar']['size percent']['min'], 
                     high=plot_params['color bar']['size percent']['max'])
        size = str(int(round(size*100)))+'%'

        pad = np.random.uniform(low=plot_params['color bar']['pad']['min'], 
                                 high=plot_params['color bar']['pad']['max'])

        cax = divider.append_axes(side, size=size, pad=pad)
        # the side of the axis
        if side == 'right': # this maybe should become a random selection?
            axis_side = 'right'
            cax.yaxis.set_ticks_position(axis_side)
        elif side == 'left':
            axis_side = 'left'
            cax.yaxis.set_ticks_position(axis_side)
        elif side == 'top':
            axis_side = 'top'
            cax.xaxis.set_ticks_position(axis_side)
        elif side == 'bottom':
            axis_side = 'bottom'
            cax.xaxis.set_ticks_position(axis_side)

    xerrs = []; yerrs = []
    plt.draw()
    cols = data_here.get_facecolors()
    elinewidth = int(round(np.random.uniform(low=plot_params['error bars']['elinewidth']['min'], 
                                                 high=plot_params['error bars']['elinewidth']['max'])))
    if 'xerrs' in data:# and 'yerrs' not in data: # have x-errors
        cols_scatter = cols.reshape(-1,4)#*255
        # print('cols scatter:', cols_scatter.shape)
        # print('cols type:', cols_scatter.dtype)
        # print('cols min/max:', np.min(cols_scatter), np.max(cols_scatter))
        # print('xs:', data['xs'].shape)
        # print('ys:', data['ys'].shape)
        # print('xerrs:', data['xerrs'].shape)
        #cols_scatter = cols_scatter.astype('int')
        try:
            (_, caps, bars) = ax.errorbar(data['xs'],data['ys'],xerr=data['xerrs'],
                                     linewidth=0,elinewidth=elinewidth,
                                     markersize=0, 
                                      ecolor=cols_scatter, zorder=0)
        except Exception as e:
            print('Issue with colors in xerrs:')
            print(e)
            (_, caps, bars) = ax.errorbar(data['xs'],data['ys'],xerr=data['xerrs'],
                                     linewidth=0,elinewidth=elinewidth,
                                     markersize=0, zorder=0)
            
        xerrs.append(bars)
    if 'yerrs' in data:# and 'xerrs' not in data: # have x-errors
        cols_scatter = cols.reshape(-1,4)#*255
        # print('cols scatter:', cols_scatter.shape)
        # print('cols type:', cols_scatter.dtype)
        # print('cols min/max:', np.min(cols_scatter), np.max(cols_scatter))
        # print('xs:',data['xs'].shape)
        # print('ys:',data['ys'].shape)
        # print('yerrs:',data['yerrs'].shape)
        #cols_scatter = cols_scatter.astype('int')
        try:
            (_, caps, bars) = ax.errorbar(data['xs'],data['ys'],yerr=data['yerrs'],
                                     linewidth=0, elinewidth=elinewidth,
                                     markersize=0, 
                                      ecolor=cols_scatter, zorder=0)
        except Exception as e:
            print('Issue with colors in yerrs:')
            print(e)
            (_, caps, bars) = ax.errorbar(data['xs'],data['ys'],yerr=data['yerrs'],
                                     linewidth=0, elinewidth=elinewidth,
                                     markersize=0, zorder=0)
        yerrs.append(bars)
        
    # save data
    if cax != []:
        data_out = {'data':data_here, 'color bar':cax, 'marker':marker, 'marker size':marker_size,
                    'color bar params':{'side':side, 'pad':pad, 'size':size, 
                                       'axis side':axis_side, 
                                       }
                   }
    else:
        data_out = {'data':data_here, 'marker':marker, 'marker size':marker_size}

    # add in x/y errors, if present
    if 'xerrs' in data:
        data_out['x error bars'] = xerrs
    if 'yerrs' in data:
        #print("YESS TO Y IN DATA")
        data_out['y error bars'] = yerrs
    if 'xerrs' in data or 'yerrs' in data:
        data_out['error bar params']:{'elinewidth':elinewidth}
    
    return data_out, ax




def get_contour_plot(plot_params, data, ax):
    p = np.random.uniform(0,1) # probability that has a colorbar
    #pi = np.random.uniform(0,1) # probability that is an image (vs a contour with lines)
    choices = []; probs = []
    for k,v in plot_params['image or contour']['prob'].items():
        choices.append(k)
        probs.append(v)
    plot_type = np.random.choice(choices, p=probs)
    cax = []; side = ''
    
    if plot_type == 'contour':
        nlevels = int(round(np.random.uniform(low=plot_params['nlines']['min'],
                                              high=plot_params['nlines']['max'])))
        data_here2 = ax.contour(data['xs'], data['ys'], data['colors'], nlevels)
        data_here = {'contour':data_here2}
    elif plot_type == 'image':
        real_x = data['xs']
        real_y = data['ys']
        dx = (real_x[1]-real_x[0])/2.
        dy = (real_y[1]-real_y[0])/2.
        extent = [real_x[0]-dx, real_x[-1]+dx, real_y[0]-dy, real_y[-1]+dy]
        #plt.imshow(data, extent=extent)
        data_here1 = ax.imshow(data['colors'], extent=extent)
        data_here = {'image':data_here1}
    elif plot_type == 'both':
        pg = np.random.uniform(0,1)
        grayContours = False
        if pg <= plot_params['image or contour']['both contours']['prob gray']: # probability that contours are gray for "both" situation
            grayContours = True
        cmap = np.random.choice(['gray', 'gray_r'])
        real_x = data['xs']
        real_y = data['ys']
        dx = (real_x[1]-real_x[0])/2.
        dy = (real_y[1]-real_y[0])/2.
        extent = [real_x[0]-dx, real_x[-1]+dx, real_y[0]-dy, real_y[-1]+dy]
        data_here1 = ax.imshow(data['colors'], extent=extent)
        nlevels = int(round(np.random.uniform(low=plot_params['nlines']['min'],
                                              high=plot_params['nlines']['max'])))
        if not grayContours:
            data_here2 = ax.contour(data['xs'], data['ys'], data['colors'], nlevels)
        else:
            data_here2 = ax.contour(data['xs'], data['ys'], data['colors'], nlevels,
                                   cmap=cmap)

        data_here = {'image':data_here1, 'contour':data_here2}
    else:
        print('not supported plot type!')
        import sys; sys.exit()

    if not p <= plot_params['colormap contour']['prob']: # not have color map
        pass 
    else:
        divider = make_axes_locatable(ax)

        # get probs
        probs = []; choices = []
        for k,v in plot_params['color bar']['location probs'].items():
            probs.append(v); choices.append(k)
        side = np.random.choice(choices, p=probs)
        size = np.random.uniform(low=plot_params['color bar']['size percent']['min'], 
                     high=plot_params['color bar']['size percent']['max'])
        size = str(int(round(size*100)))+'%'

        pad = np.random.uniform(low=plot_params['color bar']['pad']['min'], 
                                 high=plot_params['color bar']['pad']['max'])

        cax = divider.append_axes(side, size=size, pad=pad)
        # the side of the axis
        if side == 'right': # this maybe should become a random selection?
            axis_side = 'right'
            cax.yaxis.set_ticks_position(axis_side)
        elif side == 'left':
            axis_side = 'left'
            cax.yaxis.set_ticks_position(axis_side)
        elif side == 'top':
            axis_side = 'top'
            cax.xaxis.set_ticks_position(axis_side)
        elif side == 'bottom':
            axis_side = 'bottom'
            cax.xaxis.set_ticks_position(axis_side)
    plt.draw()

    # xerrs = []; yerrs = []
    # plt.draw()
    # cols = data_here.get_facecolors()
    # elinewidth = int(round(np.random.uniform(low=plot_params['error bars']['elinewidth']['min'], 
    #                                              high=plot_params['error bars']['elinewidth']['max'])))
    # if 'xerrs' in data:# and 'yerrs' not in data: # have x-errors
    #     (_, caps, bars) = ax.errorbar(data['xs'],data['ys'],xerr=data['xerrs'],
    #                                  linewidth=0,elinewidth=elinewidth,
    #                                  markersize=0, ecolor=cols, zorder=0)
    #     xerrs.append(bars)
    # if 'yerrs' in data:# and 'xerrs' not in data: # have x-errors
    #     (_, caps, bars) = ax.errorbar(data['xs'],data['ys'],yerr=data['yerrs'],
    #                                  linewidth=0, elinewidth=elinewidth,
    #                                  markersize=0, ecolor=cols, zorder=0)
    #     yerrs.append(bars)
        
    # save data
    if cax != []:
        data_out = {'data':data_here, 'color bar':cax, 
                    'color bar params':{'side':side, 'pad':pad, 'size':size, 
                                       'axis side':axis_side}#, 
                                       #'marker':marker, 'marker size':marker_size}
                   }
    else:
        data_out = {'data':data_here}

    # add in x/y errors, if present
    if 'xerrs' in data:
        data_out['x error bars'] = xerrs
    if 'yerrs' in data:
        #print("YESS TO Y IN DATA")
        data_out['y error bars'] = yerrs
    if 'xerrs' in data or 'yerrs' in data:
        data_out['error bar params']:{'elinewidth':elinewidth}
    
    return data_out, ax




# HISTOGRAMS: PLOTS
def get_histogram_plot(plot_params, data, ax):
    datas = []
    linestyles_here = []; linethicks_here = []; markers_here = []
    marker_sizes_here = []
    xerrs = []; yerrs = []

    elinewidth = int(round(np.random.uniform(low=plot_params['error bars']['elinewidth']['min'], 
                                            high=plot_params['error bars']['elinewidth']['max'])))
    rwidth = np.random.uniform(low=plot_params['rwidth']['min'], 
                                            high=plot_params['rwidth']['max'])
    #print('rwidth', rwidth)

    orientation='vertical' # default
    axis = 'xs'
    err = 'xerrs'
    if len(data['xs']) == 0: # flipped!
        axis = 'ys'
        err = 'yerrs'
        orientation='horizontal'


    # line boarder?
    lthick = int(round(np.random.uniform(low=plot_params['line thick']['min'], 
                               high=plot_params['line thick']['max'])))
    if np.random.uniform(0,1) > plot_params['line thick']['prob']:
        lthick = 0

    # choose random linestyle
    linestyle = np.random.choice(linestyles)

    # choose random color
    linecolor = np.array(ImageColor.getcolor(colors_(1)[0],'RGBA'))/255
    barcolor = np.array(ImageColor.getcolor(colors_(1)[0], 'RGBA'))/255

    # number of bins?
    nbins = int(round(np.random.uniform(low=plot_params['nbins']['min'], 
                                            high=plot_params['nbins']['max'])))

    if lthick > 0:
        data_here = ax.hist(data[axis], orientation=orientation, linewidth=lthick, 
                                     linestyle = linestyle, edgecolor=linecolor, 
                            color=barcolor, rwidth=rwidth, bins=nbins)
    else:
        data_here = ax.hist(data[axis], orientation=orientation, 
                                     linestyle = linestyle, edgecolor=linecolor, 
                            color=barcolor, rwidth=rwidth, bins=nbins)

    # add in error bars
    data_heights = data_here[0] # heights of DATA values
    bin_edges = data_here[1] # bin edges of DATA values
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    errs = []
    for b in data_heights:
        es = np.random.uniform(low=plot_params['error bars']['x']['size']['min'], 
                                        high=plot_params['error bars']['x']['size']['max'])
        errs.append(b*es)

    hasErr = False
    if 'xerrs' in data: # different!
        if data['xerrs']:
            hasErr = True
    elif 'yerrs' in data:
        if data['yerrs']:
            hasErr = True

    if hasErr:
        (_, caps, bars) = ax.errorbar(bin_centers,data_heights,yerr=errs,
                                          linewidth=0,elinewidth=elinewidth,
                                          markersize=0, ecolor=linecolor, zorder=10) # error bars on top
    
    xerr_bars = []; yerr_bars = []
    if 'xerrs' in data:
        #if len(data['xerrs']) > 0:
        if data['xerrs']: # DIFFERENT
            #print("YES XERR")
            xerr_bars = bars
    elif 'yerrs' in data:
        #if len(data['yerrs']) > 0:
        if data['yerrs']: # DIFFERENT
            #print("YES YERR")
            yerr_bars = bars

    data_out = {'data':data_here, 'plot params':{
                                            'linethick':lthick, 
                                            'linestyles':linestyle,
                                             'bar color':barcolor,
                                             'edge color':linecolor,
                                             'orientation':orientation,
                                             'rwidth':rwidth,
                                             'nbins':nbins
                                            }
               }
    
    # add in x/y errors, if present
    if len(xerr_bars) > 0:
        data_out['x error bars'] = [xerr_bars] # list for formatting
        data_out['plot params']['elinewidth'] = elinewidth
    if len(yerr_bars) > 0:
        data_out['y error bars'] = [yerr_bars]
        data_out['plot params']['elinewidth'] = elinewidth
    return data_out, ax

###############################################
############## MAIN PLOT #####################
###############################################

def make_plot(plot_params, data, ax, plot_type='line', linestyles=linestyles):#, plot_style='default'):
    if plot_type == 'line':
        data_out, ax = get_line_plot(plot_params, data, ax, linestyles=linestyles)
        return data_out, ax
    elif plot_type == 'scatter':
        data_out, ax = get_scatter_plot(plot_params, data, ax)
        return data_out, ax
    elif plot_type == 'histogram':
        data_out, ax = get_histogram_plot(plot_params, data, ax)
        return data_out, ax
    elif plot_type == 'contour':
        data_out, ax = get_contour_plot(plot_params, data, ax)
        return data_out, ax
    else:
        print('not implement yet!')
        import sys; sys.exit()

