# Depinj 

Depinj is a python dependency injection library based on type annotations, it allow's you to define members of a class, and if the type of those members are in the dependency injection system it will be injected once that is called. For example

```python
import depinj 
import random

class RandomNumber:
	rnumber = random.random()

class TestClass:
	rnumber: RandomNumber

depinj.add_scoped(RandomNumber)
depinj.add_scoped(TestClass)

test_class = depinj.get_scoped(TestClass)
```

The *test_class* variable will have an scoped RandomNumber instance, there is support for singletons to, with the function *add_singleton*.

### inject

There is an *inject* decorator that inject's the dependencies into function objects, for example following the previous code:

```python
import depinj 

@depinj.inject
def print_number(rn: RandomNumber):
	print(rn.rnumber)

print_number()
```

It can also be used in the *__init__* method like this:

```python

class TestClass:
	rnumber: RandomNumber

	@pydep.inject
	def __init__(self, rnumber: RandomNumber):
		self.rnumber = rnumber
	
test_class = TestClass()
```

### Depinj object

```python
from depinj import Injector 

dep = Injector()

dep.add_scoped(SomeClass)
```

This Injector object represent's the dependency injection system, in fact, the functions defined at top-level module are using a global instance of the Depinj class. This way you can have multiple dependency injection systems if you want to have different classes for each one.

If you are going to use a different Injector object than the global one, then you have pass that object into the *inject* function with the *injector* named parameter. 