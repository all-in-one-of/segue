# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.


from PySide import QtGui, QtCore


class OptionsWidget(QtGui.QFrame):
    '''Manage export options.'''
    
    def __init__(self, host, processors=None, parent=None):
        '''Initialise with *host* application and *parent*.'''
        super(OptionsWidget, self).__init__(parent=parent)
        self._host = None
        self.build()
        self.post_build()
        
        self.host = host
        
        if processors:
            self.set_processors(processors)
    
    @property
    def host(self):
        '''Return current host application.'''
        return self._host
    
    @host.setter
    def host(self, host):
        '''Set host application to *host*.'''
        self._host = host
        
        self.frame_range_combobox.clear()
        self.frame_range_combobox.addItem('Set Manually', 'manual')
        try:
            self.host.get_frame_range()
        except (NotImplementedError, AttributeError):
            pass
        else:
            self.frame_range_combobox.addItem('Set From Time Slider', 'auto')
            self.frame_range_combobox.setCurrentIndex(
                self.frame_range_combobox.count() - 1
            )
    
    def get_processors(self):
        '''Return current processors.'''
        processors = []
        for index in self.processor_widget.count():
            processors.append(
                self.processor_widget.itemData(index)
            )
        
        return processors
    
    def set_processors(self, processors):
        '''Set processors clearing any existing ones.'''
        self.processor_widget.clear()
        
        if processors is None:
            return
        
        for processor in processors:
            self.processor_widget.addItem(processor.display_name, processor)
        
    def build(self):
        '''Build and layout the interface.'''
        self.setLayout(QtGui.QGridLayout())
        
        self.frame_range_label = QtGui.QLabel('Range')
        self.layout().addWidget(self.frame_range_label, 0, 0)
        
        self.frame_range_combobox = QtGui.QComboBox()
        self.layout().addWidget(self.frame_range_combobox, 0, 1)
        
        self.frame_range_group = QtGui.QFrame()
        self.frame_range_group.setLayout(QtGui.QHBoxLayout())
        self.frame_range_group.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.frame_range_group, 1, 1)
        
        self.start_frame_widget = QtGui.QDoubleSpinBox()
        self.start_frame_label = QtGui.QLabel('Start')
        self.start_frame_label.setBuddy(self.start_frame_widget)
        self.frame_range_group.layout().addWidget(self.start_frame_label)
        self.frame_range_group.layout().addWidget(self.start_frame_widget,
                                                  stretch=1)
        
        self.stop_frame_widget = QtGui.QDoubleSpinBox()
        self.end_frame_label = QtGui.QLabel('End')
        self.end_frame_label.setBuddy(self.stop_frame_widget)
        self.frame_range_group.layout().addWidget(self.end_frame_label)
        self.frame_range_group.layout().addWidget(self.stop_frame_widget,
                                                  stretch=1)
        
        self.step_frame_widget = QtGui.QDoubleSpinBox()
        self.step_frame_label = QtGui.QLabel('Step')
        self.step_frame_label.setBuddy(self.step_frame_widget)
        self.frame_range_group.layout().addWidget(self.step_frame_label)
        self.frame_range_group.layout().addWidget(self.step_frame_widget,
                                                  stretch=1)
        
        self.processor_widget = QtGui.QComboBox()
        self.processor_label = QtGui.QLabel('Process')
        self.processor_label.setBuddy(self.processor_widget)
        self.layout().addWidget(self.processor_label, 2, 0)
        self.layout().addWidget(self.processor_widget, 2, 1)
        
        self.layout().setColumnStretch(0, 0)
        self.layout().setColumnStretch(1, 1)
        
    def post_build(self):
        '''Perform post-build operations.'''
        self.start_frame_widget.setMinimum(-10000.00)
        self.start_frame_widget.setMaximum(10000.00)
        
        self.stop_frame_widget.setMinimum(-10000.00)
        self.stop_frame_widget.setMaximum(10000.00)
        
        self.step_frame_widget.setValue(1.0)
        self.start_frame_widget.setValue(1.0)
        self.stop_frame_widget.setValue(24.0)
        
        self.frame_range_combobox.currentIndexChanged.connect(
            self.on_select_range
        )
    
    def on_select_range(self, index):
        '''Handle choice of range options.'''
        option = self.frame_range_combobox.itemData(index)
        if option == 'auto':
            for control in (self.start_frame_widget, self.stop_frame_widget):
                control.setEnabled(False)
                
            start, stop = self.host.get_frame_range()
            self.start_frame_widget.setValue(float(start))
            self.stop_frame_widget.setValue(float(stop))
            
        else:
            for control in (self.start_frame_widget, self.stop_frame_widget):
                control.setEnabled(True)

