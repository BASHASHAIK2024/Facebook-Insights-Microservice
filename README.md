SDE Intern Assignment - Deepsolv

Guidelines:
You can use Python for implementing the solution. You may choose FastAPI/Django/Flask or any other Server framework for creating a Web Server.
You would need to use a database (MySQL/ MongoDB) for persistent storage.
Your APIs should be well tested and should be in a demo-able state. You will be asked to run these APIs after this assignment.
Use of AI or any kind of plagiarism is STRICTLY PROHIBITED, if detected by our systems, your Application will be straightaway rejected automatically.
The focus should be on developing a robust, scalable, and maintainable backend system. 
Candidates should adhere to best practices in software development, including OOP principles, SOLID design patterns, clean code, and RESTful API design.
The requirements are divided into two sections:
Mandatory Section: You must complete ALL mandatory requirements to qualify.
Bonus Section: Attempt the bonus requirements only after completing the mandatory section. Bonus features will earn you extra points and provide an edge over other candidates.

Problem statement: Facebook Insights Microservice

Your task is to design and implement a Facebook Insights service, which is basically an application to check insights of a given username of a Facebook Page, where username means the last part we see in the Page’s URL. For example: Boat company’s page’s URL is -> https://www.facebook.com/boat.lifestyle, so boat.lifestyle is the page username you'll get.

Your Application will be able to fetch details of a given page username (either by scraping or using API, we recommend scraping to save your development time, if not familiar with Facebook’s APIs), store the required information into a Database, with separate schemas for Page, SocialMediaUser, Posts, etc. And we, as the operator of the application, can get the details of any Facebook Page, from the DB.


MANDATORY requirements:
Have a Scraper service in your application, that scrapes any given username from Facebook (you can use any existing scraping libraries available), for the following details of a Page. For example:
Basic details of the Page
Page Name
Page url
id (the facebook platform specific id)
Profile_pic
Email ID
Website
Page Category
Total Followers, Total Likes
Page Creation Date
Any other fields you find useful or a good-to-have
Posts of the Page (you can have top 25-40 posts stored since, some pages might have a large number of posts)
Comments on the Posts
Followers (if available for a page) Following (if available - profile pic, name, id etc.) stored in DB
Storing the Scraped data into any DB, with relationships maintained between entities.
Expose a GET endpoint to get details of a given Page username from the db (if a page is not present in the DB, then only try fetching it in realtime via scraping/API), with the some filters like:
Find by follower count range, for eg. Find the pages between 20k-40k Followers, find by name of the page (similar search), find by category
Get list of the following/followers of a given Page
Get recent 10-15 Posts of the Page.
Have Pagination in GET requests, wherever applicable.
Make Sure, to create a Postman Collection of the included APIs, that you can directly share or present.

BONUS Requirements:
Provide AI Summary on a Page (using ChatGPT API, or any other LLMs) from the followers, like counts, type of page, about the page, type of followers.
Use Asynchronous programming for API calls, database operations, and any I/O-bound tasks.
Use a Storage Server like GCS, S3 etc. for the profile pictures or the Posts you’re fetching, to make a clone of them in the server, and use that link as a mainstream link.
Implement Caching for the data, with TTL of for eg. 5 minutes for us to test.

Deliverables
A public github repository Link.
Documentation attached as README.md in the repo for easy understanding of your code.
Postman Collection JSON (Optional)
Deployed server link (Optional)
Demo Video (optional)

Submit your assignment on the Google Form - https://forms.gle/D6gQf9mnTJnDiec57 
