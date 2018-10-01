# Fast-Food-Fast

- This is an online system where users can place orders on the available food items

# User Interface

- https://m-asiimwe.github.io/Fast-Food-Fast/

# Deployment:

- https://fast-foods-fast-1.herokuapp.com/api/v1/orders

# Functionality 

- User can signup and login as client or admin.
- Customer can place an order.
- Admin can view a list of orders.
- Admin can accept or decline orders.
- Admin can mark orders as completed.
- Customer  can view a history of ordered food.

# Endpoints

- Get all orders | /api/v1/orders
- Get a specific order | /api/v1/orders/<int:order_id>
- Place a new order | /api/v1/orders
- pdate the status of an order | /api/v1/orders/<int:order_id>

# Prerequisites

- You will need postman
- Install python 3.6
- Install and create a virtual environment
- Install the requirements at "requirements.txt" in the created virtual environment

# Getting Started

- Clone the api branch to your computer with "git clone https://github.com/m-asiimwe/Fast-Food-Fast/tree/api
- Run the run.py file to start your local server with the command (python run.py) after installing the virtual environment

# Running the tests

- To run the test run "pytest --cov" in a command line interface

# Build badge

[![Build Status](https://travis-ci.org/m-asiimwe/Fast-Food-Fast.svg?branch=api)](https://travis-ci.org/m-asiimwe/Fast-Food-Fast?branch=api)

# Coverage Badge

[![Coverage Status](https://coveralls.io/repos/github/m-asiimwe/Fast-Food-Fast/badge.svg?branch=api)](https://coveralls.io/github/m-asiimwe/Fast-Food-Fast?branch=api)

# Maintainability Badge

[![Maintainability](https://api.codeclimate.com/v1/badges/fe5d0f7b2397b5cc47bf/maintainability)](https://codeclimate.com/github/m-asiimwe/Fast-Food-Fast/maintainability)

# Authors

- Mark Ayebare