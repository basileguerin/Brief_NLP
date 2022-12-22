import requests
from bs4 import BeautifulSoup
import pandas as pd
import joblib

class Sonic2():
    @staticmethod
    def scrap():
        notes = []
        comments = []
        for i in range(1,13):
            print(f"Page {i} sur 13")
            url = f"https://www.allocine.fr/film/fichefilm-281203/critiques/spectateurs/?page={i}"
            request = requests.get(url)
            soup = BeautifulSoup(request.content, "html.parser")
            datas = soup.find_all('div', {"class": "hred review-card cf"})

            for data in datas:
                comment = data.find("div", {"class": "content-txt review-card-content"}).text
                comment = comment.replace('"',"'")
                comments.append(comment)

                note = data.find("span", {"class": "stareval-note"}).text
                note = note.replace(',', '.')
                notes.append(note)
        

        df = pd.DataFrame(list(zip(comments, notes)), columns= ['Commentaires', 'Notes'])
        return df

class Inception():
    @staticmethod
    def scrap():
        notes = []
        comments = []
        for i in range(1,479):
            print(f"Page {i} sur 479")
            url = f"https://www.allocine.fr/film/fichefilm-143692/critiques/spectateurs/?page={i}"
            request = requests.get(url)
            soup = BeautifulSoup(request.content, "html.parser")
            datas = soup.find_all('div', {"class": "hred review-card cf"})

            for data in datas:
                comment = data.find("div", {"class": "content-txt review-card-content"}).text
                comment = comment.replace('"',"'")
                comments.append(comment)

                note = data.find("span", {"class": "stareval-note"}).text
                note = note.replace(',', '.')
                notes.append(note)
        

        df = pd.DataFrame(list(zip(comments, notes)), columns= ['Commentaires', 'Notes'])
        return df

if __name__ == '__main__':
    df_sonic = Sonic2.scrap()
    df_inception = Inception.scrap()

    datas = {
        'sonic2' : df_sonic,
        'inception' : df_inception
    }
    joblib.dump(datas, 'dataframes')
