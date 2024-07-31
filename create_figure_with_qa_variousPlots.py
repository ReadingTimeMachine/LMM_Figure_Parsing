# save files
fullproc_r = '/Users/jnaiman/LMM_Figure_Parsing/resources/'

# save here
fake_figs_dir = '/Users/jnaiman/Dropbox/JCDL2024/paper_submission/data_full/'

save_full_json_file = False

nPlots = 200

nProcs = 8

# ------------ Plotting params ------------
import numpy as np
# stats for doing calculations
stats = {'minimum':np.min, 'maximum':np.max, 'median':np.median, 'mean':np.mean}

from plot_parameters import plot_types_params
plot_params = plot_types_params.copy()

# ****** scatter plots *****
linestyles = ['-', '--', ':'] # only use a subset of the linestyles

plot_params_line = {'scatter':plot_params['scatter'].copy()}

plot_params_line['scatter']['npoints'] = {'min':10, 'max':150}

plot_params_line['scatter']['colormap scatter'] = {'prob': 0.85}

# just linear, random
plot_params_line['scatter']['distribution']['random']['prob'] = 1 # 

# gaussian mixture model
plot_params_line['scatter']['distribution']['gmm']['prob'] = 1
plot_params_line['scatter']['distribution']['gmm']['nclusters'] = {'min': 1, 'max': 5}
plot_params_line['scatter']['distribution']['gmm']['nsamples'] = {'min': 10, 'max': 50}

# linear plots
plot_params_line['scatter']['distribution']['linear']['prob'] = 1

# probability of getting a scatter plot
plot_params_line['scatter']['prob'] = 1

# ***** lines *******
plot_params_line['line'] = plot_params['line'].copy()

plot_params_line['line']['npoints'] = {'min':10, 'max':100}
plot_params_line['line']['nlines'] = {'min':1, 'max':10}

# just linear, random
plot_params_line['line']['distribution']['random']['prob'] = 1

# gaussian mixture model
plot_params_line['line']['distribution']['gmm']['prob'] = 1
plot_params_line['line']['distribution']['gmm']['histogram as line']['prob'] = 1
plot_params_line['line']['distribution']['gmm']['nclusters'] = {'min': 1, 'max': 5}
plot_params_line['line']['distribution']['gmm']['nsamples'] = {'min': 10, 'max': 50}

# linear plots
plot_params_line['line']['distribution']['linear']['prob'] = 1

# Prob for getting line
plot_params_line['line']['prob'] = 1

# ********* histograms **********

linestyles_hist = ['-'] # only use a subset of the linestyles

plot_params_line['histogram'] = plot_params['histogram'].copy()

# no horizontal plots
plot_params_line['histogram']['horizontal prob'] = 0.0

# random distributions
plot_params_line['histogram']['distribution']['random']['prob'] = 1

# gaussian mixture model
plot_params_line['histogram']['distribution']['gmm']['prob'] = 1
plot_params_line['histogram']['distribution']['gmm']['nclusters'] = {'min': 1, 'max': 5}
plot_params_line['histogram']['distribution']['gmm']['nsamples'] = {'min': 10, 'max': 50}

# linear distributions prob
plot_params_line['histogram']['distribution']['linear']['prob'] = 1

# ------------- LIBRARIES -----------------

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2 as cv
import pickle
import pandas as pd
#import string
from glob import glob
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PIL import ImageColor
import json

import time

# from matplotlib import font_manager
# plt.rcParams['text.usetex'] = True
import matplotlib as mpl
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = r'\usepackage{amsmath} \usepackage{amssymb}' #for \text command

# written libs
from importlib import reload # debug
import synthetic_fig_utils # debug
reload(synthetic_fig_utils) # debug
from synthetic_fig_utils import subset_by_percent, \
 get_nrows_and_ncols, normalize_params_prob, get_ticks, get_titles_or_labels, \
 get_font_info

import plot_parameters

import plot_utils
reload(plot_utils)
from plot_utils import get_contour_plot, get_histogram_plot, \
   get_line_plot, get_scatter_plot, make_plot#, get_line_plot

import pixel_location_utils
reload(pixel_location_utils)
from pixel_location_utils import get_errorbar_pixels, get_data_pixel_locations

import text_utils
reload(text_utils)
from text_utils import get_popular_nouns, get_inline_math

# create a bunch of fake figures
reload(synthetic_fig_utils)
from synthetic_fig_utils import normalize_params_prob
reload(plot_parameters)
from plot_parameters import panel_params, \
  title_params, xlabel_params, \
  ylabel_params, aspect_fig_params, dpi_params, tight_layout_params, \
  fontsizes, base

import data_utils
reload(data_utils)
from data_utils import get_data, NumpyEncoder

import distribution_utils

from plot_utils import markers
marker_sizes = np.arange(0,10)+1
line_list_thick = np.arange(1,10)

use_uniques = True # use unique inlines
verbose = True

#from sys import path

#path.append('../../full_process/')
#from image_utils import isRectangleOverlap
# special for this install
from yt.enable_parallelism import turn_on_parallelism
from yt.utilities.parallel_tools.parallel_analysis_interface import parallel_objects
from yt.funcs import is_root
turn_on_parallelism()


# ----------- plotting ----------

import plot_qa_utils
reload(plot_qa_utils)

# for figures in general
from plot_qa_utils import log_scale_ax, q1, q2, q3, q4, dpi

# still general, but specific to each plot
from plot_qa_utils import q_plot_titles, q_plot_xlabels, q_plot_ylabels, ticklabels, \
  q_plot_types

# specific to scatter plots
import scatter_plot_qa_utils
reload(scatter_plot_qa_utils)

from scatter_plot_qa_utils import q_npoints_scatter_plot_plotnums, q_colors_scatter_plot_plotnums, \
  q_linemarkers_scatters, q_linemarkersize_scatters, q_datapoints_scatters, \
  q_stats_scatters, q_errorbars_size_scatters, q_relationship_scatters, \
  q_relationship_colors_scatters, q_linear_equation_scatters, q_gmm_equation_scatters

