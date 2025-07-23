from matplotlib import pyplot as plt
from datetime import datetime
import calendar
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)

dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], date_parser = dateparse)

# Clean data

df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & (df['value']<=df['value'].quantile(0.975))]
df = df.rename(columns = {'date':'Date', 'value':'Page Views'})


def draw_line_plot():
    # Draw line plot
  
    fig = plt.figure(figsize = (28,8))
    sns.lineplot(data=df, x='Date',y='Page Views',color='red').set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
  
    # Save image and return fig (don't change this part)
  
    fig.figure.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar = df.copy()
    df_bar['Years'], df_bar['Months'], df_bar['day'] = pd.DatetimeIndex(df['Date']).year,  pd.DatetimeIndex(df['Date']).month, pd.DatetimeIndex(df['Date']).day
    df_bar = pd.pivot_table(df_bar, index = ['Years','Months'],columns = 'day',values = 'Page Views').fillna(0)
    df_bar.sort_values(by=['Years','Months'],ascending=[True,True],inplace=True)
    df_bar['Average Page Views'] = df_bar.mean(axis = 1)
    df_bar = df_bar.reset_index()
    df_bar['Months'] = df_bar['Months'].apply(lambda x: calendar.month_name[x])
    print(df_bar)
  
    # Draw bar plot
    fig = plt.figure(figsize = (10,10))
    sns.barplot(data = df_bar, x='Years',y='Average Page Views',hue = 'Months', hue_order = months)




    # Save image and return fig (don't change this part)
    
    fig.figure.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
  
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = [d.year for d in df_box.Date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.Date]
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1,2, figsize = (15,10))
    axes[0].set_title('Year-wise Box Plot (Trend)')
    sns.boxplot(ax = axes[0], x=df_box['Year'], y=df_box['Page Views'])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    sns.boxplot(ax = axes[1], x=df_box['Month'], y=df_box['Page Views'], order = months)



    # Save image and return fig (don't change this part)
    fig.figure.savefig('box_plot.png')
    return fig
