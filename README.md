# Canvas Reviews

Canvas is a Django photo sharing application where users
can review, like, and post different methods of consuming
cannabis strains.

## :camera_flash: Screenshots

<img width="380" alt="Screenshot 2022-11-28 at 9 01 44 PM" src="https://user-images.githubusercontent.com/15901574/219600936-7b040f1f-21f3-409a-9221-9ce65fef7d8f.png">

<img width="377" alt="Screenshot 2022-11-28 at 9 02 13 PM" src="https://user-images.githubusercontent.com/15901574/219601062-c4f1b59f-55f3-42de-977e-eaae1ff2cb53.png">

<img width="379" alt="Screenshot 2022-11-28 at 9 03 23 PM" src="https://user-images.githubusercontent.com/15901574/219600801-6e0685f5-10f8-49af-abcf-a9f62556d54e.png">

## :artificial_satellite: Technologies
* Python
* Django
* Django auth
* PostgreSQL
* AWS S3
* Bootstrap
* Heroku

## :hammer_and_wrench: Installation

Create an environment for the application dependencies using an environment manager of your choice. See [virtualenv](https://virtualenv.pypa.io/en/latest/) or [conda](https://docs.conda.io/en/latest/).

```bash
conda create --name $ENVIRONMENT_NAME python
```

Activate the environment.

```bash
conda activate $ENVIRONMENT_NAME
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 
the dependencies located in requirements.txt.

```bash
python -m pip install -r requirements.txt
```

Create a table in PostgreSQL and [configure the setings.py](https://docs.djangoproject.com/en/3.2/ref/settings/) located in the canvas directory.

Make the migrations.

```bash
python manage.py makemigrations
```

Apply the changes to the database.

```bash
python manage.py migrate
```

Run the server.

```bash
python manage.py runserver
```

## Next Features
* Updated create view UI
* Light/Dark UI toggle
* Admin upload strains by CSV
* Admin upload users by CSV
* Dockerize





