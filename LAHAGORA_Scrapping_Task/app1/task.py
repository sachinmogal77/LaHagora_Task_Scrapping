# scraping
from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery import app, shared_task
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import lxml
from google_play_scraper import app
from celery import shared_task

from app1.models import Playstore

# logging
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


# save function
@shared_task(serializer='json')
def save_function(package_list):
    """Save packages to the database.
    Saves packages to the database if they do not already exist.
    Parameters:
        packages_list (json, str): A JSON list of packages objects.
    Returns:
        Playstore (class Playstore): Package objects for each unique package.
    """
    source = package_list[0]['source']
    new_count = 0

    error = True
    try: 
        latest_package = Playstore.objects.filter(source=source).order_by('-id')[0]
        print(latest_package.published)
        print('var TestTest: ', latest_package, 'type: ', type(latest_package))
    except Exception as e:
        print('Exception at latest_package: ')
        print(e)
        error = False
        pass
    finally:
        # if the latest_package has an index out of range (nothing in model) it will fail
        
        # this catches failure so it passes the first if statement
        
        if error is not True:
            latest_package = None

    for package in package_list:

        # latest_article is None signifies empty DB
        if latest_package is None:
            try:
                Playstore.objects.create(
                    title = package['title'],
                    description = package['description'],
                    published = package['summary'],
                    created_at = package['created_at'],
                    updated_at=package['updated_at'],
                    reviews = package['reviews'],
                    ratings = package['ratings'],                 
                    histogram = package['histogram']

                )
                new_count += 1
            except Exception as e:
                print('failed at latest_package is none')
                print(e)
                break
        
       
        else:
            return print('playstore scraping failed')

    logger.info(f'New Packages: {new_count} packages(s) added.')
    return print('finished')


# scraping function
@shared_task
def playstore_scrapping():
    package_list = []
    try:
        print('Starting the scraping tool')
        # execute my request, parse the data using XML
        # parser in BS4
        r = requests.get('https://play.google.com/store/games?hl=en&gl=US')
        soup = BeautifulSoup(r.content, features='xml')
        # select only the "items" I want from the data
        packages = soup.findAll('com.snakeattack.game')
    
        # for each "item" I want, parse it into a list
        for a in packages:
            title = a.find('title').text
            description = a.find('description').text
            reviews = a.find('reviews').txt
            ratings = a.find('ratings').txt
            histogram = a.find('histogram').txt
            created_at = a.find('created_at').txt
            updated_at = a.find('updated_at').txt

            published_wrong = a.find('pubDate').text
            published = datetime.strptime(published_wrong, '%a, %d %b %Y %H:%M:%S %z')
            # print(published, published_wrong) # checking correct date format
            # create an "packages" object with the data
            # from each "item"
            packages = {
                'title': title,
                'description': description,
                'reviews' : reviews,
                'ratings' : ratings,
                'histogram': histogram,
                'created_at':created_at,
                'updated_at':updated_at,
                'published': published,
                
            }
            # append my "package_list" with each "packages" object
            package_list.append(packages)
            print('Finished scraping the packages')
    
            return save_function(package_list)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)

result = app(
    'com.snakeattack.game', 
    lang='en',      # defaults to 'en'
    country='us'    # defaults to 'us'
)
print(result)