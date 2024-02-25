Install Django: Once Python is installed, you can install Django using pip, Python's package manager. Open a terminal or command prompt and run the following command:

pip install django

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Create a Django project: In your terminal or command prompt, navigate to the directory where you want to create your Django project. Then, run the following command to create a new Django project:

django-admin startproject project_name

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Navigate to the project directory: Change into the newly created project directory using the cd command:

cd project_name

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Create a Django app: Django projects are made up of one or more apps. You can create a new app within your project using the following command:

python manage.py startapp app_name

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Define models: In your app directory, open the models.py file and define your database models using Django's model syntax. Models define the structure of your database tables and the relationships between them.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Make migrations: After defining your models, you need to create database migrations. Run the following command to generate migrations for your app:

python manage.py makemigrations

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Apply migrations: Once migrations are created, apply them to your database to create the corresponding tables. Run the following command:

python manage.py migrate

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Create a superuser (optional): If you want to access the Django admin interface, you can create a superuser account by running the following command and following the prompts:

python manage.py createsuperuser

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Run the development server: Start the Django development server to test your project locally. Run the following command:

python manage.py runserver

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Access your project: Open a web browser and navigate to http://127.0.0.1:8000/ or http://localhost:8000/ to view your Django project.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
In settings.py You have to Add your email id and password to OTP verification using Email and You have to create Razorpay-integration-in-django and add Id to perform Payment Integration .

I already uploaded my complete working Video 

******FEATURES******
1) user Registration with Otp Verfication
2) Login-page
3) user can change password
4) home page to view all products
5) we can see details of each product
6) cart page
7) payment integration we can use card UPI Bank account etc


******UPDATION******
1) adding rating for each product with average 
2) order confirmation user should receive confirmation message after confirmation of order through mail
3) dividing product types
