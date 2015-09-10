import requests, os, bs4, re, shutil

MOVE_FILES = True   # True/False Move files to base directory & delete old sub directories.
TEST_MODE = True   # True/False Test mode will print old/new filenames instead of renaming and moving the files.

file_name_regex = re.compile('(.*?)(?:[\[\(])*([0-9]{4})(.*)')
video_extensions = set('3g2 3gp asf asx avi flv m4v mkv mov mp4 mpg rm swf vob wmv'.split())

base_dir = os.getcwd()
not_found = found = 0

def check_url():
    """ Tests for a url match
    Rotten Tomatoes URLs can be formatted a few different ways
    /m/movie_title or /m/movie_title_year or /m/movie_title-year
    """
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
    """ Get's the Critic and Audience Ratings from the HTML using Beatiful soup
    """
    rating_critic = rating_audience = 'na'
    bs4_obj = bs4.BeautifulSoup(tomato_html.text, "html.parser")
    for x, row in enumerate(bs4_obj.find_all('span',attrs={"class" : "meter-value"})):
        if (x == 0):
            rating_critic = row.text
    for row in bs4_obj.find_all('div',attrs={"class" : "meter-value"}):
        rating_audience = row.text.strip()
    return rating_critic, rating_audience





for subfoldername, subfolder, filenames in os.walk(base_dir): 
    for filename in filenames:                  
        file_extention = filename[filename.rfind(".")+1:]
        if file_extention in video_extensions:      
            movie = file_name_regex.search(filename)
            if movie and "sample" not in movie.group(3):        #ignores video sample files
                movie_title = movie.group(1).replace('.',' ').strip().lower()
                underscore_title = movie_title.replace(' ','_')
                movie_year = movie.group(2)
                tomato_html = check_url()
                if tomato_html is None and "the" in movie_title:        # If RT URL has not been found, and the title contains a 'the', this strips the 'the' and tries again
                    underscore_title = underscore_title.replace('the_','')
                    tomato_html = check_url()

                if (tomato_html):
                    rating_critic, rating_audience = get_rating(tomato_html)
                    new_name =  "\\" + movie_title.title() + " (" + movie_year + ") C-" + rating_critic + " A-" + rating_audience + "." + file_extention
                    print(new_name)
                    found += 1
                else:
                    print('-',movie_title,movie_year,"- Valid URL Not Found")
                    if MOVE_FILES:
                        new_path =  base_dir + "\\" + filename
                    not_found += 1

                old_path = subfoldername+ "\\" + filename
                if MOVE_FILES:
                    new_path = base_dir + new_name
                elif not MOVE_FILES:
                    new_path = subfoldername + new_name
                if TEST_MODE:
                    print('old path:',old_path)
                    print('new path:',new_path)
                elif not TEST_MODE:
                    shutil.move(old_path, new_path)
                if subfoldername != base_dir and MOVE_FILES:
                    if TEST_MODE:
                        print('delete:  ', subfoldername)
                    elif not TEST_MODE:
                        shutil.rmtree(subfoldername)
                
print('')                  
print('found:',found,'not found:',not_found)
if TEST_MODE:
    print('Test Complete.  Change TEST_MODE variable to False to run the program live!')
input('\nPress Enter to close')
