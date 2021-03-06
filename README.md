# Banking System
A skeleton  secure  banking  system  (SBS) with  limited  functional, performance, and security requirements for secure banking transactions and user account management.

## Steps to run this application:
- Install python: if you are using mac and have brew installed, run: `brew install python`
- Install [pip](https://pip.pypa.io/en/stable/installing/).
- You may want to set up a python virtual environment to prevent globally installed modules interacting. [Python venv](https://docs.python.org/3/library/venv.html)
- Install python modules: run `pip install -r requirements.txt`
- Ensure you have mysql environment setup on your system.
- Once mysql setup is done, create a local connection with default settings for now.
- Create a schema **ss_project**. If you want a different name, add that name in **settings.py**.
- To create the tables in the database, go inside the **banking_system** directory (where manage.py is located). Then run `python manage.py check`.
- If everything is fine, you won't see any errors. Run `python manage.py makemigrations` now.
- If the above step is successful, run `python manage.py migrate`.
- You should now be able to see the table inside the **ss_project** schema.
- Run `python manage.py runserver` 
- To register a new user go to:  http://localhost:8000/accounts/register.
- To login go to:  http://localhost:8000/accounts/login. (You might not be able to login immediately because the accounts are not active unless an admin makes them active). To make them active, follow the below steps.
  - Django provides an admin panel for super users.
  - To create a super user stop the server and then run: `python manage.py createsuperuser`. Enter all the details (All the fields are manadatory right now.)
  - Go to: http://localhost:8000/admin and login with your credentials.
  - Make the account active from the admin panel.
  - Restart the server: `python manage.py runserver`
  - You should now be able to login.
  - The application now has a OTP functionality. To see the OTP sent, you can either go to the terminal where your local server is running or go to admin panel and check it in the User Login heading.
