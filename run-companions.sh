# ==========================================================================
# The following command logs you into the public account for the QRG 
# Docker registry.  If you have your own account, you'll want to use that
# instead.  Or if you're already signed in using your own account, just 
# comment out the line below.

#docker login gavotte.cs.northwestern.edu:30500 -u cs371 -p TrHhpBgkw59x3q7z


# ==========================================================================
# Below you'll find three sections, each with a different way to run the
# Companions container.  Uncomment only the section you want to use
# ==========================================================================


# ==========================================================================
# SECTION #1
# 
# If you just want to run Companions and don't want to map any of your 
# computer's local directories into the container, uncomment this section
# and comment out the other sections.
#
# The Companions Web UI will be exposed at http://<host>:9100/smgr.html.
# E.g.: http://localhost:9100/smgr.html if you're accessing it from the
# same computer as the one running the container.

# docker run -it --rm -p 9100:9100 --name companions \
#   gavotte.cs.northwestern.edu:30500/companions/companions:latest


# ==========================================================================
# SECTION #2
# 
# To run Companions with various directories mapped to directories on your 
# local computer, uncomment this section and comment out the others.
# 
# If you want to replace the default knowledge base with one of your own,
# place the KB files in the directory specified by kb_path.  If this
# directory is empty, the default KB will be used.  If there are any files
# in this directory, Companions will use those as the KB so be sure it's
# a valid KB.
# 
# Edit the variables below to the directories you wish to use.
# 
# Directory descriptions:
# 
# LOG_PATH: Companions agents log errors and other pertinent 
#   information to this directory.  If you don't map your own directory
#   Companions will write logs internal to the container.  This data is 
#   not persistent and will be lost when the container is stopped.
#   
# PATCHES_PATH: Lisp files in this directory will be automatically loaded
#   when Companions starts.  If you do not map your own directory, no
#   patches will be loaded.
# 
# KB_PATH: Companions expects the knowledge base to be in this directory.
#   
#   If you don't map your own directory, then Companions will use the 
#   NextKB knowledge base built into the container.  Changes to this KB
#   will not be persistent and will be lost when the container is
#   stopped.
#   
#   If you map your own directory but it's empty, then Companions will 
#   copy the KB built into the container to your directory and will use 
#   the KB copied to your directory.  
#   
#   If you map your own directory and it contains any files Companions 
#   will try to use those files as the knowledge base.  So make sure 
#   those files are a valid knowledge base.
# 
# SKETCH_PATH: If you map your own directory, sketches in this directory
#   will be available to WebSketch.  If you don't use your own directory, 
#   WebSketch will use a set of sample sketches built into the container.
#   Note that those sample sketches will also be automatically copied into 
#   any directory you map.
# 
# KIOSK_QUESTIONS_PATH: Kiosk training questions will be loaded from this
#   directory.  If you don't map your own directory, the Kiosk agent will
#   use a set of training questions built into the container.
# 
# PYTHONIAN_CODE: Pythonian code will be loaded from this directory.  If
#   you don't map your own directory, Companions will use a version of the
#   Pythonian code built into the container.

LOG_PATH=~/companions/logs
PATCHES_PATH=~/companions/patches
FLAT_FILES_PATH=~/companions/flat-files
KB_PATH=~/companions/kb
SKETCH_PATH=~/companions/sketches
KIOSK_QUESTIONS_PATH=~/companions/kiosk-questions
PYTHONIAN_CODE=~/companions/pythonian

docker run -it --rm -p 9100:9100 --name companions \
  -v $LOG_PATH:/app/companions/externalizable-vols/logs \
  -v $PATCHES_PATH:/app/companions/externalizable-vols/patches \
  -v $FLAT_FILES_PATH:/app/companions/externalizable-vols/flat-files \
  -v $KB_PATH:/app/companions/externalizable-vols/kb \
  -v $SKETCH_PATH:/app/companions/user-data/samples/websketch \
  -v $KIOSK_QUESTIONS_PATH:/app/companions/externalizable-vols/kiosk-questions \
  -v $PYTHONIAN_CODE:/code \
  gavotte.cs.northwestern.edu:30500/companions/companions:latest


# ==========================================================================
# SECTION #3
# 
# If you want to use Bash inside the container instead of running Companions
# uncomment this section and comment out the others.  This is only useful 
# for debugging.

# docker run -it --entrypoint bash -p 9100:9100 \
#   gavotte.cs.northwestern.edu:30500/companions/companions:latest


# ==========================================================================
# End of File
