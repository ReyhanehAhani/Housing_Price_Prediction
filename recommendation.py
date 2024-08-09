# -*- coding: utf-8 -*-
"""Recommendation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14_5CF1Z9H2qCDQ2y0zva1ndR9shaNjFp
"""

import pandas as pd
import numpy as np
import networkx as nx

book = pd.read_csv('/content/Books.csv')
user = pd.read_csv('/content/Users.csv')
rate = pd.read_csv('/content/Ratings.csv')

book.head()

book.drop(['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], axis = 1)

user.head()

rate.head()

"""# Creating the Graph
 Each note is Users and books and the edges will be the ratings.
"""

g = nx.Graph()
g.add_nodes_from(book['ISBN'], bipartite=0)
g.add_nodes_from(user['User-ID'].astype(str), bipartite=1)

rate = rate.dropna(subset=['Book-Rating'])
for _, row in rate.iterrows():
    g.add_edge(row['User-ID'], row['ISBN'], weight=int(row['Book-Rating']))

def recommend(user_id, g, num=5):
    user_id = str(user_id)  # Ensure user_id is string if necessary
    if user_id not in g:
        return []  # Return empty if user not in graph

    # Fetch books rated by the user
    rated_books = [n for n, attrs in g[user_id].items() if attrs['weight'] > 0]

    # Personalization for PageRank: only consider this user
    personalization = {node: 0 for node in g}
    personalization[user_id] = 1

    # Compute PageRank scores
    ranking = nx.pagerank(g, personalization=personalization, alpha=0.9)

    # Filter out already rated books and prepare recommendations
    recommendations = {isbn: rank for isbn, rank in ranking.items() if isbn in book['ISBN'].values and isbn not in rated_books}

    # Sort by rank score
    recommended_books = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)

    # Retrieve book titles
    recommended_books_with_titles = []
    for isbn, score in recommended_books[:num]:
        if not book[book['ISBN'] == isbn].empty:
            book_title = book[book['ISBN'] == isbn]['Book-Title'].iloc[0]
            recommended_books_with_titles.append((book_title, score))
        else:
            recommended_books_with_titles.append(("Unknown Title", score))

    return recommended_books_with_titles

# Get recommendations for a specific user
recommended_books = recommend(5, g, 3)
print('Recommended books for user 5:')
for title, score in recommended_books:
    print(f'{title} (Score: {score:.4f})')