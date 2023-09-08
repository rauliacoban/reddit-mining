from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from cleanup import postsFromCSV

infile = "cleaned.csv"

date_limits = ['2019-06-01 00:00:00', 
               '2019-09-01 00:00:00', 
               '2020-01-01 00:00:00', 
               '2020-03-01 00:00:00', 
               '2020-06-01 00:00:00', 
               '2020-09-01 00:00:00', 
               '2021-01-01 00:00:00', 
               '2020-03-01 00:00:00', 
               '2021-06-01 00:00:00']
periods = []
texts = []

for x in date_limits:
    periods.append([])
    texts.append('')

if __name__ == "__main__":
    posts = postsFromCSV(infile)

    for idx in posts.index:
        if idx % 50000 == 0:
            print(idx / 1000)
        text = posts['title'][idx]
        date = posts['created'][idx]

        for idx in range(len(date_limits)):
            if date < date_limits[idx]:
                #print(date, date_limits[idx])
                periods[idx].append(text)
                break


    for idx in range(len(periods)):
        texts[idx] = ' '.join(periods[idx])
    
    #print(texts)



    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    term_document_matrix = vectorizer.fit_transform(texts)
    print(term_document_matrix) # Print term-document column for the first wiki page


    #'''
    # Apply LDA
    n_topics = 3
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(term_document_matrix)

    # Print top words for each topic
    def print_top_words(model, feature_names, n_top_words):
        for topic_idx, topic in enumerate(model.components_):
            message = f"Topic #{topic_idx + 1}: "
            message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
            print(message)

    n_top_words = 10
    feature_names = vectorizer.get_feature_names_out()
    #print_top_words(lda, feature_names, n_top_words)

    import pyLDAvis
    import pyLDAvis.lda_model

    # Prepare the LDA visualization data
    visualization_data = pyLDAvis.lda_model.prepare(lda, term_document_matrix, vectorizer)

    # Display the LDA visualization
    pyLDAvis.display(visualization_data)
        #'''