# specific to histogram plots
import histogram_plot_qa_utils
reload(histogram_plot_qa_utils)

from histogram_plot_qa_utils import q_nbars_hist_plot_plotnums, q_colors_hist_plot_plotnums, \
  q_colorlines_hist_plot_plotnums, q_linethickness_hists, q_barpoints_bars, q_stats_hists, \
  q_errorbars_existance_lines, q_errorbars_size_histogram, q_distribution_hists, \
  q_linear_equation_hists, q_gmm_equation_hists

# specific to linear plots
import linear_plot_qa_utils
reload(linear_plot_qa_utils)

from linear_plot_qa_utils import q_nlines_plot_plotnums, \
  q_nlines_plot, q_colors_lines, q_linestyles_lines, \
  q_linethickness_lines, q_linemarkers_lines, q_linemarkersize_lines, \
  q_datapoints_lines, q_stats_lines, q_errorbars_existance_lines, \
  q_errorbars_size_lines, q_relationship_lines, \
  q_linear_equation_lines, q_linear_gmm_lines

# for making plots
import plot_utils
reload(plot_utils)
from plot_utils import get_histogram_plot, make_plot

reload(plot_utils)
import distribution_utils
reload(distribution_utils)

# ------------------- Plotting parameters ----------------

# get fonts -- see "cnn_create_synthetic_ticks" in FullProcess
dfont = pd.read_csv(fullproc_r + 'fonts.csv')
font_names = dfont['font name'].values

# for plot styles
plot_styles = plt.style.available

plot_types_qa = ['line', 'scatter', 'histogram']

# get words
popular_nouns = get_popular_nouns(fullproc_r + 'data/')

inlines = get_inline_math(fullproc_r,
                          recreate_inlines=False,
                         use_uniques=use_uniques)

# ---------------- RUN -------------------

# normalize params
plot_params_line, panel_params, \
  title_params, xlabel_params, \
  ylabel_params = normalize_params_prob(plot_params_line.copy(), panel_params, 
                                        title_params, xlabel_params, 
                                        ylabel_params)

# create qa pairs
qa_pairs = {}
# question levels    
qa_pairs['Level 1'] = {}
qa_pairs['Level 2'] = {}
qa_pairs['Level 3'] = {}
qa_pairs['Level 1']['Figure-level questions'] = {} # Figure-level questions
qa_pairs['Level 1']['Plot-level questions'] = {}
qa_pairs['Level 2']['Plot-level questions'] = {}
qa_pairs['Level 3']['Plot-level questions'] = {}



plot_params_here = plot_params_line.copy()

ifigure = 0

datas_all = {} # for multiples
plt.close('all')

verbose_qa = False

my_storage = {}

# ##### RUN ########

ilist = np.arange(nPlots)

