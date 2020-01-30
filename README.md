<p align="center">
<img src="https://github.com/lilyyangyn/cds_flask/blob/master/app/static/assets/images/logo.png">
</p>
# CDS Ordering Website

This is a python project of ordering website for CDS.

## Getting Started

#### **1. Set Up Virtual Evironment**
Program should be run in a virtual environment.

Created using the third-party utility `virtualenv`:

`virtualenv venv`

The folder now has a subfolder called `venv` that holds a new virtual environment.

__Linux and Mac OS X__ users can activate the virtual environment with the following commands:

`source venv/bin/activate`

For __Windows__ users:

`venv\Scripts\activate`

When the work in the virtual environment is complete, you can return to the global Python interpreter:

`deactivate`

#### **2. Install Requirement Packages**
Requirements can be checked in the file _**requirements.txt**_.

To install all required packages:

```sh
pip install -r requirements.txt
``` 

#### **3. Configure the Components**
+ Edit the _**config.py**_ to configure the components before start the server:

	Set `SQLALCHEMY_DATABASE_URI` to determin which database you want to use
	
+ Edit the configurations through os environmental variables:
	
	Set `MAIL_USERNAME` and `MAIL_PASSWORD` for email sending
	
	Set `CDS_ADMIN` to determine the admin-privilege account

#### **4. Start the Server**
Go to the root of the project:

`cd CDS`

Start the server: 

`python manage.py runserver`

## Available Commands

#### Start the Server

`python manage.py runserver`

#### Start the Shell

`python manage.py shell`

#### Database Migration

`python manage.py db <MigrateCommand>`

MigrateCommand:
+ `init`: Create a migration repository
+ `upgrade`: Apply the changes in the migration to the database
+ `downgrade`: Delete all changes in the migration
+ `migrate`: Create migration automatically
+ `revision`: Create migration manually

#### Test

`python manage.py test [--coverage]`

## Project Structure
+ app
	- routings (blueprints)
	
		- main
		
			- main routes: 
			
				`menu, weekly_menu, about`
			
			- error handler: 
				`403, 404, 500`
			
		- auth
		
			- authentication routes: 
			
				```
				login, logout, 
				signup, confirm, resend_confirmation, unconfirmed, 
				change_password, password_reset_request, password_reset```
		
		- client
		
			- client routes:
			
				```
				users,
				profile, edit_profile
				deposits, create_deposit, in_debt```
			
		- supply
		
			- dish routes:
				
				```
				dishes,
				clear_all_stocks, reset_available_days,
				new_dish, edit_dish,
				supply_dish, stop_supply_dish,
				increase_stock, decrease_stock```			
			
			- restaurant routes:
			
				```
				restaurants,
				new_restaurant, edit_restaurant,
				stop_cooperation, start_cooperation```
			
			- spot routes:
			
				```
				spots,
				new_spot, edit_spot,
				stop_use, start_use```
			
		- ordering
		
			- ordering routes:
				
				```
				orders, 
				daily_orders_statistics, daily_orders_printing,
				create_order, cancel_order, invoice, 
				
	- templates
	
		_dynamic pages corresponding to different routes_
	
	- static
	
		_static files including assets (pics, css) and static pages_
		
	- \_\_init\_\_.py
	
		_init the app and all related components, e.g. db, mail sender, scheduler, etc._
		
	- decorators.py
	
	- emails.py
	
	- models.py
	
	- schedulerjobs.py
	
+ migration

	_Database migration records_
	
+ tests

	_Unit tests_
	
+ venv

	_The virtual environment_
