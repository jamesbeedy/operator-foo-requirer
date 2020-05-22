#!/usr/bin/env python3
import sys
sys.path.append('lib')

import logging

from ops.charm import CharmBase
from ops.framework import Object
from ops.main import main


logger = logging.getLogger()


class FooRequires(Object):
    """This class defines the functionality for the 'requires'
    side of the 'foo' relation.

    Hook events observed:
        - relation-changed
    """

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)
        # Observe the relation-changed hook event and bind
        # self.on_relation_changed() to handle the event.
        self.framework.observe(
            charm.on[relation_name].relation_changed,
            self.on_relation_changed
        )

    def on_relation_changed(self, event):
        """This method retrieves the value for 'foo'
        (set by the provides side of the relation) from the
        event.relation.data on the relation-changed hook event.
        """
        # Retrieve and log the value for 'foo' if it exists in
        # the relation data.
        foo = event.relation.data[event.unit].get('foo', None)
        if foo is not None:
            logger.info(f"The value for 'foo' is {foo}!")
        else:
            logger.warning("'foo' not in relation data")


class FooRequirerCharm(CharmBase):
    """This charm demonstrates the requirer side of the relationship by
    extending CharmBase with a custom 'requires' event object that observes
    the relation-changed hook event.
    """
    
    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.start, self.on_start)
        self.framework.observe(self.on.install, self.on_install)

        # Adds our requiring side of the relation, FooRequires to the charm.
        self.foo = FooRequires(self, "foo")

    def on_start(self, event):
        pass

    def on_install(self, event):
        pass


if __name__ == "__main__":
    main(FooRequirerCharm)
