from requests import Session
from bs4 import BeautifulSoup
from bs4.element import Tag
import pandas as pd

# keywords = pd.read_csv('keywords.csv', header=0, index_col=None)

keywords = []
text=input("Search Something: ")
keywords.append(text)
df = pd.DataFrame(columns=['keyword', 'title', 'url', 'description'])

for i in keywords:
    # Scraper that gives back: titles, links, descriptions

    params = {"q": i, 'gl': 'IN', 'num': 20}
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36 Edg/80.0.361.62"
    }

    with Session() as session:
        r = session.get(
            "https://www.google.com/search?q=", params=params, headers=headers)

        soup = BeautifulSoup(r.content, 'lxml')

        result_div = soup.find_all('div', attrs={'class': 'g'})

        links = []
        titles = []
        descriptions = []

        for r in result_div:
            # Checks if each element is present, else, raise exception
            try:
                link = r.find('a', href=True)
                title = r.find('h3')

                if isinstance(title, Tag):
                    title = title.get_text()

                description = r.select('.aCOpRe span:not(.f)')

                if isinstance(description, Tag):
                    description = description.get_text()

                # Check to make sure everything is present before appending
                if link != '' and title != '' and description != '':
                    links.append(link['href'])
                    titles.append(title)
                    descriptions.append(description)
            # Next loop if one element is not present
            except Exception as e:
                print(e)
                continue

    for link, title, description in zip(links, titles, descriptions):
        df = df.append({
            'keyword': i,
            'title': title,
            'url': link,
            'description': description
        }, ignore_index=True)
    
        
df.to_csv(r'final_data.csv', index=False)
# file_name = df['keyword']+".csv"
# pd.DataFrame(df).T.to_csv(file_name, index=None)




# for index, row in df.iterrows():
#     file_name = row['Name']+".csv"  #Change the column name accordingly
#     pd.DataFrame(row).T.to_csv(file_name, index=None)