'''
Path Parameter
==================

A Path Parameter is part of the URL path itself.

It is mainly used to identify a specific resource.

ex :- GET /users/101

Real Example
GET /products/500
500 = product ID
API fetches one specific product
In Python Flask
@app.route("/users/<id>")
def get_user(id):
    return f"User ID is {id}"

If request is:
/users/101

Output:
User ID is 101

============================================================

Query Parameter
===================

A Query Parameter comes after ? in the URL.

Used for:

filtering
searching
sorting
pagination
Example
GET /users?city=Bangalore

Here:

city=Bangalore

is the query parameter.

Meaning:


“Get users from Bangalore”

Multiple Query Parameters
GET /products?category=mobile&brand=apple

Meaning:

category = mobile
brand = apple
In Flask
from flask import request

@app.route("/users")
def get_users():
    city = request.args.get("city")
    return f"City is {city}"

Request:

/users?city=Bangalore

Output:

City is Bangalore

==================================================================================================


3. Payload / Request Body
=================================

A Payload (also called Request Body) is data sent inside the HTTP request body.

Mostly used in:

POST
PUT
PATCH

Used when sending large or structured data.

Example
POST /users

Body (Payload):

{
  "name": "Mahadev",
  "age": 24,
  "city": "Bangalore"
}

Meaning:

“Create a new user with these details”

In Flask
from flask import request

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    return data
    
Main Difference
Feature	Path Parameter	Query Parameter	Payload / Body
Location	Inside URL path	After ? in URL	Inside request body
Purpose	Identify specific resource	Filter/search/sort	Send actual data
Mostly Used In	GET, PUT, DELETE	GET	POST, PUT, PATCH
Visible in URL	Yes	Yes	No
Example	/users/101	/users?city=blr	{ "name": "Mahadev" }


Short Interview Answer
==========================

Path parameters are used to identify a specific resource in the URL.
Query parameters are used for filtering, searching, or optional data in the URL.
Payload/request body is used to send actual structured data to the server, mainly in POST or PUT requests.

'''
