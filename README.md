# mKisan
A app to let the Farmer sell his crop to any buyer easily, online.

# What this app does?
This app enables Farmers to sell their directly crop to buyers (FPOs, Exporters, Traders, and Processors) which reduces waste of time and increases Farmer's Income. This website is more than an ecommerce website. It also provides helps for farmers. It's made particularly for farmers. It shows current temperature, weather, humidity etc. which is helpful.

# What are the Features?
Some of the features are:

- Easy to use interface
- Easier to buy or sell on this platform
- Small App size, Installable on any device
- Connects Farmers and buyers through one platform.
- Maximizes Farmers profit
- Most of features in a e-commerce site.

# Distinctiveness and Complexity
Many small thing can make a big difference.
## Models
This app stores more data about a listing than the commerce app in cs50 project. As it is made particulary for farmers it stores adding info like crop type, category etc. This app also allows user to sell product in two ways. First is Buy it now and second is Auction. Buy it now where a product has fixed price and buyer can buy it on a fixed price. But in Auction there's a starting price for the user and buyers bet on the product. When the owner close the listing the user with highest bet wins and will get the product.

## Design
This app a whole lot more design enhancements. I used tailwind css in this project.
This website has a responsive layout and has a lot of UI and UX improvements.

## PWA (Progressive Web App)
This app has manifest and service worker which means this website can even work offline and can be installed as an app on user's device. Whereas other apps takes a lot more space, a PWA is just couples of KB's. It's very fast because the service worker cache's the assests on user's browser so that next the user opens the website they don't have to fetch the whole website again, which makes this web app fast.

## Fast
This app ships very low css and js. It's very fast and it got all 90 above rating in lighthouse test.

## User auth
I used the `django-phone-auth` library for the authentication instead of the old one. It allows password resets, email confirmation and more.

# File Structure
In the `commerce` folder is settings and configuration for the project. The main app is in the mKisan folder.
In mKisan folder := In this folder there are static files like js, css, and images. Images contain this app's icons and logo. In the `js` folder there are three files : `listing.js, menu.js and weather.js`. `listing.js` contain js for listing form to work properly, like hiding some fields depending upon user's choice. `menu.js` contains script for the menu functionality and responsiveness. `weather.js` contains weather api calls to show the user current weather info.
in the css folder there is a styles.css file which is generated by tailwind depending on what classes I'm using in the project.
`templates` folder contains html templates for the website. `base.html` is the root template.
`static_src` is folder for tailwind. there are configuration files for tailwind in it.

# How to run this project

First run the django server
```
python manage.py runserver
```
then start tailwind
```
python manage.py tailwind start
```


