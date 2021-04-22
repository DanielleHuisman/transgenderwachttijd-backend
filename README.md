# transgenderwachttijd.nl

Website which displays the current waiting times for transgender care in the Netherlands.

## Development
### Prerequisites
Make sure Python 3, pip, PyCharm and Pipenv are installed on your system.
You can install Pipenv by running `pip install pipenv` in a terminal.

### Setup
1. Clone this repository.
2. Open the folder in PyCharm.
3. Go to `Settings > Project > Python Interpreter`.
4. Go to the settings next to `Python Interpreter` and click `Add...`.
5. Select `Pipenv environment` on the left side.
6. Make sure the `Base interpreter` and `Pipenv executable` are correct.
7. Make sure `Install packages from Pipfile` is checked.
8. Click `Ok`. PyCharm will now install the dependencies.
9. Close the settings.
10. Open PyCharm's terminal (bottom left).
11. Run the migrations with `python manage.py migrate`.
12. Seed the database with `python manage.py loaddata */fixtures/*.json`.
13. Run the cache migrations with `python manage.py createcachetable`.
14. Create an admin user with `python manage.py createsuperuser`.
15. Close PyCharm's terminal.

### Running
PyCharm should have automatically detected Django and created a run configuration for the project.
You can now run the project by clicking the green arrow (`Run`) or green bug (`Debug`) in the top right corner.

## Production
### Setup
TODO

Run the following commands in the Docker container (`docker exec -it <container id> bash`).
```bash
# Seed database
pipenv run python manage.py loaddata */fixtures/*.json

# Create super user
pipenv run python manage.py createsuperuser
```

TODO
