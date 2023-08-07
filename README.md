# photo-sharing
A photo-sharing app experiment

# To setup your EC2
```sudo apt-get update```

## Step 1: Clone the Repository

1. Open your terminal or command prompt.

2. Change to the directory where you want to clone the Photo Sharing app. For example:
```cd djangoprojects```

3. Clone the repository by running the following command:

```git clone https://github.com/MikeMatovu/photo-sharing.git```

## Step 2: Install Dependencies
4. Once the repository is cloned, change to the app's directory:

```cd photo-sharing```

## Step 3: Install Dependencies

5. Install the required Python packages from the 'requirements.txt' file:

```pip install -r requirements.txt```

## Step 4: Set Up the Database

1. Apply the database migrations to create the necessary database schema:

```python manage.py migrate```


## Step 5: Create a Superuser (Optional but Recommended)

Creating a superuser allows you to access the Django admin interface and manage the app's data.

1. Create a superuser by running:
```python manage.py createsuperuser```


2. Follow the prompts to set a username, email, and password for the superuser.

## Step 6: Run the Development Server

1. Start the development server by running:
```python manage.py runserver```


2. Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/). You should see the Photo Sharing app's homepage.

## Step 7: Access the Admin Interface (Optional)

1. To access the Django admin interface, go to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

2. Log in using the superuser credentials you created earlier.

## Congratulations! You've successfully cloned and run the Photo Sharing Django app on your local machine. You can now explore and interact with the app using your web browser. Enjoy sharing photos and engaging with other users on the app!