for sto, ifigure in parallel_objects(ilist, nProcs,storage=my_storage):

    print('--------------------- Figure', ifigure, '-------------------')
    ######### pick things ########
    # figure
    color_map = 'gray' # hack#np.random.choice(plt.colormaps())
    #plt.set_cmap(color_map)
    
    npanels, panel_style, nrows, ncols = get_nrows_and_ncols(panel_params)
    ####npanels, panel_style,nrows,ncols = 1, 'horizontal', 1,1 # HACK
    plot_style = np.random.choice(plot_styles)
    
    aspect_fig = np.random.uniform(low=aspect_fig_params['min'], 
                                   high=aspect_fig_params['max'])
    # rows and cols 
    aspect_fig *= nrows/ncols
    dpi = int(np.random.uniform(low=dpi_params['min'], high=dpi_params['max']))
    # tight layout or not
    print('panel style:', panel_style, 'nrows,ncols=', (nrows,ncols), 
          'aspect=', aspect_fig, 'dpi=', dpi)
    
    tight_layout = True


    # get all font stuffs
    title_fontsize, xlabel_fontsize, ylabel_fontsize, \
       xlabel_ticks_fontsize, ylabel_ticks_fontsize, \
                           csfont = get_font_info(fontsizes, font_names)
    #print("ALL IS WELL HERE 1")

    # plot types?
    success = False
    start_time = time.time()
    while not success:
        #with plt.style.context(plot_style):
        if True:
            plt.style.use(plot_style)
            plt.set_cmap(color_map) 
            #plt.rcParams['image.cmap'] = 'gray' #color_map
            if tight_layout:
                fig,axes = plt.subplots(nrows,ncols,figsize=(base*nrows, base*aspect_fig*ncols), 
                                        dpi=dpi,layout='tight')
            else:
                fig,axes = plt.subplots(nrows,ncols,figsize=(base*nrows, base*aspect_fig*ncols), 
                                        dpi=dpi)
                
            if npanels == 1:
                axes = [axes]
                plot_inds = [(0,0)] # i,j
            else: # flatten, for now
                # create inds
                if len(axes.shape) > 1: # 2d
                    ashape = np.array(axes.shape).copy()
                else:
                    ashape = [nrows, ncols]
                plot_inds = np.empty(shape=(ashape[0], ashape[1],2), dtype=int)
                for i in range(ashape[0]):
                    for j in range(ashape[1]):
                        plot_inds[i,j][0] = i
                        plot_inds[i,j][1] = j
                plot_inds = plot_inds.reshape((ashape[0]*ashape[1],-1))
                axes = axes.flatten()
            

            #**HERE** have to save index
                    
            ######### Generate plot data #########
            #print('here 1')
            
            choices = []; probs = []
            for k,v in plot_params_here.items():
                choices.append(k)
                probs.append(v['prob'])
        
            data_for_plots = []
            plot_types = []
            data_from_plots = []
            titles = []; xlabels = []; ylabels = []; cbars = []
            end_time = time.time()
            distribution_types = []
            try:
            #if True:
                for iplot, ax in enumerate(axes):
                    plot_params_here_ax = plot_params_here.copy()
                    start_time = time.time()
                    plot_type = np.random.choice(choices, p=probs)
                    print('PLOT TYPE:', plot_type)
                    # get distribution type
                    dist_params = plot_params_here[plot_type]['distribution'] 
                    choices_d = []; probs_d = []
                    for k,v in dist_params.items():
                        choices_d.append(k)
                        probs_d.append(v['prob'])

                    distribution_type = np.random.choice(choices_d, p=probs_d)
                    print('  Distribution Type:', distribution_type)
                    
                    xmin,xmax = log_scale_ax()
                    plot_params_here_ax[plot_type]['xmin']=xmin
                    plot_params_here_ax[plot_type]['xmax']=xmax
                    if plot_type == 'line' or plot_type == 'scatter' or plot_type == 'contour':
                        ymin,ymax = log_scale_ax()
                        plot_params_here_ax[plot_type]['ymin']=ymin
                        plot_params_here_ax[plot_type]['ymax']=ymax
                    if plot_type == 'scatter' or plot_type == 'contour': 
                        cmin,cmax = log_scale_ax()
                        plot_params_here_ax[plot_type]['colors']['min']=cmin
                        plot_params_here_ax[plot_type]['colors']['max']=cmax
  
                    
                    #print('here 2')
                    success_get_data = False
                    while not success_get_data:
                        data_for_plot = get_data(plot_params_here_ax[plot_type],
                                        plot_type=plot_type,
                                                distribution=distribution_type)
                        if len(data_for_plot['xs']) > 0 and len(data_for_plot['ys'])>0 and plot_type != 'histogram':
                            success_get_data = True
                        elif len(data_for_plot['xs']) > 0 and plot_type == 'histogram':
                            success_get_data = True
                    end_time = time.time()
                
                    ######### PLOT ############
                    start_time = time.time()
                    #print('here 3')
                    if plot_type != 'histogram':
                        data_from_plot, ax = make_plot(plot_params_here_ax[plot_type], data_for_plot, 
                                             ax, plot_type=plot_type, linestyles=linestyles)#, plot_style=plot_style)
                    else:
                        data_from_plot, ax = make_plot(plot_params_here_ax[plot_type], data_for_plot, 
                                             ax, plot_type=plot_type, linestyles=linestyles_hist)#, plot_style=plot_style)
                    
                    #import sys; sys.exit()
                    end_time = time.time()
                    #print('here 4')
    
                    # set ticksizes
                    ax.tick_params(axis='x', which='major', labelsize=xlabel_ticks_fontsize, labelfontfamily=csfont['fontname'])
                    ax.tick_params(axis='y', which='major', labelsize=ylabel_ticks_fontsize, labelfontfamily=csfont['fontname'])
    
                    start_time = time.time()
                    p = np.random.uniform(0,1)
                    if p < title_params['prob']:
                        title_words = get_titles_or_labels(popular_nouns, title_params['capitalize'],
                                                 title_params['equation'], inlines,
                                                 nwords=np.random.randint(low=title_params['n words']['min'],
                                                                          high=title_params['n words']['max']+1))
                        title = ax.set_title(title_words, fontsize = title_fontsize, **csfont)
                    else:
                        title = ''
                        
                    xlabel_words = get_titles_or_labels(popular_nouns, xlabel_params['capitalize'],
                                                 xlabel_params['equation'], inlines,
                                                 nwords=np.random.randint(low=xlabel_params['n words']['min'],
                                                                          high=xlabel_params['n words']['max']+1))
                    xlabel = ax.set_xlabel(xlabel_words, fontsize=xlabel_fontsize, **csfont)
                    ylabel_words = get_titles_or_labels(popular_nouns, ylabel_params['capitalize'],
                                                 ylabel_params['equation'], inlines,
                                                 nwords=np.random.randint(low=ylabel_params['n words']['min'],
                                                                          high=ylabel_params['n words']['max']+1))
                    ylabel = ax.set_ylabel(ylabel_words, fontsize=ylabel_fontsize, **csfont)
                    end_time = time.time()
            
                    # save
                    data_for_plots.append(data_for_plot)
                    plot_types.append(plot_type)
                    data_from_plots.append(data_from_plot)
                    titles.append(title)
                    xlabels.append(xlabel)
                    ylabels.append(ylabel)
                    distribution_types.append(distribution_type)
    
                    if plot_type == 'scatter': # or plot_type == 'contour':
                        if 'color bar' in data_from_plot:
                            side = data_from_plot['color bar params']['side']
                            if side == 'top' or side == 'bottom':
                                orientation = 'horizontal'
                            else:
                                orientation = 'vertical'
    
                            cbar = fig.colorbar(data_from_plot['data'], 
                                         cax=data_from_plot['color bar'], 
                                         orientation=orientation)
                            cbars.append(cbar)

                    if plot_type == 'contour':
                        if 'color bar' in data_from_plot:
                            side = data_from_plot['color bar params']['side']
                            if side == 'top' or side == 'bottom':
                                orientation = 'horizontal'
                            else:
                                orientation = 'vertical'
                    
                            if 'image' in data_from_plot['data']: # select correct colorbar to use
                                datac = data_from_plot['data']['image']
                            else:
                                datac = data_from_plot['data']['contour']
                                            
                            cbar = fig.colorbar(datac, 
                                         cax=data_from_plot['color bar'], 
                                         orientation=orientation)
                            cbars.append(cbar)

    
                #if not save_smalls:
                plt.set_cmap(color_map) # do again
                fig.tight_layout()
                fig.savefig(fake_figs_dir + 'Picture' + str(ifigure+1) + '.png', dpi=dpi)#, bbox_inches='tight')
                print('saved:', fake_figs_dir + 'Picture' + str(ifigure+1) + '.png')
                # else:
                #     fig.savefig(save_small_dir + 'Picture' + str(ifigure+1) + '.png', dpi=dpi)
                #     print('saved:', save_small_dir + 'Picture' + str(ifigure+1) + '.png')
                    
                success = True
            except Exception as e:
            #else:
                print('[ERROR]:')
                plt.close(fig)
                print('issue with plotting, trying again')
                print(e)
                if 'unknown color specifier' in str(e):
                    print(e)
                    import sys; sys.exit()
                if 'At least one value in the dash list must be positive' in str(e):
                    print(e)
                    print(data_from_plots)
    
    
    ####### end of plotting ############
    # try the whole thing again
    width, height = fig.canvas.get_width_height()
    # save data
    datas = {}
    # figure datas
    datas['figure'] = {'dpi':dpi, 'base':base, 'aspect ratio': aspect_fig, 
                          'nrows':nrows, 'ncols':ncols, 
                         'plot style':plot_style, 
                         'color map':color_map,
                         'title fontsize':title_fontsize, 
                         'xlabel fontsize':xlabel_fontsize,
                         'ylabel fontsize':ylabel_fontsize, 
                      'plot indexes':plot_inds}
    
    # now, get data things
    for iplot, ax in enumerate(axes):
        ###### get data from plot ######
        data_from_plot = data_from_plots[iplot]
        data_for_plot = data_for_plots[iplot]
        plot_type = plot_types[iplot]
        title = titles[iplot]
        xlabel = xlabels[iplot]
        ylabel = ylabels[iplot]
    
        data_pixels = get_data_pixel_locations(data_from_plot, plot_type, ax, width, height)
    
        # bounding box of square
        bbox = ax.get_position() # Bbox(x0, y0, x1, y1)
        xpix1 = np.array([bbox.x0,bbox.x1])
        ypix1 = np.array([bbox.y0,bbox.y1])
        xpix1 *= width
        ypix1 *= height
        
        # x-tick locations
        xticks = get_ticks(ax.get_xticklabels(), ax.get_xticklines())
    
        # y-tick locations
        yticks = get_ticks(ax.get_yticklabels(), ax.get_yticklines())
        
        # for colorbars
        colorbar_ticks = []
        if 'color bar' in data_from_plots[iplot]:
            colorbar = data_from_plots[iplot]['color bar']
            if data_from_plots[iplot]['color bar params']['side'] == 'left' \
               or data_from_plots[iplot]['color bar params']['side'] == 'right':
                ticks = colorbar.get_yticklabels()
                tick_locs = colorbar.get_yticklines(minor=False)
            else:
                ticks = colorbar.get_xticklabels()
                tick_locs = colorbar.get_xticklines(minor=False)
            colorbar_ticks = get_ticks(ticks, tick_locs)

        # title
        # Get the bounding box of the title in display space
        if title != '':
            title_bbox = title.get_window_extent()
            title_words = title.get_text()
        else:
            title_bbox = -1
            title_words = ''
    
        # xlabel
        xlabel_bbox = xlabel.get_window_extent()
        xlabel_words = xlabel.get_text()
        # ylabel
        ylabel_bbox = ylabel.get_window_extent()
        ylabel_words = ylabel.get_text()
    
    
        ########## save data ##############

        # line plot 
        plot_name = 'plot' + str(iplot) 
        datas[plot_name] = {}
        # line plot type
        datas[plot_name]['type'] = plot_type # tag for kind of plot
        datas[plot_name]['distribution'] = distribution_types[iplot]
        datas[plot_name]['data'] = data_for_plot
        datas[plot_name]['data pixels'] = data_pixels
        datas[plot_name]['data from plot'] = json.loads(json.dumps(data_from_plot, cls=NumpyEncoder))
        if (plot_type == 'scatter' or plot_type == 'contour') and 'color bar' in data_from_plots[iplot]:
            #print('yes indeed')
            w = data_from_plots[iplot]['color bar'].get_window_extent()
            datas[plot_name]['color bar'] = {'xmin':w.x0,'ymin':w.y0,
                                             'xmax':w.x1,'ymax':w.y1, 
                                             'params':data_from_plot['color bar params']}
        xtmp = []
        for xt in xticks:
            l = {'data':xt[0], 'xmin': xt[1], 
                 'ymin': xt[2], 
                 'xmax':xt[3], 'ymax':xt[4],
                 'tx':xt[5], 'ty':xt[6]}
            xtmp.append(l)
        datas[plot_name]['xticks'] = xtmp.copy()
        # 
        xtmp = []
        for xt in yticks:
            l = {'data':xt[0], 'xmin': xt[1], 
                 'ymin': xt[2], 
                 'xmax':xt[3], 'ymax':xt[4], 
                'tx':xt[5], 'ty':xt[6]}
            xtmp.append(l)
        datas[plot_name]['yticks'] = xtmp.copy()
        if len(colorbar_ticks) > 0:
            xtmp = []
            for xt in colorbar_ticks:
                l = {'data':xt[0], 'xmin': xt[1], 
                     'ymin': xt[2], 
                     'xmax':xt[3], 'ymax':xt[4], 
                    'tx':xt[5], 'ty':xt[6]}
                xtmp.append(l)
            datas[plot_name]['color bar ticks'] = xtmp.copy()
            
        # axis box
        datas[plot_name]['square'] = {'xmin':xpix1[0], 'ymin':ypix1[0], 
                                         'xmax':xpix1[1], 'ymax':ypix1[1]}
        # title
        if title_bbox != -1:
            datas[plot_name]['title'] = {'xmin':title_bbox.x0, 'ymin':title_bbox.y0, 
                                            'xmax':title_bbox.x1, 'ymax':title_bbox.y1,
                                           'words':title_words}
        else:
            pass
        datas[plot_name]['xlabel'] = {'xmin':xlabel_bbox.x0, 'ymin':xlabel_bbox.y0, 
                                        'xmax':xlabel_bbox.x1, 'ymax':xlabel_bbox.y1,
                                       'words':xlabel_words}
        datas[plot_name]['ylabel'] = {'xmin':ylabel_bbox.x0, 'ymin':ylabel_bbox.y0, 
                                        'xmax':ylabel_bbox.x1, 'ymax':ylabel_bbox.y1,
                                       'words':ylabel_words}

    # dump full data
    if save_full_json_file:
        dumped = json.dumps(datas, cls=NumpyEncoder)
        with open(fake_figs_dir + 'Picture' + str(ifigure+1) + '_fullData.json', 'w') as f:
            json.dump(dumped, f)

    # create qa pairs
    qa_pairs = {}
    # question levels    
    qa_pairs['Level 1'] = {}
    qa_pairs['Level 2'] = {}
    qa_pairs['Level 3'] = {}
    qa_pairs['Level 1']['Figure-level questions'] = {} # Figure-level questions
    qa_pairs['Level 1']['Plot-level questions'] = {}
    qa_pairs['Level 2']['Plot-level questions'] = {}
    qa_pairs['Level 3']['Plot-level questions'] = {}

    #print(qa_pairs)

    ###### L1 ######
    # basic figure level
    qa_pairs = q1(datas, qa_pairs, verbose=verbose_qa)
    qa_pairs = q2(datas, qa_pairs, verbose=verbose_qa)
    qa_pairs = q3(datas, qa_pairs, verbose=verbose_qa)
    qa_pairs = q4(datas, qa_pairs, verbose=verbose_qa)

    # basic, plot-level
    # titles/axis labels
    qa_pairs = q_plot_titles(datas, qa_pairs, verbose=verbose_qa)
    qa_pairs = q_plot_xlabels(datas, qa_pairs, verbose=verbose_qa)
    qa_pairs = q_plot_ylabels(datas, qa_pairs, verbose=verbose_qa)
    # x/y axis tick labels
    qa_pairs = ticklabels(datas, qa_pairs, tick_type='x', verbose=verbose_qa)
    qa_pairs = ticklabels(datas, qa_pairs, tick_type='y', verbose=verbose_qa)
    # plot types
    qa_pairs = q_plot_types(datas, qa_pairs, plot_types_qa, use_list=True, verbose=verbose_qa)

    # line-plot specifics
    for iplot in range(len((axes))):
        if datas['plot'+str(iplot)]['type'] == 'line': # line plots
            ####### L1 ########
            # line plots in numbers/words
            qa_pairs = q_nlines_plot_plotnums(datas, qa_pairs, plot_num = iplot, verbose=verbose_qa)
            qa_pairs = q_nlines_plot(datas, qa_pairs, plot_num = iplot, verbose=verbose_qa)
            # colors of lines
            qa_pairs = q_colors_lines(datas, qa_pairs, plot_num=iplot, use_words=False, verbose=verbose_qa)
            qa_pairs = q_colors_lines(datas, qa_pairs, plot_num=iplot, use_words=True, verbose=verbose_qa)
            # linestyles
            qa_pairs = q_linestyles_lines(datas, qa_pairs, plot_num=iplot, 
                                          use_words=False, use_list=False, verbose=verbose_qa)
            qa_pairs = q_linestyles_lines(datas, qa_pairs, plot_num=iplot, 
                                          use_words=True, use_list = False, verbose=verbose_qa)
            qa_pairs = q_linestyles_lines(datas, qa_pairs, plot_num=iplot, 
                                          use_words=False, use_list=True,
                              linestyle_list=linestyles, verbose=verbose_qa)
            qa_pairs = q_linestyles_lines(datas, qa_pairs, plot_num=iplot, 
                                          use_words=True, use_list = True,
                              linestyle_list=linestyles, verbose=verbose_qa)
            # line thicknesses
            qa_pairs = q_linethickness_lines(datas, qa_pairs, 
                                             plot_num=iplot, use_words=False, verbose=verbose_qa)
            qa_pairs = q_linethickness_lines(datas, qa_pairs, plot_num=iplot,  
                                             use_words=True, verbose=verbose_qa)
            # line markers
            qa_pairs = q_linemarkers_lines(datas, qa_pairs, plot_num=iplot, use_words=False, verbose=verbose_qa)
            qa_pairs = q_linemarkers_lines(datas, qa_pairs, plot_num=iplot, use_words=True, verbose=verbose_qa)
            # line marker sizes
            qa_pairs = q_linemarkersize_lines(datas, qa_pairs, plot_num=iplot, use_words=False, verbose=verbose_qa)
            qa_pairs = q_linemarkersize_lines(datas, qa_pairs, plot_num=iplot, use_words=True, verbose=verbose_qa)
            # data points
            qa_pairs = q_datapoints_lines(datas, qa_pairs, plot_num=iplot, use_words=False, verbose=verbose_qa)
            qa_pairs = q_datapoints_lines(datas, qa_pairs, plot_num=iplot, use_words=True, verbose=verbose_qa)

            ###### L2 #######
            # stats items
            for k,v in stats.items(): # for all stats
                qa_pairs = q_stats_lines(datas, qa_pairs, stat={k:v}, 
                                         plot_num=iplot, use_words=False, verbose=verbose_qa)
                qa_pairs = q_stats_lines(datas, qa_pairs, stat={k:v}, 
                                         plot_num=iplot, use_words=True, verbose=verbose_qa)

            # existance of error bars & values
            for axisv in ['x','y']:
                qa_pairs = q_errorbars_existance_lines(datas, qa_pairs, 
                                                       axis=axisv, plot_num=iplot, use_words=False, verbose=verbose_qa)
                qa_pairs = q_errorbars_existance_lines(datas, qa_pairs, 
                                                       axis=axisv, plot_num=iplot, use_words=True, verbose=verbose_qa)  

                if axisv + 'errs' in datas['plot'+str(iplot)]['data']:
                    qa_pairs = q_errorbars_size_lines(datas, qa_pairs, axis=axisv, 
                                                      plot_num=iplot, use_words=False, verbose=verbose_qa)
                    qa_pairs = q_errorbars_size_lines(datas, qa_pairs, axis=axisv, 
                                                      plot_num=iplot, use_words=True, verbose=verbose_qa) 

            ###### L3 ######
            # type of functional relationship
            for use_list in [True,False]:
                qa_pairs = q_relationship_lines(datas, qa_pairs, plot_num=iplot, use_words=False, 
                                                use_nlines = False, verbose=verbose_qa, use_list=True)
                qa_pairs = q_relationship_lines(datas, qa_pairs, plot_num=iplot, use_words=True, 
                                                use_nlines = False, verbose=verbose_qa, use_list=True)
                qa_pairs = q_relationship_lines(datas, qa_pairs, plot_num=iplot, use_words=False, 
                                                use_nlines = True, verbose=verbose_qa, use_list=True)
                qa_pairs = q_relationship_lines(datas, qa_pairs, plot_num=iplot, use_words=True, 
                                                use_nlines = True, verbose=verbose_qa, use_list=True)
            # relationship parameters (Linear & GMM)
            hasLine = False
            hasGMM = False
            if 'data params' not in datas['plot'+str(iplot)]['data']:
                if verbose_qa: print('Not a linear relationship!')
            else:
                for k,v in datas['plot'+str(iplot)]['data']['data params'].items():
                    if 'line' in k and distribution_types[iplot]=='linear':
                        hasLine = True
                    elif 'line' in k and distribution_types[iplot]=='gmm':
                        hasGMM = True
            if hasLine: # linear
                qa_pairs = q_linear_equation_lines(datas, qa_pairs, plot_num=iplot, 
                                                   use_words=False, use_nlines = False, verbose=verbose_qa)
                qa_pairs = q_linear_equation_lines(datas, qa_pairs, plot_num=iplot, 
                                                   use_words=True, use_nlines = False, verbose=verbose_qa)
                qa_pairs = q_linear_equation_lines(datas, qa_pairs, plot_num=iplot, 
                                                   use_words=False, use_nlines = True, verbose=verbose_qa)
                qa_pairs = q_linear_equation_lines(datas, qa_pairs, plot_num=iplot, 
                                                   use_words=True, use_nlines = True, verbose=verbose_qa)

            if hasGMM: # GMM
                qa_pairs = q_linear_gmm_lines(datas, qa_pairs, plot_num=iplot, 
                                              use_words=False, use_nlines = False, verbose=verbose_qa)
                qa_pairs = q_linear_gmm_lines(datas, qa_pairs, plot_num=iplot, 
                                              use_words=True, use_nlines = False, verbose=verbose_qa)
                qa_pairs = q_linear_gmm_lines(datas, qa_pairs, plot_num=iplot, 
                                              use_words=False, use_nlines = True, verbose=verbose_qa)
                qa_pairs = q_linear_gmm_lines(datas, qa_pairs, plot_num=iplot, 
                                              use_words=True, use_nlines = True, verbose=verbose_qa)  
        elif datas['plot'+str(iplot)]['type'] == 'scatter':
            ############ L1 #############
            # number of points
            qa_pairs = q_npoints_scatter_plot_plotnums(datas, qa_pairs, plot_num = iplot, use_words=False, verbose=verbose_qa)
            qa_pairs = q_npoints_scatter_plot_plotnums(datas, qa_pairs, plot_num = iplot, use_words=True, verbose=verbose_qa)
            # colors of each point
            qa_pairs = q_colors_scatter_plot_plotnums(datas, qa_pairs, plot_num = iplot, use_words=False, verbose=verbose_qa)
            qa_pairs = q_colors_scatter_plot_plotnums(datas, qa_pairs, plot_num = iplot, use_words=True, verbose=verbose_qa)
            # marker types
            qa_pairs = q_linemarkers_scatters(datas, qa_pairs, plot_num = iplot, 
                                              use_words=False, use_list=False, verbose=verbose_qa)
            qa_pairs = q_linemarkers_scatters(datas, qa_pairs, plot_num = iplot, 
                                              use_words=True, use_list = False, verbose=verbose_qa)
            qa_pairs = q_linemarkers_scatters(datas, qa_pairs, plot_num = iplot, 
                                              use_words=False, use_list=True, 
                                              line_list=markers, verbose=verbose_qa)
            qa_pairs = q_linemarkers_scatters(datas, qa_pairs, plot_num = iplot, 
                                              use_words=True, use_list = True, 
                                              line_list=markers, verbose=verbose_qa)
            # marker sizes
            qa_pairs = q_linemarkersize_scatters(datas, qa_pairs, plot_num = iplot, 
                                                 use_words=False, use_list=False, verbose=verbose_qa)
            qa_pairs = q_linemarkersize_scatters(datas, qa_pairs, plot_num = iplot, 
                                                 use_words=True, use_list = False, verbose=verbose_qa)
            qa_pairs = q_linemarkersize_scatters(datas, qa_pairs, plot_num = iplot, 
                                                 use_words=False, use_list=True, 
                                                 line_list=marker_sizes, verbose=verbose_qa)
            qa_pairs = q_linemarkersize_scatters(datas, qa_pairs, plot_num = iplot, 
                                                 use_words=True, use_list = True, 
                                                 line_list=marker_sizes, verbose=verbose_qa)
            # data points x & y & colors
            if 'colors' in datas['plot'+str(iplot)]['data']:
                use_colors = True
            else:
                use_colors = False
            qa_pairs = q_datapoints_scatters(datas, qa_pairs, plot_num = iplot, use_words=False, 
                                             use_colors=use_colors, verbose=verbose_qa)
            qa_pairs = q_datapoints_scatters(datas, qa_pairs, plot_num = iplot, use_words=True, 
                                             use_colors=use_colors, verbose=verbose_qa)

            ###### L2 #######
            # stats items
            for k,v in stats.items():
                qa_pairs = q_stats_scatters(datas, qa_pairs, stat={k:v}, plot_num=iplot, 
                                            use_words=False, use_colors=use_colors, verbose=verbose_qa)
                qa_pairs = q_stats_scatters(datas, qa_pairs, stat={k:v}, plot_num=iplot, 
                                            use_words=True, use_colors=use_colors, verbose=verbose_qa)
                
            # existance of error bars & values
            for axisv in ['x','y']:
                qa_pairs = q_errorbars_existance_lines(datas, qa_pairs, axis=axisv, plot_num=iplot, 
                                                   use_words=False, verbose=verbose_qa)
                qa_pairs = q_errorbars_existance_lines(datas, qa_pairs, axis=axisv, plot_num=iplot, 
                                                   use_words=True, verbose=verbose_qa)

                if axisv + 'errs' in datas['plot'+str(iplot)]['data']:
                    qa_pairs = q_errorbars_size_scatters(datas, qa_pairs, axis=axisv, plot_num=iplot, 
                                                         use_words=False, use_avg=False, verbose=verbose_qa)
                    qa_pairs = q_errorbars_size_scatters(datas, qa_pairs, axis=axisv, plot_num=iplot, 
                                                         use_words=True, use_avg=False, verbose=verbose_qa)
                    qa_pairs = q_errorbars_size_scatters(datas, qa_pairs, axis=axisv, plot_num=iplot, 
                                                         use_words=False, use_avg=True, verbose=verbose_qa)
                    qa_pairs = q_errorbars_size_scatters(datas, qa_pairs, axis=axisv, plot_num=iplot, 
                                                         use_words=True, use_avg=True, verbose=verbose_qa)


            ###### L3 ######
            # type of functional relationship for x & y
            qa_pairs = q_relationship_scatters(datas, qa_pairs, plot_num=iplot, 
                                               use_words=False, verbose=verbose_qa)
            qa_pairs = q_relationship_scatters(datas, qa_pairs, plot_num=iplot, 
                                               use_words=True, verbose=verbose_qa)
            qa_pairs = q_relationship_scatters(datas, qa_pairs, plot_num=iplot, 
                                               use_words=False, verbose=verbose_qa, use_list=True)
            qa_pairs = q_relationship_scatters(datas, qa_pairs, plot_num=iplot, 
                                               use_words=True, verbose = verbose_qa, use_list=True)
            
            # type of functional relationship for colors
            qa_pairs = q_relationship_colors_scatters(datas, qa_pairs, plot_num=iplot, 
                                                      use_words=False, verbose=verbose_qa)
            qa_pairs = q_relationship_colors_scatters(datas, qa_pairs, plot_num=iplot, 
                                                      use_words=True, verbose=verbose_qa)
            qa_pairs = q_relationship_colors_scatters(datas, qa_pairs, plot_num=iplot, 
                                                      use_words=False, verbose=verbose_qa, use_list=True)
            qa_pairs = q_relationship_colors_scatters(datas, qa_pairs, plot_num=iplot, 
                                                      use_words=True, verbose = verbose_qa, use_list=True)
            # linear parameters for x & y & colors
            hasLine = False
            if 'data params' not in datas['plot'+str(iplot)]['data']:
                #print('Not a linear relationship!')
                pass
            else:
                if datas['plot'+str(iplot)]['distribution'] == 'linear':
                    hasLine = True
            if hasLine:
                qa_pairs = q_linear_equation_scatters(datas, qa_pairs, plot_num=iplot, parameter_tag='points',
                                                      use_words=False, verbose=verbose_qa)
                qa_pairs = q_linear_equation_scatters(datas, qa_pairs, plot_num=iplot, parameter_tag='points',
                                                      use_words=True, verbose=verbose_qa)
            # what about line color?
            hasLineColor = False
            if 'data params' in datas['plot'+str(iplot)]:
                if 'colors' in datas['plot'+str(iplot)]['data params']:
                    if datas['plot'+str(iplot)]['data params']['colors']['type'] == 'linear':
                        hasLineColor = True
            if hasLineColor:
                qa_pairs = q_linear_equation_scatters(datas, qa_pairs, plot_num=iplot, 
                                                      parameter_tag='colors', use_words=False, 
                                                      verbose=verbose_qa)
                qa_pairs = q_linear_equation_scatters(datas, qa_pairs, plot_num=iplot, 
                                                      parameter_tag='colors', use_words=True, 
                                                      verbose=verbose_qa)

            # GMM or linear parameters for colors
            hasGMM = False
            if 'data params' not in datas['plot'+str(iplot)]['data']:
                #print('Not a gmm relationship!')
                pass
            else:
                if datas['plot'+str(iplot)]['distribution'] == 'gmm':
                    hasGMM = True
            if hasGMM:
                qa_pairs = q_gmm_equation_scatters(datas, qa_pairs, plot_num=iplot, 
                                                   parameter_tag='points', use_words=False, 
                                                      verbose=verbose_qa)
                qa_pairs = q_gmm_equation_scatters(datas, qa_pairs, plot_num=iplot, 
                                                   parameter_tag='points', use_words=True, 
                                                      verbose=verbose_qa)
            # what about line color?
            hasGMMColor = False
            if 'data params' in datas['plot'+str(iplot)]:
                if 'colors' in datas['plot'+str(iplot)]['data params']:
                    if datas['plot'+str(iplot)]['data params']['colors']['type'] == 'gmm':
                        hasGMMColor = True
            if hasGMMColor:
                qa_pairs = q_gmm_equation_scatters(datas, qa_pairs, plot_num=iplot, 
                                        parameter_tag='colors', use_words=False, 
                                                      verbose=verbose_qa)
                qa_pairs = q_gmm_equation_scatters(datas, qa_pairs, plot_num=iplot, 
                                        parameter_tag='colors', use_words=True, 
                                                      verbose=verbose_qa)
        elif datas['plot'+str(iplot)]['type'] == 'histogram':
            ############ L1 #############
            # number of bars
            qa_pairs = q_nbars_hist_plot_plotnums(datas, qa_pairs, plot_num = iplot, use_words=False, verbose=verbose_qa)
            qa_pairs = q_nbars_hist_plot_plotnums(datas, qa_pairs, plot_num = iplot, use_words=True, verbose=verbose_qa)
            # colors of bars
            qa_pairs = q_colors_hist_plot_plotnums(datas, qa_pairs, plot_num = iplot, use_words=False, verbose=verbose_qa)
            qa_pairs = q_colors_hist_plot_plotnums(datas, qa_pairs, plot_num = iplot, use_words=True, verbose=verbose_qa)
            # colors of lines around each bar
            qa_pairs = q_colorlines_hist_plot_plotnums(datas, qa_pairs, plot_num = iplot, use_words=False, verbose=verbose_qa)
            qa_pairs = q_colorlines_hist_plot_plotnums(datas, qa_pairs, plot_num = iplot, use_words=True, verbose=verbose_qa)
            # if present, thickness of lines around each bar
            qa_pairs = q_linethickness_hists(datas, qa_pairs, plot_num = iplot, 
                                             use_words=False, use_list = False, verbose=verbose_qa)
            qa_pairs = q_linethickness_hists(datas, qa_pairs, plot_num = iplot, 
                                             use_words=True, use_list = False, verbose=verbose_qa)
            qa_pairs = q_linethickness_hists(datas, qa_pairs, plot_num = iplot, 
                                             use_words=False, use_list = True, 
                                             line_list=line_list_thick, verbose=verbose_qa)
            qa_pairs = q_linethickness_hists(datas, qa_pairs, plot_num = iplot, 
                                             use_words=True, use_list = True, 
                                             line_list=line_list_thick, verbose=verbose_qa)

            # left/right/center locations of each bar & height of each bar
            qa_pairs = q_barpoints_bars(datas, qa_pairs, plot_num = iplot, use_words=False, verbose=verbose_qa)
            qa_pairs = q_barpoints_bars(datas, qa_pairs, plot_num = iplot, use_words=True, verbose=verbose_qa)

            ###### L2 #######
            # stats items
            for k,v in stats.items():
                qa_pairs = q_stats_hists(datas, qa_pairs, stat={k:v}, plot_num=iplot, use_words=False, verbose=verbose_qa)
                qa_pairs = q_stats_hists(datas, qa_pairs, stat={k:v}, plot_num=iplot, use_words=True, verbose=verbose_qa)

            # existance of error bars & values
            qa_pairs = q_errorbars_existance_lines(datas, qa_pairs, axis='x', plot_num=iplot, 
                                                   use_words=False, name_of_axis='y', verbose=verbose_qa)
            qa_pairs = q_errorbars_existance_lines(datas, qa_pairs, axis='x', plot_num=iplot, 
                                                   use_words=True, name_of_axis='y', verbose=verbose_qa)

            # size of error bars
            qa_pairs = q_errorbars_size_histogram(datas, qa_pairs, axis='x', plot_num=iplot, 
                                                  use_words=False, use_avg=False, name_of_axis='y', verbose=verbose_qa)
            qa_pairs = q_errorbars_size_histogram(datas, qa_pairs, axis='x', plot_num=iplot, 
                                                  use_words=True, use_avg=False, name_of_axis='y', verbose=verbose_qa)
            qa_pairs = q_errorbars_size_histogram(datas, qa_pairs, axis='x', plot_num=iplot, 
                                                  use_words=False, use_avg=True, name_of_axis='y', verbose=verbose_qa)
            qa_pairs = q_errorbars_size_histogram(datas, qa_pairs, axis='x', plot_num=iplot, 
                                                  use_words=True, use_avg=True, name_of_axis='y', verbose=verbose_qa)


            ###### L3 ######
            # what is the approximate distribution of x-values used to create the plot?
            qa_pairs = q_distribution_hists(datas, qa_pairs, plot_num=iplot, 
                                            use_words=False, verbose=verbose_qa)
            qa_pairs = q_distribution_hists(datas, qa_pairs, plot_num=iplot, 
                                            use_words=True, verbose=verbose_qa)
            qa_pairs = q_distribution_hists(datas, qa_pairs, plot_num=iplot, 
                                            use_words=False, use_list=True, verbose=verbose_qa)
            qa_pairs = q_distribution_hists(datas, qa_pairs, plot_num=iplot, 
                                            use_words=True, use_list=True, verbose=verbose_qa)
            
            # linear parameters distribution
            hasLine = False
            if 'data params' not in datas['plot'+str(iplot)]['data']:
                #print('Not a linear relationship!')
                pass
            else:
                if datas['plot'+str(iplot)]['distribution'] == 'linear':
                    hasLine = True
            if hasLine:
                qa_pairs = q_linear_equation_hists(datas, qa_pairs, plot_num=iplot, use_words=False, verbose=verbose_qa)
                qa_pairs = q_linear_equation_hists(datas, qa_pairs, plot_num=iplot, use_words=True, verbose=verbose_qa)
                
            # GMM or linear parameters for colors
            hasGMM = False
            if 'data params' not in datas['plot'+str(iplot)]['data']:
                #print('Not a gmm relationship!')
                pass
            else:
                if datas['plot'+str(iplot)]['distribution'] == 'gmm':
                    hasGMM = True
            if hasGMM:
                qa_pairs = q_gmm_equation_hists(datas, qa_pairs, plot_num=iplot, use_words=False, verbose=verbose_qa)
                qa_pairs = q_gmm_equation_hists(datas, qa_pairs, plot_num=iplot, use_words=True, verbose=verbose_qa)

                
    # also dump qa
    dumped = json.dumps(qa_pairs, cls=NumpyEncoder)
    with open(fake_figs_dir + 'Picture' + str(ifigure+1) + '_qa.json', 'w') as f:
        json.dump(dumped, f)
            
    # for full thing
    #datas_all[ifigure] = datas.copy()
    plt.close(fig)

# back to basics
plt.style.use('default')


if is_root():
    print('DONE!')
