CityFury
========


Setup
-----

1. conda env create -f environment.yml
2. source activate cityfury
3. touch cityfury/local_settings.py
4. python manage.py syncdb
5. python manage.py migrate
6. TODO: python manage.py load_initial_data
7. python manage.py runserver
8. Go to http://127.0.0.1:8000/ on your browser
