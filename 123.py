import os
import shutil
os.chdir(os.getcwd()+"/static/files")
path = str(os.getcwd())+"/abraxane"
shutil.make_archive("download", 'zip', path)
os.chdir("C:/Users/daddela/Pictures/wpvuln")
