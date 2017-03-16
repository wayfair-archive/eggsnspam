Green Eggs & Spam - A Flask Demo App
====================================

Flask is a leight-weight, loosely coupled, and unopinionated framework for developing python web services.

This application serves as an example & guideline for rolling your own Flask app at Wayfair, and in many ways, serves as the "Official Wayfair opinion" on how to structure your Flask projects.

### Some things to keep in mind
- The target audience for this project is people who are new to Python and/or Flask, and the implementation has been kept intentionally basic to minimize complexity.
- Table names follow Wayfair's internal naming convention for selfish reasons.
- Tests intentionally demonstrate 3 patterns of testing including: leveraging an in-memory SQLite database, mocking, and dependency injection. This is to demonstrate different testing patterns.


README.md META
--------------

The README.md should answer the following main questions:

* What does the app do? -- Summarize the app succinctly
* How do I use the app? -- Enumerate the app's endpoints so people know how to use it
* How do I get it up and running locally? -- Outline all the steps required to setup the app from a reasonably blank slate
* How do I run the test suite? -- Demonstrate how to run the test suite

Apps evolves over time, and README files often get out of date. Try your best to keep this file accurate and if someone points out an inaccuracy, fix it immediately.


Service Endpoints
-----------------

"OOP" examples implement the following API:

* `/PROJ/user`:
    * [GET] - List all users
    * [POST] - Create a user
* `/PROJ/user/{user_id}`:
    * [GET] - Get a user by id
    * [PUT] - Update a user
    * [DELETE] - Delete a user
* `/PROJ/user/{user_id}/breakfast_recommendations`:
    * [GET] - Get a user's personalized breakfast recommendations
* `/PROJ/user/{user_id}/preference`:
    * [GET] - List all the user's ingredient preferences
    * [POST] - Create an ingredient preference
* `/PROJ/user/{user_id}/preference/{ingredient_id}`:
    * [GET] - Get a user's ingredient preference
    * [PUT] - Update a user's preference for an ingredient
    * [DELETE] - Delete a user's preference for an ingredient
* `/PROJ/breakfast`:
    * [GET] - List all breakfasts
* `/PROJ/breakfast/{breakfast_id}`:
    * [GET] - Get a breakfast by id
* `/PROJ/ingredient`:
    * [GET] - List all ingredients
* `/PROJ/ingredient/{ingredient_id}`:
    * [GET] - Get an ingredient by id

The "Simple" example is aimed at those who want to get right to the vector math and simplify their implementation as much as possible. I'm looking at you, Data Scientists!

* `/PROJ/user/{user_id}/breakfast_recommendations`:
    * [GET] - Get a user's personalized breakfast recommendations


Quickstart
----------

### Dependencies

So long as you have Vagrant installed and configured, you should be good to go. If you don't, please follow the instructions at https://www.vagrantup.com/.

### Install and run the test suite / service

1) Clone the repo

2) Initialize Vagrant from the `eggsnspam` folder
```bash
vagrant up
```

3) SSH onto your vagrant box with `vagrant ssh` and run the test suite:
```bash
bin/run_tests.sh
```

4) While SSHed into the vagrant box, you can also start the service:
```
bin/run_local.sh
```

You should now have the eggsnspam service running on http://localhost:8888/

### Run These Example Queries inside your VM while `run_local.sh` is running

```
## Create a user using oop_phrasebook
curl -X "POST" "http://localhost:8888/oop_phrasebook/user/" \
     -H "Content-Type: text/plain; charset=utf-8" \
     -d $'{
  "first_name": "Robert",
  "last_name": "Ford"
}'

## Create a user using oop_orm
curl -X "POST" "http://localhost:8888/oop_orm/user/" \
     -H "Content-Type: text/plain; charset=utf-8" \
     -d $'{
  "first_name": "Dolores",
  "last_name": "Abernathy"
}'

## Get a user using oop_orm
curl -X "GET" "http://localhost:8888/oop_orm/user/1"

## Get recommendations using oop_phrasebook
curl -X "GET" "http://localhost:8888/oop_phrasebook/user/1/breakfast_recommendations"

## Get recommendations using simple_phrasebook
curl -X "GET" "http://localhost:8888/simple_phrasebook/user/1/breakfast_recommendations"
```

Acknowledgements
----------------

- Flask, its community, and the Python community at large. All of you people rock.
- [Fbone](https://github.com/imwilsonxu/fbone) which provided inspiration for the project structure
