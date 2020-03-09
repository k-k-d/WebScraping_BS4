# imports

from bs4 import BeautifulSoup;
import requests;
import csv;
import json;

# initialising fields

names = []
areas = []
types = []
ratings = []
votes = []
agent = {"User-Agent":"Mozilla/5.0"}
url = "https://www.zomato.com/bangalore/south-bangalore-restaurants?page="

# iterate through 6 pages by giving different page url parameters with the get request

for i in [1, 2, 3, 4, 5, 6]:

    res = requests.get(url + str(i), headers = agent)
    soup = BeautifulSoup(res.text, 'html.parser')

    # name tags all have the attribute dtata-result-type as ResCard_Name

    name_tags = soup.find_all(name = 'a', attrs = {"data-result-type" : "ResCard_Name"})
    for name_tag in name_tags:
        names.append(name_tag.text.strip())

    # area and page numbers are contained in <b><\b> tag and page numbers are removed in the end

    area_tags = soup.find_all(name = 'b')
    del area_tags[-1]
    del area_tags[-1]
    for area_tag in area_tags:
        areas.append(area_tag.text.strip())

    # type is within a child of the div tag of the col-s-12 class but sometimes it is not specified and is taken care of

    type_tags = soup.find_all(name = 'div', attrs = {'class' : "col-s-12"})
    for type_tag in type_tags:
        if(type_tag.find(name = 'div', attrs = {"class" :  "res-snippet-small-establishment"})):
            word = ''
            for tag in type_tag.find_all(name = 'a'):
                word += (tag.text.strip())
                word += ', '
            word = word[: -1]
            word = word[: -1]
            types.append(word)
        else:
            types.append("Not Specified")

    # rating is pretty straightforward

    rating_tags = soup.find_all(name = 'div', attrs = {'class' : 'rating-popup'})
    for rating_tag in rating_tags:
        ratings.append(rating_tag.text.strip())

    # span is in the span within a div tag whose class is search_result_string

    votes_ = []
    vote_tags = soup.find_all(name = 'div', attrs = {'class' : 'search_result_rating'})
    for vote_tag in vote_tags:
        if(vote_tag.find(name = 'span')):
            votes_.append(vote_tag.find(name = 'span').text.strip())
        else:
            votes_.append("Nil Votes")
    for vote in votes_:
        vote = vote[:-6]
        votes.append(vote)

# limit number of restaurants to 80

names = names[:80]
areas = areas[:80]
types = types[:80]
ratings = ratings[:80]
votes = votes[:80]

# writing to csv

with open('restaurants.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['restaurant_id', 'name', 'area', 'restaurant_type', 'rating', 'number_of_votes'])
    for i in range(80):
        filewriter.writerow([str(i + 1), names[i], areas[i], types[i], ratings[i], votes[i]])

# reading from the csv and writing to json
# easier to code than manipulating arrays to get a json directly

json_data = {}

with open('restaurants.csv', 'r') as csvfile:
    filereader = csv.DictReader(csvfile)
    for row in filereader:
        json_data[row['restaurant_id']] = row

with open('restaurants.json', 'w') as jsonfile:
    jsonfile.write(json.dumps(json_data, indent = 4))