#!/usr/bin/env python3
import sys
sys.path.append('lib')

import logging

from ops.charm import CharmBase
from ops.main import main

from ops.framework import (
    Object,
    ObjectEvents,
    EventSource,
    EventBase,
)


logger = logging.getLogger()


class FooAvailableEvent(EventBase):
    """Emitted when the value for 'foo' has been received."""


class FooEvents(ObjectEvents):
    foo_available = EventSource(FooAvailableEvent)


class FooRequires(Object):

    on = FooEvents()

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)
        self.framework.observe(
            charm.on[relation_name].relation_changed,
            self.on_relation_changed
        )

    def on_relation_changed(self, event):
        logger.info(event.relation.data[event.unit]['foo'])
        self.on.foo_available.emit()


class FooRequirerCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.start, self.on_start)
        self.framework.observe(self.on.install, self.on_install)

        self.foo = FooRequires(self, "foo")
        self.framework.observe(self.foo.on.foo_available, self.on_foo_available)

    def on_start(self, event):
        pass

    def on_install(self, event):
        pass

    def on_foo_available(self, event):
        logging.info("FOO AVAILABLE IN CHARM")


if __name__ == "__main__":
    main(FooRequirerCharm)
