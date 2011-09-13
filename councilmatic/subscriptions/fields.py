import pickle

from django.db.models import fields
from django.db.models.fields.subclassing import SubfieldBase

class SerializedObjectField(fields.TextField):
    description = "SerializedObject"
    __metaclass__ = SubfieldBase

    def get_internal_type(self):
        return "TextField"

    @classmethod
    def get_prep_value(cls, value):
#        if callable(value):
#            value = value()
        return pickle.dumps(value)

    def to_python(self, value):
        try:
            print 'unpickled:', pickle.loads(str(value))
            return pickle.loads(str(value))

        # Assume that, if we get an error either in the string conversion or in
        # the unpickling of that string, we mean that this is the exact value we
        # want.
        except:
            print 'verbatim:', repr(value)
            return value

#
# This little bit of magic is here because I tried to migrate with a
# SerializedObjectField, and got an error that directed me to
# http://south.aeracode.org/wiki/MyFieldsDontWork
#
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^subscriptions\.fields\.SerializedObjectField"])
