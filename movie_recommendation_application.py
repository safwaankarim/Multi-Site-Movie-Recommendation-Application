# Safwaan Karim Homework 9


# Note: All the different thresholds for scores were set based on my own personal preference

# Part A: Importing all the necessary libraries 

import time
import pandas as pd
from bs4 import BeautifulSoup
import requests    


# Part B: Pulling a list of movies from MetaCritic

link_meta = 'https://www.metacritic.com/browse/movies/release-date/theaters/metascore' #link for page containing top recent movies ranked by their metascore

# The header used in this program was taken from https://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit-a-k-a-and-generate-user-agent
# The MetaCritic site appears to throw up errors if headers are not used

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#End of code from https://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit-a-k-a-and-generate-user-agent

response = requests.get(link_meta, headers = header)
time.sleep(2)

soup = BeautifulSoup(response.text, 'lxml')

movie_content = soup.find_all('td', class_ = 'clamp-summary-wrap')

meta_list = []

# Extracting the movie title and a respective metascore from each movie that passes the threshold
for i in movie_content:                
    movie_title = i.find('a', class_ ="title").text
    movie_score_tag = i.find('div' , class_ ="clamp-score-wrap")
    movie_score_tag_2 = movie_score_tag.find('a')
    movie_score = int(movie_score_tag_2.find('div', class_ = 'metascore_w large movie positive').text)
    
    if movie_score > 80:                
         meta_list.append(movie_title)
    else:
        continue
    
# Part C: Pulling a list of movies from RottenTomatoes 
    
link_rt = 'https://www.rottentomatoes.com/browse/movies_in_theaters/audience:upright~sort:critic_highest?page=2'
response = requests.get(link_rt)
time.sleep(2)

rt_list = []

soup            = BeautifulSoup(response.text, 'lxml')
movie_content = soup.find_all('div', slot ='caption')



# Extracting the movie title and a respective critic and audience score from each movie that passes the threshold

for i in movie_content:
    
    try:                                                       #Placing a try/except statement here to catch cases where there is a missing score
        
        audience_score = int(i.find('score-pairs')['audiencescore'])
        critic_score = int(i.find('score-pairs')['criticsscore'])
        movie_name = i.find('span', class_ = "p--small").text.strip()
        if audience_score >= 70 and critic_score >= 90:
            rt_list.append(movie_name)
        else:
            continue
        
    except:
        continue
    
# Part D: Pulling a list of movies from IMDB 

link_imdb = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'


response = requests.get(link_imdb)
time.sleep(2)

imdb_list = []

soup            = BeautifulSoup(response.text, 'lxml')
movie_content = soup.find_all('tr')

# Extracting the movie title and a respective imdb score from each movie that passes the threshold 

for movie in movie_content:
    try:
        
        movie_tag = movie.find('td', class_="titleColumn")
        movie_title = movie_tag.find('a').text
        rating_tag = movie.find('td', class_ = 'ratingColumn imdbRating')
        rating = float(rating_tag.find('strong').text)
        if rating > 7:
            imdb_list.append(movie_title)
        else:
            continue
    
    except:
        continue
    
# Part E: Printing out all the different lists and finding the common movies across lists

print('MetaCritic List \n', meta_list, '\n')
   

print('RottenTomatoes List \n', rt_list,'\n')

print('IMDB List \n',imdb_list, '\n')


def intersection(lst1, lst2, lst3): 
    return list(set(lst1) & set(lst2) & set(lst3))
 

common_movies = intersection(imdb_list, meta_list, rt_list)


# Part F: Creating a user-defined function to get the director's name of each film that makes it to the final list from MetaCritic

def movie_director(movies):
    
    dir_dict = {}
    for i in movies:
        dir_list = []
        string = i.lower().replace(' ', '-')
# The header used in this program was taken from https://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit-a-k-a-and-generate-user-agent
        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#End of code from https://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit-a-k-a-and-generate-user-agent
        meta_link = 'https://www.metacritic.com/movie/'
        meta_movie_link = meta_link + string
        response = requests.get(meta_movie_link, headers = user_agent)
        soup = BeautifulSoup(response.text, 'lxml')
        dir_tag = soup.find('div', class_ ="director")
        dir_names = dir_tag.find_all('a')
        for x in dir_names:
            dir_list.append(x.text)
        time.sleep(2)
        dir_dict[i] = dir_list
            
    return dir_dict

new_movie_dict = movie_director(common_movies)

print(new_movie_dict) # The value of each key is a list to account for cases where there is more than 1 director for a film

# Part F: Writing the data from the lists onto a text file:

with open('/Users/safwaan/Desktop/Semester 1/Python/movies_to_watch.text','w', encoding = 'utf-8') as file:
    file.write('Films To Watch' +'\n' + '\n')
    count = 1
    for i in new_movie_dict:
        
        file.write(str(count) + ')' + i +'\n')
        directors = ", ".join(new_movie_dict[i])
        file.write('Directed by: ' + directors +'\n' + '\n')
        count += 1
        