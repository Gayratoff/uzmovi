import requests
from bs4 import BeautifulSoup
from main import jsonExtract

def get_movie(name):
    url = f"http://uzmovi.com/search?q={name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    movies = soup.select('a.short-images-link')
    results = []
    count = 0
    for movie in movies:
        title = movie.get('title')
        movie_url = movie.get('href')
        movie_response = requests.get(movie_url)
        movie_soup = BeautifulSoup(movie_response.content, "html.parser")
        links = movie_soup.select('a.btn1')
        qualities = movie_soup.select('button.btn-trailer')
        urls = [{'HAVOLA': link.get('href'), 'SIFATI': quality.text} for link, quality in zip(links, qualities)]
        if title and movie_url and urls:
            results.append({
                'NOMI': title,
                "ONLAYN KO'RISH": movie_url,
                'YUKLASH': urls

            })
            count += 1

    if count > 0:
        result = {
            'ok': True,
            'results': results,
            'count': count,
            'Dasturchi': "@MrGayratov | @MistrUz",
            'Kanal': "@KingsOfPy",
        }
    else:
        result = {
            'ok': False,
            'results': "Natijalar topilmadi",
            'count': count,
            'Dasturchi': "@MrGayratov | @MistrUz",
            'Kanal': "@KingsOfPy",
        }
    return result

name = input("Kino nomini kiriting: ")
result = get_movie(name)
print(result)
print(jsonExtract(result, "NOMI"))
print(jsonExtract(result, "ONLAYN KO'RISH"))
print(jsonExtract(result, "HAVOLA"))