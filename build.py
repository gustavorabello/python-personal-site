## =================================================================== ##
#  this is file setup.py, created at 30-Oct-2011                #
#  maintained by Gustavo Rabello dos Anjos                              #
#  e-mail: gustavo.rabello@gmail.com                                    #
## =================================================================== ##

import os,fnmatch,re,shutil,socket
from subprocess import call
from PIL import Image

def populateImageDB():

 dirname = 'static/figures/'

 print ""
 print " ************************************* "
 print " *  Adding entries to the database:  * "
 print ""

 # loop all files
 for arq in os.listdir(dirname):

  if fnmatch.fnmatch(arq, '*.txt'): 
   # spliting base name and extension
   basename = os.path.splitext(arq)[0]
   filename = basename + '.png'
     
   fopen = open(dirname+arq,'r')
   line = fopen.readlines()

   title = line[0].split('\n')[0]
   dim   = line[2].split('\n')[0]
   date  = line[4].split('\n')[0]
   text  = line[6].split('\n')[0]
   
   # saving in the database
   img = Image(filename=filename,
               title=title, 
               dimension=dim, 
               date=date,
               text=text)
  
   print "  " + filename + " " + title + " " + dim + " " + date + " " + text

 print ""
 print " *  Entries in the database ADDED:   * "
 print " ************************************* "
 print ""

def populateRecipeDB():

 dirname = 'static/recipes/'

 print ""
 print " ************************************* "
 print " *  Adding entries to the database:  * "
 print ""

 # loop all files
 for arq in os.listdir(dirname):

  if fnmatch.fnmatch(arq, '*.txt'): 
   # spliting base name and extension
   basename = os.path.splitext(arq)[0]
   filename = basename + '.png'
   infoname = basename + '.html'
     
   fopen = open(dirname+arq,'r')
   line = fopen.readlines()

   obj = line[0].split('\n')[0]
   date = line[2].split('\n')[0]
   info = line[4].split('\n')[0]

   # saving in the database
   rec = Recipe(obj=obj,
                image=filename,
                date=date,
                info=infoname)
  
   print "  " + obj + " " + filename + " " + date + " " + infoname

 print ""
 print " *  Entries in the database ADDED:   * "
 print " ************************************* "
 print ""


def populateSaleDB():

 dirname = 'static/sales/'

 print ""
 print " ************************************* "
 print " *  Adding entries to the database:  * "
 print ""

 # loop all files
 for arq in os.listdir(dirname):

  if fnmatch.fnmatch(arq, '*.txt'): 
   # spliting base name and extension
   basename = os.path.splitext(arq)[0]
   filename = basename + '.png'
     
   fopen = open(dirname+arq,'r')
   line = fopen.readlines()

   obj = line[0].split('\n')[0]
   info = line[2].split('\n')[0]
   cond = line[4].split('\n')[0]
   link = line[6].split('\n')[0]
   original = line[8].split('\n')[0]
   price = line[10].split('\n')[0]

   print "   " + filename + " " + info + " " + cond \
         + " " + link + " " + original + " " + price

 print ""
 print " *  Entries in the database ADDED:   * "
 print " ************************************* "
 print ""

