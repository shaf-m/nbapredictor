from GoogleNews import GoogleNews
from newspaper import Article, Config
import pandas as pd
import nltk

#config will allow us to access the specified url for which we are #not authorized. Sometimes we may get 403 client error while parsing #the link to download the article.
nltk.download('punkt')

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

googlenews=GoogleNews(start='12/20/2022',end='12/23/2022')
googlenews.search('Raptors')
result=googlenews.result()
df=pd.DataFrame(result)
print(df.head())
