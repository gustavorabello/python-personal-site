## =================================================================== ##
#  this is file setup.py, created at 30-Oct-2011                #
#  maintained by Gustavo Rabello dos Anjos                              #
#  e-mail: gustavo.rabello@gmail.com                                    #
## =================================================================== ##

import os,time,fnmatch,re,shutil,socket
from datetime import datetime, timedelta
from subprocess import call
#from PIL import Image

def populateImageDB():

 dirname = 'static/figures/'

 print ("")
 print (" ************************************* ")
 print (" *  Adding entries to the database:  * ")
 print ("")

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
  
   print ("  " + filename + " " + title + " " + dim + " " + date + " " + text)

 print ("")
 print (" *  Entries in the database ADDED!   * ")
 print (" ************************************* ")
 print ("")

def populateRecipeDB():

 dirname = 'static/recipes/'

 print ("")
 print (" ************************************* ")
 print (" *  Adding entries to the database:  * ")
 print ("")

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
  
   print ("  " + obj + " " + filename + " " + date + " " + infoname)

 print ("")
 print (" *  Entries in the database ADDED!   * ")
 print (" ************************************* ")
 print ("")


def populateSaleDB():

 dirname = 'static/sales/'

 print ("")
 print (" ************************************* ")
 print (" *  Adding entries to the database:  * ")
 print ("")

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

   print ("   " + filename + " " + info + " " + cond \
         + " " + link + " " + original + " " + price)

 print ("")
 print (" *  Entries in the database ADDED!   * ")
 print (" ************************************* ")
 print ("")

def populateVideoDB():
 import youtube

def populateMusicDB():

 dirname = 'content/media/html/tabs/'

 print ("")
 print (" *************************************** ")
 print (" *   Adding entries to music folder:   * ")
 print ("")

 count = 1
 # loop all artist's folder
 for artistname in sorted(os.listdir(dirname)):
  # loop inside each folder
  if os.path.isdir(os.path.join(dirname, artistname)):
   for infile in sorted(os.listdir(dirname+artistname)):
    if fnmatch.fnmatch(infile, '*.html'): 
     # spliting base name and extension
     basename = os.path.splitext(infile)[0]
     #print (dirname+artistname+'/'+infile)
     a = datetime.now() - timedelta(seconds=count)
     timestamp = time.strftime(str(a))
     
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
     file.write("created: !!timestamp '" + timestamp + "'\n")
     file.write("---\n")
     file.close()
     count = count + 1
 
 print ("")
 print (" *  Total number of musics: " + str(count) + "        * ")
 print (" *  Finished: music folder completed!  * ")
 print (" *************************************** ")
 print ("")

def genSite():
 # removing local directory paginas

 directory = './gustavorabello.github.io'

 if os.path.exists(directory):
  print ("")
  print ("Removing contents in " + directory)
  for dirs in os.listdir(directory):
   if os.path.isdir(directory + '/' + dirs) and dirs != '.git':
    shutil.rmtree(directory + '/' + dirs)
    print ("Deleting directory " + dirs)
   else: # it is a file
    if dirs != '.gitignore' and dirs != '.git':
     print ("Deleting file " + dirs)
     os.remove(directory + '/' + dirs)
 else:
  print ("")
  print ("Creating " + directory)
  os.makedirs(directory)

 # generating webpage into paginas folder
 print ("")
 print ("Generating website at " + directory)
 print ("")
 call(['hyde','gen'])

def updatePage():
 # updating web page in github

 directory = './gustavorabello.github.io'
 os.chdir(directory)

 print ("")
 print ("Uploading to github: " + directory)
 print ("")
 # verifying if directory is up to date
 call(['git','pull'])
 # adding new files
 call(['git','add','.'])
 # commiting to github
 call(['git','commit','-a','-m','"updating site."'])
 print ("")
 print (" ---> All done! Website ready at github.")
 print ("")

def main():
 #populateSaleDB()
 #populateRecipeDB()
 populateMusicDB()
 #populateImageDB()
 populateVideoDB()
 genSite()
 updatePage()


 # completed build script
 print (u"All done running build.py.")


if __name__ == "__main__":
    main()
