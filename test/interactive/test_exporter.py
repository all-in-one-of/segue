# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import os
import sys
import time
import tempfile

from PySide import QtGui

from segue import discover_processors
from segue.backend.host.base import Host
from segue.frontend.exporter import ExporterWidget


class MockHost(Host):
    '''Mock host implementation.'''
    
    def get_selection(self):
        '''Return current selection.'''
        return ['|group1|objectA', '|group2|objectB', '|objectC',
                '|group3|group4|objectD']

    def get_frame_range(self):
        '''Return current frame range.'''
        return (1.0, 24.0)
    
    def save(self, target=None):
        '''Save scene.'''
        pass
    
    def save_package(self, selection=None, source=None, target=None,
                     start=None, stop=None, step=1):
        '''Export.'''
        if target is None:
            target = tempfile.mkdtemp('_segue')
            
        print 'Exporting to {0}.'''.format(target)
        for index in range(10):
            print 10 - index
            time.sleep(1)


if __name__ == '__main__':
    '''Interactively test the exporter.'''
    app = QtGui.QApplication(sys.argv)

    host = MockHost()
    processors = discover_processors(paths=[
        os.path.join(os.path.dirname(__file__), 'plugin')
    ], options={'host': host})
    widget = ExporterWidget(host=host, processors=processors)
    widget.show()
    
    raise SystemExit(app.exec_())

