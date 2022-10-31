# Weather
#### Description:

# CS50 Final Project - Weather

In this weather web app, you can register, login, and logout. In the main part
you can add multiple cities and it will show you the current temperature, what it
feels like, humidity, icon, and wind speed of your added cities. Your added
cities will be saved in your account. You can also remove cities that you have
added to your list. The session will remember you until you logout. That's all.

Technologies used:

- HTML
- CSS
- JavaScript
- Flask
- sqlite3
- OpenWeather
- other small libraries or packages

## How the webpage works?

The idea is simple. The user can register . During registration you need to enter these fields:

- Username
- Password: it is checked to match, must be at least 6 symbols long and is hashed after checks are done
- Password again

Registration allows you to access "/" index route


### Routing

Each route checks if the user is registered. All routes :

- index : it is the main route of the app but you need to login and register first for this.
- login : Get deta for specific user. check if the user is registered. And show alarts if user provides any invlaid details.
- register : Get user deta and save to detabase. And show alarts if user provides any invlaid details.
- add city : Chack for vlaid city and add to user detabase of that user.
- delete : Get name of city and delete from the detabase for specific user.
- contact : Render contact.html.
- logout : Delete session and redricte to login.

### Templates

- index.html
- register.html
- login.html
- contact.html
- layout.html

### Sessions

The webpage uses sessions to confirm that user is registered. Once the user logins, with his user name and password session will take his user name. Once everything passes a session is created (serialized and deserialized) and stored in the cookies. The server attaches user to subsequent requests, so the back-end can easily access the details, like : cities that the user added.

### Database

Database weather.db contains tow table :
- users
- cities

### stctic

Contains assets used by the templates, including CSS files, favicon.

###  requirements.text

Libraries that used:

- cs50
- Flask
- Flask-Session
- requests

## Possible improvements

As all applications this one can also be improved. Possible improvements:

- By add date and time of cities
- By add sunrise and sunset time

## How to launch application

- Just Type : flask run
