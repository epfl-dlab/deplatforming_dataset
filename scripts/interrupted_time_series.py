import pandas as pd
from datetime import datetime
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import math

dates = list(pd.read_csv('/dlabdata1/reddit_rad/entities/Alex Jones_global.csv').date.values) #because some of the data doesn't have column dates

def extract_ban_date(ban_date):
    return str(ban_date) + '-01'

def to_datetime(date):
    return datetime.strptime(date, '%Y-%m-%d')

def month_diff(a, b):
    return 12 * (a.year - b.year) + (a.month - b.month)

def good_range(ban_date, window):
    return month_diff(to_datetime(extract_ban_date(ban_date)), to_datetime('2020-12-01')) < -window and (month_diff(to_datetime(extract_ban_date(ban_date)), to_datetime('2008-01-01')) > window)


def align_and_center(window, data, ban):
    ''' Selects the approriate subset of the data according to the ban date and the window size and centers the month parameter on     the ban date.
    
    Args:
        window (int): the number of months in consideration before and after the ban date
        data (dataframe): dataframe containing the google trends of the entity under consideration. Must have a 'date' attribute.
        ban (str): ban date of the entity under consideration
       
    Returns:
        The dataframe centered and with new attributes 'month' and 'banned'
    '''
    ban_date = extract_ban_date(ban)
    df = data[data.date.apply(lambda x: abs(month_diff(to_datetime(ban_date), to_datetime(x))) <= window)][['date', 'max_ratio']]
    df['banned'] = df.date.apply(lambda x: 1 if month_diff(to_datetime(ban_date), to_datetime(x))<= 0 else 0)
    df['month'] = range(- window , window + 1)
    return df

def normalize_ratio(df):
    ''' Normalizes the 'max_ratio' of the google trends time series
    '''
    df['norm_max_ratio'] = (df.max_ratio - df.max_ratio.mean())/df.max_ratio.std()
    return df

def combine_all_series(dataset, window, trends_path, add_dates = True):
    ''' Combine all centered and normalized time series for the entities in dataset.
    
    Args:
        dataset (dataframe): deplatforming dataset
        window (int): the number of months in consideration before and after the ban date
        trends_path (str): paths to the files containing the google trends
        add_dates (str): Set to True if using the files in the dlabdata folder, some dates are missing.
    Returns:
        Dataset containing the combined time series for each entities
    '''
    dfs = []
    for i, row in dataset.iterrows():
        entity = row.entity
        try: # Some google trends could not be extracted so some files are missing
            data = pd.read_csv(f'{trends_path}{entity}_global.csv')
            if add_dates:
                data['date'] = dates
            ban_dates = row.ban_date
            for ban_date in ban_dates:
                if good_range(ban_date, window):
                    df = normalize_ratio(align_and_center(window, data, ban_date))
                    df['entity'] = entity
                    dfs.append(df)
        except Exception as e:
            pass
    return pd.concat(dfs)

def compute_time_series(df, log = False, print_model = False):
    ''' Trains the interrupted time series model using the data in df.
    
    Args:
        df (dataframe): pre-processed (centered) google trends time series
        log (bool): To make the model predict the log of the ratio
        print_model (bool): To print the model and its coefficients
        
    Returns:
        df (dataframe): same dataframe as in input but with the predictions given by the model
        params (dict): parameters of the model
        pvalues (dict): p-values associated to the parameters of the model
    '''
    if not log: 
        regr = smf.ols(formula = 'norm_max_ratio ~ month * banned', data = df).fit()
    else:
        regr = smf.ols(formula = 'np.log(max_ratio + 0.1) ~ month * banned', data = df).fit()
    
    df['t_pred'] = regr.predict(df)
    if print_model:
        print(regr.summary())
    return df, regr.params, regr.pvalues

def global_its(dataset, trends_path):
    ''' Computes the interrupted time series model for the whole deplatforming dataset
    
    Args:
        dataset (dataframe): deplatforming dataset
        trends_path (str): paths to the files containing the google trends
    
    Returns:
        results_drop: list (for each window) of the 'banned' parameter, representing the drop or increase of ratio at the
                      moment of the ban.
        results_angle: list (for each window) of the 'month:banned' parameter, representing the angle difference between the
                       trends before and after the ban.
        significant windows: list of boolean pairs (for each window) representing if the parameters are significant or not 
                             (p-value <= 0.05)
    '''
    results_drop = []
    results_angle = []
    significant_windows = []
    for window in range (3, 25):
        i = window-3
        df = combine_all_series(dataset, window, trends_path)
        res, params, pvalues = compute_time_series(df)
        significant_windows.append([window, pvalues['banned'] <= 0.05, pvalues['month:banned'] <= 0.05])
        results_drop.append([window, params['banned'], pvalues['banned']])
        results_angle.append([window, params['month:banned'], pvalues['month:banned']])
    return results_drop, results_angle, significant_windows

def plot_params_by_window(drop, angle):
    df_drop = pd.DataFrame(drop, columns = ['window', 'beta', 'pvalue'])
    df_angle = pd.DataFrame(angle, columns = ['window', 'gamma', 'pvalue'])
    fig, ax = plt.subplots(1, 2, figsize = (10, 8), sharey = False, sharex = True)
    
    # plot the drop
    sbplt1 = ax[0]
    sbplt1.plot('window', 'beta', data = df_drop)
    sbplt1.set_title('Evolution of beta according to window size')
    sbplt1.set_xlabel('Window size')
    sbplt1.set_ylabel('beta')
    
    # plot the angle
    sbplt2 = ax[1]
    sbplt2.plot('window', 'gamma', data = df_angle)
    sbplt2.set_title('Evolution of gamma according to window size')
    sbplt2.set_xlabel('Window size')
    sbplt2.set_ylabel('gamma')
    plt.tight_layout()
    
def individual_time_series(entity, ban_date, window, trends_path, do_log = False, print_model = False, add_dates = True):
    try: # Some google trends could not be extracted so some files are missing
        data = pd.read_csv(f'{trends_path}{entity}_global.csv')
        if add_dates:
            data['date'] = dates
        return compute_time_series(normalize_ratio(align_and_center(window, data, ban_date)), log = do_log, print_model = print_model)
    except Exception as e:
        print(e)
        return None
    
def plot_its(df, entity, window, log = False):
    if log:
        df.max_ratio = df.max_ratio.apply(lambda x: np.log(x+0.01))
    else:
        df.max_ratio = df.norm_max_ratio
    plt.plot('month', 'max_ratio', data = df, color = 'green', marker = 'o', linestyle = 'dashed')
    plt.plot('month', 't_pred', data = df[df.banned == 0], linewidth = 3)
    plt.plot('month', 't_pred', data = df[df.banned == 1], linewidth = 3)
    plt.title(f'Interrupted time series for {entity} and window size {window}')
    plt.xlabel('month')
    plt.ylabel('ratio')