def populateVideoDB():
 import gdata.youtube
 import gdata.youtube.service

 print ""
 print " ************************************* "
 print " *  Adding entries to the database:  * "
 print ""

 #
 # Add if condition to check internet connection!
 #
 count = 1
 yt_service = gdata.youtube.service.YouTubeService()
 pl_id = 'A5C4DB7CAE7AF003'
 playlist_video_feed = yt_service.GetYouTubePlaylistVideoFeed(playlist_id=pl_id)
 for entry in playlist_video_feed.entry:
  title =  entry.media.title.text
  youtube = 'http://www.youtube.com/embed/%s' % entry.media.player.url[32:43]
  description = entry.media.description.text
  date = entry.published.text[:10] + " " + entry.published.text[11:19] 
  #keywords = entry.media.keywords.text # not working
  duration = entry.media.duration.seconds

  savedir = "content/videos/" 

  file = open(savedir + str(count) + ".html",'w')
  file.write("---\n")
  file.write("title: " + title + "\n")
  file.write("duration: " + duration + "\n")
  file.write("created: !!timestamp '" + date + "'\n")
  file.write("tags: \n")
  file.write("    - two-phase \n")
  file.write("---\n")
  file.write("\n")
  file.write("{% mark video -%}\n")
  file.write("\n")
  file.write("<iframe src=\"" + youtube + "\" frameborder=\"1\" allowfullscreen></iframe> \n")
  file.write("\n")
  file.write("{% endmark %}\n")
  file.write("\n")
  file.write("\n")
  file.write("{% mark excerpt -%}\n")
  file.write(description[0:320])
  file.write("\n")
  file.write("{% endmark %}\n")
  file.write(description[320:])
  file.write("\n")
  file.close()
  count = count + 1
    
 print ""
 print " *  Total number of videos: " + str(count) + "        * "
 print " *  Entries in the database ADDED:   * "
 print " ************************************* "
 print ""

def populateMusicDB():

 dirname = 'content/media/html/tabs/'

 print ""
 print " *************************************** "
 print " *   Adding entries to music folder:   * "
 print ""

 count = 1
 # loop all artist's folder
 for artistname in os.listdir(dirname):
  # loop inside each folder
  if os.path.isdir(os.path.join(dirname, artistname)):
   for infile in os.listdir(dirname+artistname):
    if fnmatch.fnmatch(infile, '*.html'): 
     # spliting base name and extension
     basename = os.path.splitext(infile)[0]
     
     # HTML files should be formatted as follow:
     # oCarderno.html,
     # maisQueNada.html,
     # escravoDaAlegria.html etc.
     #
     # spliting basename in several words, ex:
     # myNameIsGustavo ---> my Name Is Gustavo
     splitsongname = re.sub(r'(?<=.)([A-Z])', r' \1', basename).split()

     songname=''
     for name in splitsongname: 
     # function: my Name Is Gustavo --> My Name Is Gustavo
      songname += name.title() + " "
 
     splitartistname = re.sub(r'(?<=.)([A-Z])', r' \1', artistname).split()
 
     artist=''
     for name in splitartistname: 
      # function: toquinho E Vinicius --> Toquinho E Vinicius
      artist += name.title() + " "
 
     savedir = "content/musics/" + artistname + "/"
     if not os.path.exists(savedir):
      os.makedirs(savedir)

     file = open(savedir + basename + ".html",'w')
     file.write("---\n")
     file.write("artist: " + artist + "\n")
     file.write("title: " + songname + "\n")
     file.write("type: music" + "\n")
     file.write("dir: html/tabs/" + artistname + "/" + basename + ".html\n")
     file.write("---\n")
     file.close()
     count = count + 1
 
 print ""
 print " *  Total number of musics: " + str(count) + "        * "
 print " *  Finished: music folder completed:  * "
 print " *************************************** "
 print ""

def genSite():
 # removing local directory paginas

 if socket.gethostname() == 'highland':
  directory = os.path.expanduser("~") + '/gustavo.rabello.org'
 else:
  directory = './deploy'

 if os.path.exists(directory):
  print ""
  print "Removing " + directory
  shutil.rmtree(directory)
  print ""
  print "Creating " + directory
  os.makedirs(directory)
 else:
  print ""
  print "Creating " + directory
  os.makedirs(directory)

 # generating webpage into paginas folder
 print ""
 print "Generating website at " + directory
 print ""
 call(['hyde','gen'])

def main():
 #populateSaleDB()
 #populateRecipeDB()
 populateMusicDB()
 #populateImageDB()
 #populateVideoDB()
 genSite()


 # completed build script
 print u"All done running build.py."


if __name__ == "__main__":
    main()
