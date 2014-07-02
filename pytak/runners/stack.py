# -*- coding: utf-8 -*-

"""
    stack
    ~~~~~

    Implement stack ADT using list. Stack is used to store server
    responses.

    :copyright: (c) 2014 by Zlatozar Zhelyazkov.
    :license: BSD, see LICENSE for more details.
"""

from texttable import Texttable
from colorama import Fore, Style

from pytak.logconf import console_logger

class Stack(object):
    """Implementation of the Stack ADT using a Python list.

    Used to store execution frames
    """
    def __init__(self):
        self._theItems = list()

    def __len__(self):
        """Returns the number of items in the stack. """
        return len(self._theItems)

    def __iter__(self):
        """Defines stack iterator. In this way stack object could be used in loops"""
        if self._theItems:
            ptr = len(self._theItems) - 1
            while ptr >= 0:
                yield self._theItems[ptr]
                ptr -= 1

    def isEmpty(self):
        """Returns True if the stack is empty or False otherwise."""
        return len(self) == 0

    def size(self):
        """Returns stack size"""
        return len(self._theItems)

    def peek(self):
        """Returns the top item on the stack without removing it."""
        assert not self.isEmpty(), "Cannot peek at an empty stack"
        return self._theItems[-1]

    def pop(self):
        """Removes and returns the top item on the stack."""
        assert not self.isEmpty(), "Cannot pop from an empty stack"
        return self._theItems.pop()

    def push(self, item):
        """Push an item on to the top of the stack."""
        self._theItems.append(item)

    def view(self, key=None):
        """Nice stack data view.

        Use colorama module to highlight key if passed and
        texttable for data visualisation
        """

        def __print_select():
            for idx, row in enumerate(self):
                for i in row:
                    if key in i:
                        console_logger.info("select('%s').key(%s)\n" %
                                            (Fore.RED + row['class'] + Style.RESET_ALL,
                                             Fore.RED + i + Style.RESET_ALL))
                        console_logger.info("Value of '%s' is %s\n" % (i,
                                                                       Fore.RED + str(row[i]) + Style.RESET_ALL))

        console_logger.info("\nStack size: %s\n" % self.size())

        table = Texttable()
        table.set_cols_align(["c", "c"])
        table.set_cols_valign(["t", "m"])
        table.set_cols_width([8, 150])
        table.add_row(["Current Index", "Entry"])

        for idx, row in enumerate(self):
            table.add_row([idx, row])

        console_logger.info(table.draw() + "\n")
        if key:
            __print_select()
