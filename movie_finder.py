import requests
import textwrap
from random import shuffle
from bs4 import BeautifulSoup

URL = 'https://www.imdb.com/chart/top'
response = requests.get(URL)            # Request info from website
soup = BeautifulSoup(response.text, 'html.parser')



def find_movie():
    movie_list = soup.find(class_='lister-list').find_all('tr') # Returns objects containing each movie
    shuffle(movie_list)                                         # Shuffle list to choose random one

    chosen = False
    i = 0
    while not chosen and i <= 250:
        movie_title = movie_list[i].find(class_='titleColumn').find('a').get_text()
        choice = raw_input('Have you seen: ' + movie_title + ' ? Y/N or enter to exit ')

        if choice == 'y' or choice == 'Y':
            i += 1
            continue

        elif choice == 'n' or choice == 'N':
            print("1 - More Info\n2 - Next Movie\n3 - Previous Movie\n")
            menu_choice = raw_input()
            chosen, i = menu(int(menu_choice), movie_list[i], i)

        elif choice == '':
            break

        else:
            print("Please Enter 'Y' or 'N'")
            continue

    print("Enjoy your movie!")
    raw_input("\nPress Enter to exit...")


def menu(choice, mov, i):
    if choice == 1:
        more_info(mov)
        while True:
            found = raw_input('Is this the movie you will watch? (Y/n) ')
            if found == 'y' or found == 'Y':
                return True, i
            if found == 'n' or found == 'N':
                return False, i + 1

    elif choice == 2:
        return False, i + 1

    elif choice == 3:
        return False, i - 1

    else:
        print("Invalid Choice")


def more_info(mov):
    print("\n----------------------\n")
    title = mov.find(class_='titleColumn').find('a').get_text()
    title_code = mov.find(class_='watchlistColumn').find('div')['data-tconst']

    # Create new request to IMDB
    url = 'https://www.imdb.com/title/' + title_code + '/'
    resp = requests.get(url)
    movie_soup = BeautifulSoup(resp.text, 'html.parser')

    # Get info from request
    release = movie_soup.find('span', {'id':'titleYear'}).find('a').get_text()
    rating  = movie_soup.find('div', {'class':'ratingValue'}).get_text().replace('\n','')
    summary = movie_soup.find(class_='summary_text').get_text().replace('\n', '')


    # Cast
    cast_table = movie_soup.find('table', {'class':'cast_list'})
    cast = list()
    for star in cast_table.find_all('tr'):
        name = star.find('img')
        if name is not None:
            cast.append(name.get('title'))

    # Wrap the Summary and cast to paragraph format
    summary = textwrap.dedent(summary).lstrip()
    cast_str = ', '.join(cast)
    cast_str = textwrap.dedent(cast_str)

    print("Movie:       %s" % (title) )
    print("Released:    %s" % (release) )
    print("Rating:      %s" % (rating) )
    print("Summary:     %s" % (textwrap.fill(summary,
                                      initial_indent='',
                                      subsequent_indent=' ' * 13,
                                      width=70,
                                      )) )
    print("Cast:        %s" % (textwrap.fill(cast_str,
                                       initial_indent='',
                                       subsequent_indent=' ' * 13,
                                       width = 70
                                       )) )
    print("\n----------------------\n")



if __name__ == "__main__":
    find_movie()
