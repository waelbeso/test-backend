# Back-end for Wiredcraft Developer Coding Test

Using django and django rest framework, bullid model for user & addresses.
user authentication using django rest framework built in Token authentication middleware.

## Background

Build a restful api for `get/create/update/delete` user data and Address from a sql-lit database

### User Model

```
{
  "id": "xxx",                  // user id(unique uuid)
  "namename": "test",           // user name
  "dob": "",                    // date of birth
  "description": "",            // user description
  "created_at": ""              // user created date (warp user date_joined to created_at as a property)
  "address": {                  // user address (one to many relation to Address Model )
  "id": "xxx", 
  "name": "",
  "country": "",
  "province": "",
  "city": "",
  "zip_code": "",
  "address": ""
  },
}
```

### API

```
GET    /user/{id}                   - Get user by ID
POST   /user/                       - To create a new user
PUT    /user/{id}                   - To update an existing user with data
DELETE /user/{id}                   - To delete a user from database
```

```
GET    /user/addresses/             - Get all user addresses
POST   /user/addresses/             - To create a new user addresses
PUT    /user/addresses/{id}         - To update an existing user address with data
DELETE /user/addresses/{id}         - To delete a user address from database
```

## Getting started

install the install dependencies

- $ pip install -r requirements.txt

run the server

- $ python src/manage.py runserver







