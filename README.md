# brewCase

## How to run Docker
- Clone repo to your local folder
- build docker file with command
> docker build -t brew .
- Run docker image with command
> docker run -i brew

## How to run Local
-pip install -r requirements.txt
-python cli.py
> python 3.11 required.
 
  
 ## Missing Stories (Updated)
 - Testing (Added unit test for Book class.)
 - Async programming (Removed google and amazon scrapers and added babil.com and dr.com.tr scrapers and now they are async.)
  
## Bugs.
- Prints false to the csv if book is not found.
