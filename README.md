logging_demo
============

Demonstration of category logging in python.

The goal here is to show category logging as done in python.
Category logging allows you to use whatever categorization schema you'd like,
but I'm a big fan of keeping things simple, so I go with `Class.method`.
Of course if you use the class name for your schema,
you immediately have to ask yourself about inheritance.
I looked into this and ended up with two different approaches.

static
------

This is the simple approach of just naming the logger directly.
The benefit here is that logging messages are very easy to trace into the source code.
For example:

```python
from logging import getLogger


class A(object):
    def __init__(self):
        l = getLogger('A.__init__')
        l.info('A info message')


class B(A):
    def __init__(self):
        super(B, self).__init__()
        l = getLogger('B.__init__')
        l.info('B info message')

o = B()
```

This would lead to 2 info messages.
The first logged under category `A.__init__` and the second logged under `B.__init__`.
So, it's easy to trace the message back to the code.
However if you want to manipulate the logging level of all methods called via B,
you will need to also manipulate the logging level of A.
I find this counter-intuitive. Worse, it leads to overly verbose config code.
This substantially interferes with the value proposition of category logging.

introspective
-------------

What if we use introspection to find the class and method name?
There are a couple of benefits here.
The most obvious is that implementation of the getLogger call becomes copy-pasta.
It also makes filtering by category more intuitive IMHO.
When I tweak logging levels on a class, I think least surprise is that it's super() calls inherit those logging levels.
For example:

```python
from inspect import stack as inspect_stack
from logging import getLogger


class A(object):
    def __init__(self):
        l = getLogger("{}.{}".format(self.__class__.__name__, inspect_stack()[0][3]))
        l.info('A info message')


class B(A):
    def __init__(self):
        super(B, self).__init__()
        l = getLogger("{}.{}".format(self.__class__.__name__, inspect_stack()[0][3]))
        l.info('B info message')


class C(A):
    def __init__(self):
        super(C, self).__init__()
        l = getLogger("{}.{}".format(self.__class__.__name__, inspect_stack()[0][3]))
        l.info('C info message')

o = B()
```

In this case, both info messages are under the `B.__init__` category.
I think this makes sense since if you're manipulating logging levels for B or B.__init__,
you probably don't want to also have to go writing config to manipulate logging levels for the parent, A.
It also means that both B and C classes may have different configurations and that those configurations
will be adhered to in A's behavior depending on which child class is calling into A's methods.

I feel that the introspective approach is the better option, but the downside is that it's ugly.

auto_getlogger
--------------

There's a lot of complicated code being replicated in the introspective example.
It's even using inspect.stack(), which is, in my experience, a little bit fragile,
and not something I like putting in production code.
Worse, all that replication of code is just plain ugly,
so let's use the auto_getlogger package at
https://github.com/ahammond/auto_getlogger
to automate things.

```bash
pip install auto_getlogger
```

Now our code looks a lot simpler but works the same as the introspective example above.

```python
from auto_getlogger import AutoGetLogger

class A(AutoGetLogger):
    def __init__(self, l=None):
        l. info('A info message')


class B(A):
    def __init__(self, l=None):
        super(B, self).__init__()
        l.info('B info message')


class C(A):
    def __init__(self, l=None):
        super(C, self).__init__()
        l.info('C info message')
```

In this case, we have the same behavior as with the introspective code above,
but with much cleaner code.
