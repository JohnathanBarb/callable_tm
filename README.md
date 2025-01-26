# callable_tm

`Callable TM` is a package that allows to implement functions that can join on current
transaction. It is useful when you need to call a function that is not transactional after a
transaction has been committed.

This is integrated with [transaction](https://pypi.org/project/transaction/) package,
which implements a full two-phase commit protocol.


## Usage

```python
import transaction
from callable_tm.callable_tm import callable_tm

@callable_tm
def my_function():
    do_a_kafka_producer_job()


my_function()
# this function was not called. It will be when transaction is committed

transaction.commit()
# now, the function will be called. And the Kafka Producer job will be executed
```
