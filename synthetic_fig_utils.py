import numpy as np



# for plotting, if you want to chop by tolerance
def subset_by_percent(dfin, tol = 0.01, verbose=True, round_off = 2, 
                     tol_count = None, reset_index = True, 
                     replace_insert = True, replace_deletion = True, 
                    track_insert_delete = False):
    """
    tol : in % (so 1.0 will be 1%, 0.1 will be 0.1%)
    tol_count : if not None, will over-write tol and subset by count
    """
    if tol_count is None:
        dfin_subset = dfin.loc[dfin['counts']> tol].copy()
    else:
        dfin_subset = dfin.loc[dfin['counts unnormalized']> tol_count].copy()

    # also, add the tool tip
    names = []
    for i in range(len(dfin_subset)):
        d = dfin_subset.iloc[i]
        names.append(str(round(d['counts'],2))+'%')
    dfin_subset['name']=names
    
    # rename columns for plotting 
    dfin_subset = dfin_subset.rename(columns={"counts": "% of all OCR tokens", 
                                              "counts unnormalized": "Total Count of PDF token"})
    if reset_index:
        dfin_subset = dfin_subset.reset_index(drop=True)
        
    # replace insert
    if replace_insert:
        dfin_subset.loc[(dfin_subset['ocr_letters']=='^')&(dfin_subset['pdf_letters']!='^'),'ocr_letters'] = 'INSERT'
    if replace_deletion:
        dfin_subset.loc[(dfin_subset['pdf_letters']=='@')&(dfin_subset['ocr_letters']!='@'),'pdf_letters'] = 'DELETE'
        
    d = dfin_subset.loc[(dfin_subset['ocr_letters']=='INSERT')&(dfin_subset['pdf_letters']=='DELETE')]
    if track_insert_delete:
        if len(d) > 0:
            print('Have overlap of insert and delete!')
            print(len(d))
    else: # assume error
        dfin_subset.loc[(dfin_subset['ocr_letters']=='INSERT')&(dfin_subset['pdf_letters']=='DELETE'),
                        '% of all OCR tokens'] = np.nan
        dfin_subset.loc[(dfin_subset['ocr_letters']=='INSERT')&(dfin_subset['pdf_letters']=='DELETE'),
                        "Total Count of PDF token"] = np.nan


    if verbose:
        print('shape of output=', dfin_subset.shape)
    return dfin_subset


def get_line_styles():
    # from https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
    linestyle_str = [
         ('solid', 'solid'),      # Same as (0, ()) or '-'
         ('dotted', 'dotted'),    # Same as (0, (1, 1)) or ':'
         ('dashed', 'dashed'),    # Same as '--'
         ('dashdot', 'dashdot')]  # Same as '-.'
    
    linestyle_tuple = [
         ('loosely dotted',        (0, (1, 10))),
         ('dotted',                (0, (1, 1))),
         ('densely dotted',        (0, (1, 1))),
         ('long dash with offset', (5, (10, 3))),
         ('loosely dashed',        (0, (5, 10))),
         ('dashed',                (0, (5, 5))),
         ('densely dashed',        (0, (5, 1))),
    
         ('loosely dashdotted',    (0, (3, 10, 1, 10))),
         ('dashdotted',            (0, (3, 5, 1, 5))),
         ('densely dashdotted',    (0, (3, 1, 1, 1))),
    
         ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
         ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
         ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))]

    line_styles = []
    for n,l in linestyle_str[::-1]:
        line_styles.append(l)
    for n,l in linestyle_tuple[::-1]:
        line_styles.append(l)
    
    return np.array(line_styles, dtype=object)


def get_nrows_and_ncols(panel_params, verbose=True):
    npanels = int(round(np.random.normal(loc=panel_params['number prob']['median'], 
                                  scale=panel_params['number prob']['std'])))
    if npanels < panel_params['number prob']['min']:
        npanels = panel_params['number prob']['min']
    if npanels > panel_params['number prob']['max']:
        npanels = panel_params['number prob']['max']
    if verbose: print('selected npanels:', npanels)
    
    # panel layout type?
    choices = []; probs = []
    for k,v in panel_params['layout prob'].items():
        choices.append(k)
        probs.append(v)
        
    panel_style = np.random.choice(choices, p=probs)
    
    if npanels > panel_params['to even above']:
        panel_style = 'squarish'
    
    # if square, might need to fudge the actual number
    if panel_style == 'squarish':
        n1 = int(np.floor(np.sqrt(npanels)))
        n2 = int(round(npanels/n1))
        npanels = n1*n2
        nrows, ncols = n1,n2
        # flip?
        if np.random.uniform(0,1) < 0.5:
            nrows,ncols = n2,n1
    elif panel_style == 'horizontal':
        nrows = 1
        ncols = npanels
    elif panel_style == 'vertical':
        nrows = npanels
        ncols = 1
    
    return npanels, panel_style, nrows, ncols


