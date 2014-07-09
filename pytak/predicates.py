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

def created_before_hours(id_reg, before=2):
    "Checks given id_reg mask if post is created before given hour"

    hours_before = datetime.datetime.now() - datetime.timedelta(hours=before)

    def created_before_hours_p(clazz, idx):
        """Compose idx and id_reg to form key from stack data and check if date is bigger that 'before'"""
        creation_date = datetime.datetime.fromtimestamp(float(clazz[__replace_star(id_reg, idx)]) / 1000.0)

        if creation_date < hours_before:
            return True

        else:
            log.debug("Predicate '%s' fails for %s:%s" % ("created_before_hours_p", __replace_star(id_reg, idx), creation_date))

        return False

    # return predicate
    return created_before_hours_p


# ___________________________________________________________
#                                           Helper functions

def __replace_star(id_reg, idx):
    """Replace stars in id_reg with an index value"""
    return id_reg.replace('*', idx)
