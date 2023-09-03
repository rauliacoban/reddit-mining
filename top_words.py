import matplotlib.pyplot as plt
from cleanup import postsFromCSV
from cleanup import postsToCSV
import nltk
import pandas as pd
import seaborn as sns

infile = "cleaned.csv"
date_limits = ['2019-03-01 00:00:00', 
               '2019-06-01 00:00:00', 
               '2019-09-01 00:00:00', 
               '2020-01-01 00:00:00', 
               '2020-03-01 00:00:00', 
               '2020-06-01 00:00:00', 
               '2020-09-01 00:00:00', 
               '2021-01-01 00:00:00', 
               '2021-03-01 00:00:00', 
               '2021-06-01 00:00:00'
            ]

def getWords(posts):
    words = []
    periods = []
    for idx in posts.index:
        if idx % 50000 == 0:
            print(idx / 1000)
        text = posts['title'][idx]
        date = posts['created'][idx]
        words.extend(nltk.word_tokenize(text))
        for k in range(len(date_limits)):
            if date < date_limits[k]:
                #print(date, date_limits[idx])
                #print(len(words), len(periods))
                #print([k] * (len(words) - len(periods)), '\n')
                periods.extend([k] * (len(words) - len(periods)))
                break

    return pd.DataFrame({
                            'word': words,
                            'period': periods
                        })

if __name__ == "__main__":
    #posts = postsFromCSV(infile)
    #words = getWords(posts)
    #postsToCSV(words, "words.csv")
    words = postsFromCSV("words.csv")

    datas = []

    for i in range(len(date_limits)):
        period = words[words['period'] == i]  # filter to keep only singular nouns
        counts = period['word'].value_counts().head(20)  # count noun occurrences

        counts_ascending = counts.sort_values(ascending=True) # We sort the values in ascending order first, feels more natural to see the lowest values at the bottom, highest at the top
        #print(i, len(counts_ascending))
        #counts_ascending.plot(kind='barh')  # We use barh instead of bar to switch to horizontal view
        datas.append(counts_ascending)
    #plt.show()

    COUNT = len(datas)

    fig, axes = plt.subplots(2, int(COUNT/2), figsize=(12, 8)) # Our figure will be comprised of 2 x 2 subplots
    barplots = []
    for i in range(COUNT):
        data = datas[i]
        row = int(i / int(COUNT/2))
        col = i - row * int(COUNT/2)
        barplots.append(sns.barplot(x=data, y=data.index, ax=axes[row, col], palette='Blues_r'))
        axes[row, col].set_title(date_limits[i])

    # Set y-axis labels to be more readable
    for ax in axes.flat:
        ax.set_ylabel('')

    # Set overall plot title and adjust spacing
    plt.suptitle('Frequency of Most Common Words by Part of Speech', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
