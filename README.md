README.md

-------------------------------------
Project Overview
-------------------------------------
CURRENT PROJECT GOAL:
Backend Module 02 Assignment: Adding Documentaion and Testing

Utilize Swagger to create documentation for each endpoint for the 
Mechanic API. Include detailed explanations and examples of input and output data. 
Utilize unittest to create a testcase for each endpoint ensuring properfunctionality of all Mechanic API resorces.

---

Backend Specialization 01 MODULE PROJECT GOAL:

Apply advanced techniques learned through Lessons 6-9 to Mechanic API:
- Rate Limiting
- Token Authentification
- Advanced Queries

Implement a new Blueprint for the Mechanic Shop Inventory

---
ORIGINAL PROJECT GOAL:

Expand upon implemented customer blueprint with Marshmallow schemas and completed all CRUD routes in and Application Factory Pattern by adding blueprints and routes for the remaining models: 'mechanic' and 'service_ticket'.

Test each route as it is created in Postman inside a collection. Once project is complete export collection and add to project.


-------------------------------------
Project Installations
-------------------------------------
(also in requirements_swagger.txt)

blinker==1.9.0
cachelib==0.14.0
click==8.3.3
colorama==0.4.6
Deprecated==1.3.1
ecdsa==0.19.2
Flask==3.1.3
Flask-Caching==2.4.0
Flask-Limiter==4.1.1
flask-marshmallow==1.5.0
Flask-SQLAlchemy==3.1.1
flask-swagger==0.2.14
flask-swagger-ui==5.32.6
greenlet==3.5.0
itsdangerous==2.2.0
Jinja2==3.1.6
limits==5.8.0
MarkupSafe==3.0.3
marshmallow==4.3.0
marshmallow-sqlalchemy==1.5.0
mysql-connector-python==9.7.0
ordered-set==4.1.0
packaging==26.2
pyasn1==0.6.3
python-jose==3.5.0
PyYAML==6.0.3
rsa==4.9.1
six==1.17.0
SQLAlchemy==2.0.49
typing_extensions==4.15.0
Werkzeug==3.1.8
wrapt==2.1.2


-------------------------------------
Project Architecture
-------------------------------------
Mechanic_API
|
|
|_app
|    |_blueprints
|    |    |_customers
|    |    |   |___init__.py
|    |    |   |_routes.py
|    |    |   |_schemas.py
|    |    |_inventory
|    |    |   |___init__.py
|    |    |   |_routes.py
|    |    |   |_schemas.py
|    |    |_mechanic
|    |    |   |___init__.py
|    |    |   |_routes.py
|    |    |   |_schemas.py  
|    |    |_service_ticket
|    |        |___init__.py
|    |        |_routes.py
|    |        |_schemas.py     
|    |
|    |_utils
|    |
|    |_static
|    |    |_swagger.yaml
|    |
|    |_ __init__.py
|    |_ extensions.py
|    |_ models.py
|    |
|    |_ tests
|         |_test_customer.py      
|         |_test_inventory.py 
|         |_test_mechanic.py 
|         |_test_service_ticket.py 
|
|_app.py
|_config.py
|_filestructure.txt
|_Mechanic_API.postman_collection.json
|_README.md
|_requirements_swagger.txt


-------------------------------------
Project Useage 
-------------------------------------

Create and test routes to populate tables for a 'mechanic shop'.