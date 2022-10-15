# grocery-list

## Dependencies

Flask dependency is used in this project, if you don't have it run this :

```
pip install flask
pip install pytest
pip install mutmut #mutation testing
```

## Start command

To start the project, run this command :

```
python3 init_db.py reset_db
python3 __init__.py
```

To run tests, execute this command from root:

```
pytest
mutmut run #Run mutation testing
mutmut html #Export Result into html/ folder
```
