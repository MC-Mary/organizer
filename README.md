![status badge](https://github.com/MC-Mary/organizer/blob/main/.github/workflows/main.yml/actions/workflows/style_and_testing.yml/badge.svg)
[![codecov](https://app.codecov.io/gh/MC-Mary/organizer/branch/main/graph/badge.svg)](https://app.codecov.io/gh/MC-Mary/organizer)

Thank you for your interest in my project. Below you can find some information about my app.

# MEMO for YOU
These app named "MEMO for YOU" is designed to help the parents to manage information about the child on everey step of his life.
The assumption of the project is to save all important and less important data here,
so that in the future you can easily and quickly find any information about the child's development.
However, user decides what information he wants to save in the application and which will be available for him later. 

![Home Page](niunius/static/niunius/readme/readme_home.png)

django_app_for_off_road_club/niunius/static/niunius/readme/readme_blog.png 

## Start

To start exploring the project:
1. clone this repository
2. create the virtual environment and install requirements`pip install -r requirements.txt`
3. configure a database - in the project directory you need to create the file named ***local_settings.py*** and add there DATABASES with details of the database connection.
   These details will be imported by Django as in the file `setting.py` the following code is included:
   ```python
    try:
        from my_django_project.local_settings import *
    except ImportError:
        pass
    ```
4. run the command `python manage.py migrate`
5. load initial data to fill your database - use the command `python manage.py loaddata */fixtures/*.json`
6. create a superuser to access the admin site: ` python manage.py createsuperuser`
7. open additional terminal window and run `python -m smtpd -n -c DebuggingServer localhost:1025` - this is required by email settings, in this terminal you will see sent messages
8. that's all, run `python manage.py runserver` and enjoy the app :-)

As for the app content, besides the home page already mentioned and shown, there are few more pages. These are:
about page, blog page, shop page, car service station page and contact page. A short description of each follows...

### About

This is one of articles from the blog, a specific one - with information about the club (like history, members etc.)

### Blog 

![Blog Page](niunius/static/niunius/readme/readme_blog.png)

The blog is for articles, accessible to all users. Everyone can give a thumb up or thumb down, and see comments. 
Extra functionalities as adding and editing articles are reserved for logged-in users.

### Shop

![Shop Page](niunius/static/niunius/readme/readme_shop.png)

The shop is for car parts. You can search by car models or by categories, or type whatever you are looking for in the search box.
Products are assigned to car models and to categories.
All users can make shopping, why not. You do not have to create an account on the website as this may discourage potential clients.
However, placing orders as a logged-in user allow you to check the orders' history on your profile page.

### Car Service Station

Users may review car services offer and book a visit. 

### Contact

The contact page with the address and the map. Additionally, user can send a message to the site/club owner.

## The end

Thank you one more time for your interest.
If you find anything should be added/amended/deleted in this project, you are very welcome to create pull requests.
