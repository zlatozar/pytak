# -*- coding: utf-8 -*-

"""
    predicates
    ~~~~~~~~~~

    Contains predicates that could be used in select statements

    :copyright: (c) 2014 by Zlatozar Zhelyazkov.
    :license: BSD, see LICENSE for more details.
"""

import datetime
import logging

log = logging.getLogger(__name__)

# ___________________________________________________________
#                                                       Time

# Before period
def created_before_delta(id_reg, days_before=0, hours_before=0, min_before=0, sec_before=0):
    "Check times with id_reg mask if they are before time now plus time delta"

    hours_before = datetime.datetime.now() - datetime.timedelta(days=days_before, hours=hours_before,
                                                                minutes=min_before, seconds=sec_before)

    def created_before_delta_p(clazz, idx):
        """
        Compose idx(current index e.g. 0, 1, 2, etc.) and id_reg to form key from
        clazz(stack data with key clazz) and check if date is smaller that given time delta
        """
        creation_date = __creation_date(clazz, id_reg, idx)

        if creation_date < hours_before:
            return True

        else:
            log.debug("Predicate '%s' fails for %s:%s" % ("created_before_delta_p", __replace_star(id_reg, idx),
                                                          creation_date))

        return False

    return created_before_delta_p

# Before
def created_before(id_reg, required_time):
    "Check times with id_reg mask if they are created before given time"

    def created_before_p(clazz, idx):
        """
        Compose idx(current index e.g. 0, 1, 2, etc.) and id_reg to form key from
        clazz(stack data with key clazz) and check if date is smaller to required_hour
        """
        creation_date = __creation_date(clazz, id_reg, idx)

        if creation_date < required_time:
            return True

        else:
            log.debug("Predicate '%s' fails for %s:%s" % ("created_before_p", __replace_star(id_reg, idx),
                                                          creation_date))

        return False

    # return predicate
    return created_before_p

# Equal
def created_exact(id_reg, required_time):
    "Check times with id_reg mask if they are created at given time"

    def created_exact_p(clazz, idx):
        """
        Compose idx(current index e.g. 0, 1, 2, etc.) and id_reg to form key from
        clazz(stack data with key clazz) and check if date is equal to required_hour
        """
        creation_date = __creation_date(clazz, id_reg, idx)

        if creation_date == required_time:
            return True

        else:
            log.debug("Predicate '%s' fails for %s:%s" % ("created_exact_p", __replace_star(id_reg, idx),
                                                          creation_date))

        return False

    return created_exact_p

# After
def created_after(id_reg, required_time):
    "Check times with id_reg mask if they are created after given time"

    def created_after_p(clazz, idx):
        """
        Compose idx(current index e.g. 0, 1, 2, etc.) and id_reg to form key from
        clazz(stack data with key clazz) and check if date is bigger to required_hour
        """
        creation_date = __creation_date(clazz, id_reg, idx)

        if creation_date > required_time:
            return True

        else:
            log.debug("Predicate '%s' fails for %s:%s" % ("created_after_p", __replace_star(id_reg, idx),
                                                          creation_date))

        return False

    return created_after_p

# ___________________________________________________________
#                                                     Values

def smaller(id_reg, standard_value):
    """Check values with id_reg mask if they are smaller than given value"""

    def smaller_p(clazz, idx):
        value = __extract_value(clazz, id_reg, idx)

        if cmp(value, standard_value) < 0:
            log.debug("'%s' < '%s'" % (value, standard_value))
            return True

        else:
            log.debug("Predicate '%s' fails for %s:%s" % ("smaller_p", __replace_star(id_reg, idx),
                                                          value))

        return False

    return smaller_p

def exactly(id_reg, standard_value):
    """Check values with id_reg mask if they are equal with given value"""

    def exactly_p(clazz, idx):
        value = __extract_value(clazz, id_reg, idx)

        if cmp(value, standard_value) == 0:
            log.debug("'%s' == '%s'" % (value, standard_value))
            return True

        else:
            log.debug("Predicate '%s' fails for %s:%s" % ("exactly_p", __replace_star(id_reg, idx),
                                                          value))

        return False

    return exactly_p

def bigger(id_reg, standard_value):
    """Check values with id_reg mask if they are bigger than given value"""

    def bigger_p(clazz, idx):
        value = __extract_value(clazz, id_reg, idx)

        if cmp(value, standard_value) > 0:
            log.debug("'%s' > '%s'" % (value, standard_value))
            return True

        else:
            log.debug("Predicate '%s' fails for %s:%s" % ("bigger_p", __replace_star(id_reg, idx),
                                                          value))

        return False

    return bigger_p

# ___________________________________________________________
#                                           Helper functions

def __creation_date(clazz, id_reg, idx):
    return datetime.datetime.fromtimestamp(float(clazz[__replace_star(id_reg, idx)]) / 1000.0)

def __extract_value(clazz, id_reg, idx):
    return clazz[__replace_star(id_reg, idx)]

def __replace_star(id_reg, idx):
    """Replace every star in id_reg with the corresponding idx list

    Args:
      id_reg (str): String with '*' instead of index
      idx (list): List of indexes/digits that should replace '*'
    """
    incr = id_reg
    for i in idx:
        incr = incr.replace('*', i, 1)

    return incr
