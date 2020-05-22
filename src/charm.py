#!/usr/bin/env python3
import sys
sys.path.append('lib')

import logging

from ops.charm import CharmBase
from ops.framework import Object
from ops.main import main


logger = logging.getLogger()


class FooRequires(Object):

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)
        self.framework.observe(
            charm.on[relation_name].relation_changed,
            self.on_relation_changed
        )

    def on_relation_changed(self, event):
        logger.info(event.relation.data[event.unit]['foo'])


class FooRequirerCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.start, self.on_start)
        self.framework.observe(self.on.install, self.on_install)

        self.foo = FooRequires(self, "foo")

    def on_start(self, event):
        pass

    def on_install(self, event):
        pass


if __name__ == "__main__":
    main(FooRequirerCharm)
