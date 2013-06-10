from .models import Action
from .models import AffectedContent

def record(user, did_something, *to_items):
    """Enter a new record for an action into the activity log.

    Args:
        user: The actor; an auth.User instance
        did_something: The description of the action
        *to_items: The remaining attributes refer to content items affected
            by the user taking the action.
    """
    action = Action(actor=user, description=did_something)
    action.save()

    for to_item in to_items:
        affect = AffectedContent(action=action, item=to_item)
        affect.save()
