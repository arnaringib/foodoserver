# Introduction #

Following is a list of available api commands for foodoserver


# Restaurants #
## Lists all restaurants ##
```
/api/restaurants/
```

## Details for restaurant with id: `<restaurant_id>` ##
```
/api/restaurants/<restaurant_id>/
```

## Reviews for restaurant with id: `<restaurant_id>` ##
```
/api/restaurants/<restaurant_id>/reviews/
```

## Menu for restaurant with id: `<restaurant_id>` ##
```
/api/restaurants/<restaurant_id>/menu/
```

## Submits rating for restaurant with id: `<restaurant_id>` for user with unique `<apikey>` ##
```
/api/restaurants/<restaurant_id>/rate/<rating>/<apikey>/
```

## Submit a review for restaurant ##
```
/api/restaurants/<restaurant_id>/reviews/create/<apikey>/ (POST)
review = <user review>
```

## Restaurants near a given GPS point ##
```
/api/restaurants/near/<lat>/<lng>/<distance_km>/
```

# Types #
## List of all registered restaurants types ##
```
/api/types/
```

# Users #
## Registers new user ##
```
/api/users/signup/ (POST)

required:
email
password

optional:
firstname
lastname
```

## Login ##
```
/api/users/login/

required:
email
password
```

## Info ##
```
/api/users/info/

required:
apikey
```
returns the user information

## Edit ##
### Edit Info ###
```
/api/users/edit/userinfo/(POST)

required:
apikey
password
```


### Password ###
```
/api/users/edit/password/(POST)

required:
apikey
password
```
Returns user object with api key for further interaction with the API