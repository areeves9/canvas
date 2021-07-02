# Canvas Reviews

Canvas is a Django photo sharing application where users
can review, like, and post different methods of consuming
cannabis strains.

## Installation

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

## Images

<img src="strains.png" width="250">

![strainProfile](strainProfile.png | width=100)

![feed](feed.png | width=100)





