Hello and welcome to my CFC Insight Technical Challenge.

I have programmed a word scraper that scrapes the content off the cfcunderwriting website and completes
the following tasks:

Writes a list of *all externally loaded resources* (e.g. images/scripts/fonts not hosted
on cfcunderwriting.com) to a JSON output file.
Enumerates the page's hyperlinks and identifies the location of the "Privacy Policy"
page.
Uses the privacy policy URL identified and scrapes the pages content.
Produce a case-insentitive word frequency count for all of the visible text on the page.
Your frequency count should also be written to a JSON output file.

For the external images, uncomment the section if you would like to also pull out external svg graphics.
For the fonts, external css files were included because of the fact that css files contains fonts themselves.

Images and scripts tags are outputted with their tag entirely while fonts/css is just the url.
In the json file its just urls mainly (except images where it states it is a background image).

externalresources.json has sections defined already, therefore keep them there.
wordcount.json can stay blank.

To install the required libraries run 'pip install -r requirements.txt'.
To run the code write 'python main.py'.

