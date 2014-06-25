"""This module defines all entities which Satellite exposes.

Each class in this module corresponds to a certain type of Satellite entity.
For example, the ``Host`` class corresponds to the "Host" Satellite entity.
Similarly, each class attribute corresponds to a Satellite entity attribute.
For example, the ``Host.name`` class attribute corresponds to the "name"
attribute of a "Host" entity.

"""
from robottelo import orm


class Host(orm.Entity):
    """Entity that represents a Host on a Satellite system."""
    name = orm.StringField(required=True)
