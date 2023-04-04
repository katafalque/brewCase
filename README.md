# brewCase

## How to run
- Clone repo to your local folder
- build docker file with command
> docker build .
- Run docker image with command
> docker run -t -i $image-id
- image id can be seen by command 
> docker images
 
  
 ## Missing Stories
 - Testing
 - Async programming
  
 ## Thoughts
 - Could've done this a lot better but unfortunately i got sick during weekend 
 and this was the result of todays work.
 - Couldn't find 2 proper apis so that i decided scraping amazon by using selenium.
 However, it turned out selenium doesn't support async programming so that i decided
 to skip the story since i was already late and didn't have much time.
 - Python supports async programming since python 3.5 and has a module for that named
 asyncio. I was planning to use that to send async requests to apis. Execution time 
 could've been a lot better this way.
- Created a ScraperFactory class to be able to both control implemented scrappers and 
add new one in future. I am aware of that it is not exactly like it should be because
of selenium. Since sending request to google books api and scraping amazon using selenium
have different logic, I couldn't create a one scraper interface and make others derive from that.
> Was planing to add both scrapers to list in ScraperFactory class and call their get_book_data methods when their turn come up.
> That way when a new scraper is added, adding the new scraper to that list would be enough.

- I hope these wont be seen as excuses. Thank you for giving me a chance.
