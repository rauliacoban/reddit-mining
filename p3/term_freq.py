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

COUNT = len(date_limits)

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

    for i in range(COUNT):
        period = words[words['period'] == i]  # filter to keep only singular nouns
        counts = period['word'].value_counts().head(20)  # count noun occurrences

        counts_ascending = counts.sort_values(ascending=True) # We sort the values in ascending order first, feels more natural to see the lowest values at the bottom, highest at the top
        #print(i, len(counts_ascending))
        #counts_ascending.plot(kind='barh')  # We use barh instead of bar to switch to horizontal view
        datas.append(counts_ascending)
    #plt.show()

    # Let's count the occurrences of each word - this is a prerequisite for finding term frequency
    count_words = words.groupby(['word', 'period']).size().sort_values(ascending=False).reset_index(name='count')
    count_period = words.groupby(['period']).size().sort_values(ascending=False).reset_index(name='count')
    df = count_words.merge(count_period, on='period')

    df = df.rename(columns={'count_x': 'count_word', 'count_y': 'count_period'}) # Give more meaningful names
    df['tf'] = df['count_word'] / df['count_period'] * 1000

    postsToCSV(df, "tf.csv")

    #for i in range(len(date_limits)):
    #    print(len(count_df[count_df['period'] == i]))
    # Let's sort by term frequency

    #pd.set_option('display.max_rows', 10) # You can change the max number of rows that get displayed
    #print(count_words)
    #print(count_period)
    #print(df[df['word'] == 'coronavirus'].sort_values(ascending=True, by='period'))
    #print(df[df['word'] == 'vaccine'].sort_values(ascending=True, by='period'))
    #print(df[df['word'] == 'trump'].sort_values(ascending=True, by='period'))
    #print(df[df['word'] == 'kong'].sort_values(ascending=True, by='period'))

    #'''
    topics = [
        'trump',
        'kong',
        'china',
        'myanmar',
        'venezuela',
        'coronavirus',
        'covid',
        'lockdown',
        'vaccine',
        'inflation',
    ]

    fig, axes = plt.subplots(2, int(COUNT/2), figsize=(12, 8)) # Our figure will be comprised of 2 x 2 subplots
    barplots = []
    for i in range(COUNT):
        data = df[df['word'] == topics[i]]
        row = int(i / int(COUNT/2))
        col = i - row * int(COUNT/2)
        barplots.append(sns.barplot(x=data['period'], y=data['tf'], ax=axes[row, col]))
        axes[row, col].set_title(topics[i])

    # Set y-axis labels to be more readable
    for ax in axes.flat:
        ax.set_ylabel('')

    # Set overall plot title and adjust spacing
    plt.suptitle('Term frequency by period', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
    #'''
    '''
    palette = sns.color_palette("Set1")
    palette.extend(sns.color_palette("Pastel1"))
    palette.extend(sns.color_palette("Set3"))
    palette.extend(sns.color_palette("Pastel2"))
    palette.extend(sns.color_palette("Dark2"))
    palette.extend(sns.color_palette("Accent"))
    palette.extend(sns.color_palette("Set2"))
    colorindex = 0
    colormap = dict()

    fig, axes = plt.subplots(2, int(COUNT/2), figsize=(12, 8)) # Our figure will be comprised of 2 x 2 subplots
    barplots = []
    for i in range(COUNT):
        data = df[df['period'] == i].sort_values(ascending=False, by='tf')
        data = data.head(10)

        local_pallete = sns.color_palette(n_colors=0)

        for k in range(10):
            word = data.iloc[k]['word']
            print(word)
            if word not in colormap:
                colormap[word] = palette[colorindex]
                colorindex += 1
            local_pallete.append(colormap[word])

        row = int(i / int(COUNT/2))
        col = i - row * int(COUNT/2)
        barplots.append(sns.barplot(x=data['tf'], y=data['word'], ax=axes[row, col], palette=local_pallete))
        axes[row, col].set_title(date_limits[i])

    # Set y-axis labels to be more readable
    for ax in axes.flat:
        ax.set_ylabel('')

    # Set overall plot title and adjust spacing
    plt.suptitle('Top words by period', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
    '''