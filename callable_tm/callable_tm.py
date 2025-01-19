from typing import Callable

import transaction
from transaction.interfaces import IDataManager
from zope.interface import implementer
import threading

__all__ = [
    "TransactionalCallableDataManager",
    "callable_tm",
]

_thread_data = threading.local()


def _remove_tx_callable_manager(*args):
    try:
        del _thread_data.tx_callable_manager
    except AttributeError:
        pass


def _get_tx_callable_manager():
    tx_callable_manager = getattr(_thread_data, "tx_callable_manager", None)
    if tx_callable_manager is None:
        tx_callable_manager = _thread_data.tx_callable_manager = (
            TransactionalCallableDataManager()
        )

    tx = transaction.get()
    tx.join(tx_callable_manager)
    tx.addAfterCommitHook(_remove_tx_callable_manager)
    return tx_callable_manager


@implementer(IDataManager)
class TransactionalCallableDataManager(object):
    transaction_manager = None

    def __init__(self):
        # TODO: collections.Dequeue
        # Queue vs Dequeue vs List
        self.queued_callables = []
        self.in_commit = False

    def __cleanup(self):
        self.queued_callables = []

    def __discard_functions(self):
        self.__cleanup()

    def append(self, func):
        self.queued_callables.append(func)

    def commit(self, _transaction):
        self.in_commit = True

    def sortKey(self):
        return str(id(self))

    def tpc_begin(self, _transaction):
        pass

    def tpc_vote(self, _transaction):
        pass

    def tpc_finish(self, _transaction):
        while self.queued_callables:
            callable_instance, args, kwargs = self.queued_callables.pop(0)
            callable_instance(*args, **kwargs)

        self.in_commit = False
        self.__cleanup()

    def tpc_abort(self, _transaction):
        self.__cleanup()
        self.in_commit = False

    abort = tpc_abort


def callable_tm(call: Callable):
    def __inner_callable(*args, **kwargs):
        _get_tx_callable_manager().append((call, args, kwargs))

    return __inner_callable
