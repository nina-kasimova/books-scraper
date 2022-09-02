# books-scraper

## How to run ##
paste the books list url to the first url line

## What it does ##
The script will scrape the provided list of books and save two copies of json files:
- one named after the list into a folder with all the data for future use (irrelevant for the app)
- one with the constant name will be saved to a folder for the use of json server

There are no changes to be made in the UI. The path for the json is already provided in `server.ts` file.

Rerun the server with `npm run server` while in `books-ui` folder to use the new data
