## Testing decisions

### Non tested code, why ?

- Front
raisons : (tests plus complexes et long, on a préféré se focaliser sur les units tests et functional)

- Flask 
raisons

- Mutation testing

L'exécution du mutation testing a retourné un cas d'erreur en modifiant la méthode `get_db_connection` présente dans
`src/connexion.py`. La méthode contient un `print` de l'erreur de `sqlite3.error`. Le mutation testing va remplacer 
l'erreur par un None et cela va générer une mutant non tué. Nous avons décidé de ne pas tester cette fonction car il 
s'agirait de tester un cas d'erreur et le test porterait sur la méthode print qui est native à python et non pas écrite 
par nous.

> Ci dessous il y a la trace de l'exécution du mutation testing sur `get_db_connection`

```text
--- src\connexion.py
+++ src\connexion.py
@@ -8,5 +8,5 @@
         conn = sqlite3.connect(path)
         conn.row_factory = sqlite3.Row
     except sqlite3.error as e:
-        print(e)
+        print(None)
     return conn
```

> Ci dessous la méthode en question

```python
def get_db_connection(test=False): # pragma: no mutate
    path = 'database.db' # pragma: no mutate
    if test:
        path = 'databasetest.db' # pragma: no mutate
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
    except sqlite3.error as e:
        print(e)
    return conn
```

## What has been tested and why

- Unit tests 
TODO décrire ce qu'on a fait en unit tests

- functional tests
TODO décrire ce qu'on a fait en test fonctionnels

## Advanced techniques used

- Mutation testing

Nous avons choisi d'utiliser le mutation testing sur notre programme python afin de découvrir des bugs que l'on aurait 
pas trouvé autrement. Il va permettre de tester nos tests en faisant muter nos classes. Si les classes mutantes 
survivent, c'est à dire qu'elles ne se font pas arrêter par nos tests, des tests sont manquants. Avec les retours de
l'exécution du mutation testing, nous pouvons créer des cas de tests pour les classes mutantes qui n'ont pas été tuées.


Cela a pour finalité d'augmenter le test coverage de notre code puisqu'on a pu créer de nouveaux cas de tests. 

L'exécution du mutation testing a généré 87 mutants, suite à cela 83 mutants ont été tués et 4 ont survécus

![Mutation testing result](https://github.com/jmichot/grocery-list/blob/main/res/mutmut0.png?raw=true)

Un exemple de mutant non tué qui nous a permi de créer un nouveau cas de test :

L'exécution de mutation testing a révélé un mutant non tué au niveau de la fonction `check_product_name`. Il va modifier
la condition présente dans la méthode en remplaçant un `or` en `and`. Ici le mutant a résisté aux tests puisqu'il n'y en
avait pas, cette fonction n'avait pas été testée. Pour remédier à cela, on a testé les deux cas de la condition.

> Ci dessous la trace de l'exécution du mutation testing sur `check_product_name`

```text
--- src\dao.py
+++ src\dao.py
@@ -29,7 +29,7 @@
 
 # Check name method for potential errors
 def check_product_name(product_name):
-    if product_name is None or type(product_name) is not str:
+    if product_name is None and type(product_name) is not str:
         raise NameException(NAME_NOT_STRING)
```

> Ci dessous la méthode en question 

```python
# Check name method for potential errors
def check_product_name(product_name):
    if product_name is None or type(product_name) is not str:
        raise NameException(NAME_NOT_STRING)
```

> Ci dessous les tests qui ont permis de ne pas retrouver le mutant

```python
def test_check_product_name_failed_none(self):
    with pytest.raises(NameException):
        check_product_name(None)

def test_check_product_name_failed_int_type(self):
    with pytest.raises(NameException):
        check_product_name(1)
```

![Mutation testing result](https://github.com/jmichot/grocery-list/blob/main/res/mutmut.png?raw=true)