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

    # Let's count the occurrences of each word - this is a prerequisite for finding term frequency
    count_df = words.groupby(['word', 'period']).size().sort_values(ascending=False).reset_index(name='count')

    # Let's sort by term frequency

    pd.set_option('display.max_rows', 10) # You can change the max number of rows that get displayed
    print(count_df)