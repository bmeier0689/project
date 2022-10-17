Welcome to Obake Sushi! (Pronounced Oh-Ba-Ke, it means "Monster/Ghost" in Japanese)

Here you will be able to create an account in order to order some MONSTROUSLY delicious sushi. 

After creating an account or logging in, you will find a page where you can decide to create a new order, or use our "omakase" (recommendation) method based on our chef's pick of the day. (I'm toying around with the idea of these recommendations being randomly generated from a list. Or perhaps creating a dictionary with different fish/rice combo's for each day and having the order page populating from there depending on what day it is that the users access the site. But currently I'm not sure how to do that last part, so I need to look into it.)

The user will also be able to edit their account details in case they move or need to change their name for whatever reason. 

The order page will have several entry areas with dropdown boxes, where they can select their choice of fish, they rice that they would like, whether they would like wasabi on it, and the quantity of each item. It will also include a button to add more entries. 

Lastly, the "Confirmation" page will show a detailed list of their items, as well as the quantity, and the price for each item. Then at the bottom it will give a total for all the items. There will also be buttons to cancel their order or go ahead and submit it. 

(SUBMISSION UPDATE)
I was over ambitious when planning this out, I didn't think about needing to use a many-to-many relationship until I was already well along with it, so concessions had to be made to make
sure everything would work in regards to the requirements.

Color scheme of dark mode with colors to represent the sushi stables of wasabi and salmon. Custom characters drawn by me to help add some other elements to the app so its not as flat and 2-dimensional.

Registering a new user and logging into an exsiting one both have validations in place. User must be logged in to view any of the routes within the app. 

Home page allows for 2 different types of orders, however, at this time only the 'New Order' button works, will work on adding functionality to 'Omakase' later on. 

Within the order page, currently there are 3 input boxes, with an option to add 3 more using JS with a hidden element. Currently the 3 hidden ones do not write to the DB nor get shown
on the checkout page though, will work on getting this to work properly later.

Checkout page displays the 3 most recent DB submissions (the users order) and allows the order to be canceled, thereby deleting the DB entries. No prices or total is shown due to needing
to utilize the many-to-many process and creating a table for fish with all of their information, to come in the future.

Accounts page allows you to view your account information and change your information, except password. This page has its own separate validation method but works basically the same as the 
registration pages. 

Along with all of the previously stated things to add/fix in the future, I would also like to work on the reactivity of the app so that it can be viewed on multiple platforms without any layout issues.
