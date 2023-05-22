import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
import plotly.express as px
from wordcloud import WordCloud
from scipy import signal
import scipy
#to supress warning
import warnings
warnings.filterwarnings('ignore')


#to make shell more intractive
from IPython.display import display

# setting up the chart size and background
plt.rcParams['figure.figsize'] = (16, 8)
plt.style.use('fivethirtyeight')

train_df  =pd.read_csv("static/dataset/Phising_Training_Dataset.csv") 
test_df   =pd.read_csv("static/dataset/Phising_Testing_Dataset.csv") 
train_df.head()

train_df.drop(['key','Domain_registeration_length'], axis = 1, inplace = True)
train_df.describe().T.style.background_gradient(cmap = 'rocket_r')
