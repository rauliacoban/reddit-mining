import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
from scipy import stats
import sklearn as sk
import itertools
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

from cleanup import postsFromCSV

from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from term_freq import COUNT

period_top = [ [] for _ in range(COUNT) ]
words = postsFromCSV("tf.csv")


#words = words.head(200)
unique = words[words['count_word'] >= 5000]['word'].unique()

print(words)
print(len(words))
print(len(unique))
print(unique)

df = pd.DataFrame({"word": unique})

print(df)
for period in range(COUNT):
    for word in unique:
        try:
            val = float(words.loc[(words['period'] == period) & (words['word'] == word)]['tf'])
        except:
            val = 0
        period_top[period].append(val) #words[words['period'] == period]['word' == word]

print(period_top)

for period in range(COUNT):
    df["%i" % period] = pd.DataFrame(period_top[period])
print(df)

foo = sns.heatmap(df.drop('word', axis=1).corr(), vmax=0.6, square=True, annot=True)