def normalize_params_prob(plot_types_params, panel_params, 
                          title_params, xlabel_params, 
                          ylabel_params, verbose=True):
    # create the fake figs
    #print(plot_types_params['scatter'])
    
    p = 0.0
    for k,v in plot_types_params.items():
        p += v['prob']
    if p != 1.0:
        newp = {}
        for k,v in plot_types_params.items():
            newp[k] = v['prob']/p
            plot_types_params[k]['prob'] = v['prob']/p
        if verbose: 
            print('plot_types_params probability did not add to 1! total =', p)
            print('renormalizing...')
            print('now: ', newp)
    
    # layout prob
    p = 0.0
    for k,v in panel_params['layout prob'].items():
        p += v
    if p != 1.0:
        for k,v in panel_params['layout prob'].items():
            panel_params['layout prob'][k] = v/p
        if verbose:
            print('panel_params layout probability did not add to 1! total =', p)
            print('renormalizing...')
            print('now: ', panel_params['layout prob'])
    
    # capitilize
    p = 0.0
    for k,v in title_params['capitalize'].items():
        p += v
    if p != 1.0:
        for k,v in title_params['capitalize'].items():
            title_params['capitalize'][k] = v/p
        if verbose:
            print('title_params capatilize did not add to 1! total =', p)
            print('renormalizing...')
            print('now: ', title_params['capitalize'])
    p = 0.0
    for k,v in xlabel_params['capitalize'].items():
        p += v
    if p != 1.0:
        for k,v in xlabel_params['capitalize'].items():
            xlabel_params['capitalize'][k] = v/p
        if verbose:
            print('xlabel_params capatilize did not add to 1! total =', p)
            print('renormalizing...')
            print('now: ', xlabel_params['capitalize'])
    p = 0.0
    for k,v in ylabel_params['capitalize'].items():
        p += v
    if p != 1.0:
        for k,v in ylabel_params['capitalize'].items():
            ylabel_params['capitalize'][k] = v/p
        if verbose:
            print('ylabel_params capatilize did not add to 1! total =', p)
            print('renormalizing...')
            print('now: ', ylabel_params['capitalize'])
    
    
    p = 0.0
    for k,v in plot_types_params['scatter']['color bar']['location probs'].items():
        p += v
    if p != 1.0:
        for k,v in plot_types_params['scatter']['color bar']['location probs'].items():
            plot_types_params['scatter']['color bar']['location probs'][k] = v/p
        if verbose:
            print("plot_types_params['scatter']['color bar']['location probs'] did not add to 1! total =", p)
            print('renormalizing...')
            print('now: ', plot_types_params['scatter']['color bar']['location probs'])

    return plot_types_params, panel_params, title_params, xlabel_params, ylabel_params


def get_ticks(ticklabels, ticklines):
    xticks = []
    # ticks = [t for t in ax.get_xticklabels()]
    # tick_locs = ax.get_xticklines()
    ticks = [t for t in ticklabels]
    tick_locs = ticklines
    modder = len(tick_locs)/len(ticks)
    if int(modder) != modder:
        print('cant divide!')
        import sys; sys.exit()

    modder = int(modder)
    for ip, t in enumerate(ticks):
        tx = 0.5*(tick_locs[ip*modder].get_window_extent().x0+tick_locs[ip*modder].get_window_extent().x1)
        ty = 0.5*(tick_locs[ip*modder].get_window_extent().y0+tick_locs[ip*modder].get_window_extent().y1)
        if t.get_visible():
            xticks.append( (t.get_text(), t.get_window_extent().x0, t.get_window_extent().y0,
                            t.get_window_extent().x1, t.get_window_extent().y1, tx,ty) )
    return xticks