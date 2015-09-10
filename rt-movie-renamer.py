# deal with srt (subtitles) if moving files

import requests, os, bs4, re, shutil

SIMPLEREG = re.compile('(.*?)(?:[\[\(])*([0-9]{4})(.*)')
CRITICREG = re.compile('class="tMeterScore">([0-9]{2})')
VIDEO_FN_EXTS = set('3g2 3gp asf asx avi flv m4v mkv mov mp4 mpg rm swf vob wmv'.split())
DISALLOWED_CHARS = set('\/:*?"<>')

dud = found = 0

def check_url():
    url_base = 'http://www.rottentomatoes.com/m/' + underscore_title
    tomato_url = url_base + '_' + movie_year + '/'
    tomato_html = requests.get(tomato_url)
    if (tomato_html.status_code == 200):
        return tomato_html
    tomato_url = url_base + '/'
    tomato_html = requests.get(tomato_url)
    if (tomato_html.status_code == 200):
        return tomato_html
    tomato_url = url_base + '-' + movie_year + '/'
    tomato_html = requests.get(tomato_url)
    if (tomato_html.status_code == 200):
        return tomato_html
    return 
    

def get_rating(tomato_html):
    rating_critic = rating_audience = 'na'
    bs4_obj = bs4.BeautifulSoup(tomato_html.text, "html.parser")
    for x, row in enumerate(bs4_obj.find_all('span',attrs={"class" : "meter-value"})):
        if (x == 0):
            rating_critic = row.text
    for row in bs4_obj.find_all('div',attrs={"class" : "meter-value"}):
        rating_audience = row.text.strip()
    return rating_critic, rating_audience




current_dir = os.getcwd()

for subfoldername, subfolder, filenames in os.walk(current_dir): #loop all files in directory
    #head, tail = os.path.split(subfoldername)       #splits path from last folder name
    
    for filename in filenames:                  #loops through file names in directory
        file_ext = filename[filename.rfind(".")+1:]

        if file_ext in VIDEO_FN_EXTS:       #check if it's a video file
            movie = SIMPLEREG.search(filename)
            if movie and "sample" not in movie.group(3):
                movie_title = movie.group(1).replace('.',' ').strip().lower()
                underscore_title = movie_title.replace(' ','_')
                movie_year = movie.group(2)

                tomato_html = check_url()
                if tomato_html is None and "the" in movie_title:# and "the" in movie_title:
                    underscore_title = underscore_title.replace('the_','')
                    tomato_html = check_url()

                if (tomato_html):
                    rating_critic, rating_audience = get_rating(tomato_html)
                    print(movie_title.title() + " (" + movie_year + ") C:" + rating_critic + " A:" + rating_audience)
                    new_path =  current_dir + "\\" + movie_title.title() + " (" + movie_year + ") C:" + rating_critic + " A:" + rating_audience + "." + file_ext
                    found += 1
                    #print(movie_date, movie_title)
                else:
                    print('-',movie_title,movie_year,"- Valid URL Not Found")
                    new_path =  current_dir + "\\" + filename
                    dud += 1
                old_path = subfoldername+ "\\" + filename
                #print(old_path)
                #print(new_path)
                shutil.move(old_path, new_path)
                if subfoldername != current_dir:
                    #print('delete', )
                    shutil.rmtree(subfoldername)
                
                    
print('not found:',dud)              

input('\nPress Enter to close')
