import pandas as pd
from pandas import option_context
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

def xmostcommon_doubleplot(df_alive, df_dead, variable, title):

    # Make a data definition
    count_alive = df_alive['count']
    bars_alive = df_alive[variable]

    count_dead = df_dead['count']
    bars_dead = df_dead[variable].to_list()

    if variable == 'apacheadmissiondx':
        bars_dead[0] = 'Cardiac arrest' # too long variable name

    y_pos = np.arange(len(bars_dead))
    
    # Create the first subplot
    plt.subplot(221)
    plt.barh(y_pos, count_alive)
    plt.yticks(y_pos, bars_alive)
    # plt.xlabel('Occurrences')
    plt.title(f'{title} (alive)')
    
    # Create the second subplot
    plt.subplot(224)
    plt.barh(y_pos, count_dead)
    plt.yticks(y_pos, bars_dead)
    plt.title(f'{title} (dead)')
    
    # Display the plot
    plt.show()

def xmostcommon_df(df, mortalitystatus, variable, x):
    dataframe = df.groupby(mortalitystatus, as_index=False)[variable].value_counts().reset_index(drop=True)
    df_dead = dataframe[dataframe[mortalitystatus] == 'Expired'][:x].sort_values('count', ascending=True)

    with option_context('display.max_colwidt', 400):
        display(df_dead[[variable, 'count']])