'''
get_news.py
Author: Cole J. Krudwig
'''

import warnings
import yfinance as yf
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import sys
import os

warnings.filterwarnings("ignore", message="Your max_length is set to .*", category=UserWarning)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

class FinBotMedia:
    def __init__(self, ticker_symbol):
        '''
        GetNews

        Parameters:
            self
            ticker_symbol (str): The ticker symbol for the stock you are interested in.
        '''
        self.ticker_symbol = ticker_symbol
        self.stock = yf.Ticker(self.ticker_symbol)
        self.recent_news = None
        self.article_content = {}
        self.fin_table = pd.DataFrame(columns=['Title', 'URL', 'Summary', 'Sentiment'])

    def fetch_news(self):
        '''
        Fetch the most recent articles on yahoo finance about a given company.

        Parameters:
            None

        Returns:
            df (pd.DataFrame): A dataframe of the most recent news stories and their associated data excluding content (see get_content for more about this).
        '''
        news = self.stock.news
        df = pd.DataFrame(news)
        df['date'] = df['providerPublishTime'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
        self.recent_news = df

        links = self.recent_news['link'].tolist()

        for url in links:
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                article = soup.find('div', class_='caas-body')

                if article:
                    content = article.get_text(separator='\n')
                    self.article_content[url] = content
                else:
                    self.article_content[url] = 'Content not found!'
            except requests.RequestException as e:
                self.article_content[url] = 'Request error: Failed to fetch content!'

        return self.recent_news, self.article_content
    
    def summarize_and_analyze(self):
        '''
        Summarizes and analyzes news data of the desired ticker.

        Parameters:
            None

        Returns:
            None
        '''
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

        if self.article_content:
            for url, content in self.article_content.items():
                if content and content != 'Request error: Failed to fetch content!':
                    title = self.recent_news.loc[self.recent_news['link'] == url, 'title'].iloc[0]
                    publisher = str(self.recent_news.loc[self.recent_news['link'] == url, 'publisher'].iloc[0])

                    # Summarize content
                    chunk_size = 1024  # Adjust chunk sizes as needed
                    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
                    summarized_texts = []
                    for chunk in chunks:
                        try:
                            summarized_text = summarizer(chunk, max_length=60, min_length=30, do_sample=False)[0]['summary_text']
                            summarized_texts.append(summarized_text)
                        except Exception as e:
                            print(f"Error summarizing chunk: {e}")
                    summary = "\n".join(summarized_texts)

                    # Sentiment
                    sentiment_chunks = [content[i:i+512] for i in range(0, len(content), 512)]
                    sentiment_scores = []
                    for sentiment_chunk in sentiment_chunks:
                        sentiment = sentiment_analyzer(sentiment_chunk)[0]
                        sentiment_score = int(sentiment['label'].split()[0])
                        sentiment_scores.append(sentiment_score)
                    # Average sentiment score
                    avg_sentiment_score = sum(sentiment_scores) / len(sentiment_scores)

                    # Add data to dataframe
                    new_row = pd.DataFrame({
                        'Title': [title],
                        'URL': [url],
                        'Summary': [summary],
                        'Sentiment': [avg_sentiment_score]
                    })

                    self.fin_table = pd.concat([self.fin_table, new_row], ignore_index=True)

        #print(self.fin_table)

    def display(self):
        '''
        Displays analysis in cli.

        Parameters:
            None

        Returns:
            None
        '''
        for index, row in self.fin_table.iterrows():
            print(f'Title: {row['Title']} \nURL: {row['URL']} \nSummary: {row['Summary']} \nSentiment Score: {row['Sentiment']}')
            print('='*50)
