# Grab Music from Youtube

Grabs music from youtube and adds it to Apple Music's local library.

## External Dependencies

- [`ffmpeg`](https://ffmpeg.org)

    Use your favorite package manager to install it

## Google Custom Search API

For now, to be able to use this project, you need to enable Google Custom Search API, generate API key credentials and set a project:

-   Visit [https://console.developers.google.com](https://console.developers.google.com) and create a project.

-   Visit [https://console.developers.google.com/apis/library/customsearch.googleapis.com](https://console.developers.google.com/apis/library/customsearch.googleapis.com) and enable "Custom Search API" for your project.

-   Visit [https://console.developers.google.com/apis/credentials](https://console.developers.google.com/apis/credentials) and generate API key credentials for your project.

-   Visit [https://cse.google.com/cse/all](https://cse.google.com/cse/all) and in the web form where you create/edit your custom search engine enable "Image search" option and for "Sites to search" option select "Search the entire web but emphasize included sites".  

After setting up your Google developers account and project you should have been provided with developers API key and project CX.
Then, put your credentials in `google-api.json`

## TODO:

- [ ] Create a CLI
- [ ] Work on other artwork sources

## Current Usage

```
python3 main.py [url]
```