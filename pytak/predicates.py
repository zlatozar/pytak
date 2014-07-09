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
#                                                      Hours

# Before period
def created_before_delta(id_reg, days_before=0, hours_before=0, min_before=0, sec_before=0):
    "Checks given id_reg mask if data is created before given time delta"

    hours_before = datetime.datetime.now() - datetime.timedelta(days=days_before, hours=hours_before,
                                                                minutes=min_before, seconds=sec_before)

    def created_before_delta_p(clazz, idx):
        """
        Compose idx(current index e.g. 0, 1, 2, etc.) and id_reg to form key from clazz(stack data with key clazz)
        and check if date is smaller that given time delta
        """
        creation_date = __creation_date(clazz, id_reg, idx)

        if creation_date < hours_before:
            return True

        else:
            log.debug("Predicate '%s' fails for %s:%s" % ("created_before_delta_p", __replace_star(id_reg, idx), creation_date))

        return False

    return created_before_delta_p

# Before
def created_before(id_reg, required_time):
    "Checks given id_reg mask if data is created before given time"

    def created_before_p(clazz, idx):
        """
        Compose idx(current index e.g. 0, 1, 2, etc.) and id_reg to form key from clazz(stack data with key clazz)
        and check if date is smaller to required_hour
        """
        creation_date = __creation_date(clazz, id_reg, idx)

        if creation_date < required_time:
            return True

        else:
            log.debug("Predicate '%s' fails for %s:%s" % ("created_before_p", __replace_star(id_reg, idx), creation_date))

        return False

    # return predicate
    return created_before_p

# Equal
def created_exact(id_reg, required_time):
    "Checks given id_reg mask if data is created at given time"

    def created_exact_p(clazz, idx):
        """
        Compose idx(current index e.g. 0, 1, 2, etc.) and id_reg to form key from clazz(stack data with key clazz)
        and check if date is equal to required_hour
        """
        creation_date = __creation_date(clazz, id_reg, idx)

        if creation_date == required_time:
            return True

        else:
            log.debug("Predicate '%s' fails for %s:%s" % ("created_exact_p", __replace_star(id_reg, idx), creation_date))

        return False

    return created_exact_p

# After
def created_after(id_reg, required_time):
    "Checks given id_reg mask if data is created after given time"

    def created_after_p(clazz, idx):
        """
        Compose idx(current index e.g. 0, 1, 2, etc.) and id_reg to form key from clazz(stack data with key clazz)
        and check if date is bigger to required_hour
        """
        creation_date = __creation_date(clazz, id_reg, idx)

        if creation_date > required_time:
            return True

        else:
            log.debug("Predicate '%s' fails for %s:%s" % ("created_after_p", __replace_star(id_reg, idx), creation_date))

        return False

    return created_after_p

# ___________________________________________________________
#                                                     Values


# ___________________________________________________________
#                                           Helper functions

def __creation_date(clazz, id_reg, idx):
    return datetime.datetime.fromtimestamp(float(clazz[__replace_star(id_reg, idx)]) / 1000.0)

def __replace_star(id_reg, idx):
    """Replace stars in id_reg with an index value"""
    return id_reg.replace('*', idx)
