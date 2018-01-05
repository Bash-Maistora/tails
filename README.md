# Tails technical challenge

## Set Up

1. Create a virtualenv with Python 3 
2. Install dependencies with pip from requirements.txt
3. Run the server

Task two took longer than expected as I got some errors that turned out to be from postcodes.io unable to locate the Bagshot store from the postcode.

Task three:
1. The user submits his postcode on the webpage with a form.
2. Retrieve the postcode outward from the submitted postode and send an api call with it to postcodes.io.
3. Parse the response to get the nearest codes and their distance. 
3. Filter through the stores to find those within each outward code and append them to a separate list, then add the distance as object variable to the store object. 
4. Sort the list with nearest stores by distance and pass to the template.
