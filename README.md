# django-smmc

Searchable Multimedia Collection is a Django app to store files along with tags associated with them. It uses Django REST framework in order to act as a back-end for any client application.

## Quick start

1. Add "smmc" to your INSTALLED_APPS setting (and make sure you have "rest_framework" there) like this:
```python
INSTALLED_APPS = [
	...
	'rest_framework',
    ...
    'smmc',
]
```
2. Include the polls URLconf in your project urls.py like this:
```python
url(r'^smmc/', include('smmc.urls')),
```
3. Run `python manage.py migrate` to create the smmc models.
4. Start the development server and visit http://127.0.0.1:8000/admin/ to create entries and tags (you'll need the Admin app enabled).
5. Visit http://127.0.0.1:8000/smmc/tags/ to view a list of all distinct tags.
6. Visit http://127.0.0.1:8000/smmc/entries/random/ to view random entries or http://127.0.0.1:8000/smmc/entries/tag/[tag]/ to view entries related to specified tag.