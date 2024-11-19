import sys
import matplotlib
matplotlib.use('QtAgg')
import os
from pathlib import Path
import logging
import warnings
warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)
logging.getLogger('matplotlib.font_manager').disabled = True



import numpy as np
import pandas as pd
import fcuff as fc
from fcuff.model import Datum

#import emn_sdk
#from emn_sdk.io.ckan import CKAN

### DO NOT DELETE ###
import PyQt6
dll_dir = os.path.dirname(PyQt6.__file__)
dll_path = os.path.join(dll_dir, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = dll_path

#from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6 import QtCore
from PyQt6 import QtWidgets, QtGui, QtCore

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QDesktopServices, QFont, QPalette, QColor
from PyQt6.QtCore import Qt, qVersion


from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar)

#from matplotlib.backends.qt_compat import is_pyqt5
if qVersion() == 5:
	from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
	from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

else:
	from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
	from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar




import matplotlib
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

class DataHandler():
	def __init__(self):
		self.folder = FuelcellUI.homedir
		self.files = None
		self.data = []
		self.expt_type = 'cp'
		self.colone = 1
		self.coltwo = 2
		self.area = 5
		self.refelec = 0
		self.rxn = 0
		self.pyr = False
		self.pts_to_avg = 300
		self.export_data = False
		self.saveloc = ''

	### actions ###
	def load_raw_data(self):
		all_data = fc.load_data(filename=self.files, folder=self.folder, expt_type=self.expt_type)
		current_names = [d.get_name() for d in self.data]
		new_data = [d for d in all_data if d.get_name() not in current_names]
		self.data.extend(new_data)

	def process_data(self):
		self.load_raw_data()
		if self.expt_type == 'cv':
			fc.cv_process(data=self.data, potential_column=self.colone, current_column=self.coltwo, area=self.area, reference=self.refelec, export_data=self.export_data, save_dir=self.saveloc)
		elif self.expt_type == 'lsv':
			fc.lsv_process(data=self.data, potential_column=self.colone, current_column=self.coltwo, area=self.area, reference=self.refelec, thermo_potential=self.rxn, export_data=self.export_data, save_dir=self.saveloc)
		elif self.expt_type == 'cp':
			fc.cp_process(data=self.data, potential_column=self.colone, current_column=self.coltwo, area=self.area, reference=self.refelec, thermo_potential=self.rxn, export_data=self.export_data, save_dir=self.saveloc, pts_to_avg=self.pts_to_avg, pyramic=self.pyr)
		elif self.expt_type == 'ca':
			fc.ca_process(data=self.data, potential_column=self.colone, current_column=self.coltwo, area=self.area, reference=self.refelec, thermo_potential=self.rxn, export_data=self.export_data, save_dir=self.saveloc, pts_to_avg=self.pts_to_avg, pyramic=self.pyr)

	### accessors ###
	def get_folder(self):
		return self.folder

	def get_files(self):
		return self.files

	def get_data(self):
		return self.data

	def get_expt_type(self):
		return self.expt_type

	### modifiers ###
	def set_folder(self, new_folder):
		self.folder = new_folder

	def set_files(self, new_files):
		self.files = new_files

	def set_data(self, new_data):
		self.data = new_data

	def set_expt_type(self, new_type):
		self.expt_type = new_type

	def set_colone(self, new_col):
		self.colone = new_col
	
	def set_coltwo(self, new_col):
		self.coltwo = new_col

	def set_area(self, new_area):
		self.area = new_area	

	def set_refelec(self, new_val):
		self.refelec = new_val

	def set_rxn(self, new_val):
		self.rxn = new_val

	def set_pyr(self, new_state):
		self.pyr = new_state

	def set_pts_to_avg(self, new_val):
		self.pts_to_avg = new_val

	def set_export_data(self, new_state):
		self.export_data = new_state

	def set_saveloc(self, new_path):
		self.saveloc = new_path

class VisualHandler():
	def __init__(self):
		self.data = []
		self.plot_data = []
		self.datafolder = None
		self.datafiles = None
		self.vis_code = 0
		self.use_raw = False
		self.xcol = 0
		self.ycol = 1
		self.ecol = 3
		self.drawline = True
		self.drawscatter = True
		self.drawerr = False

		self.expt_codes = {0:['ca', 'cp'], 1:['cv'], 2:['lsv'], 3:['eis']}
	
	### actions ###
	def load_data(self):
		new_data = fc.datums.load_data(filename=self.datafiles, folder=self.datafolder)
		for this_data in new_data:
			if this_data.get_processed_data() is None:
				this_data.set_processed_data(this_data.get_raw_data())
		self.data.extend(new_data)


	def draw_plot(self, ax):
		self.plot_data = [d for d in self.data if d.get_expt_type() in self.expt_codes[self.vis_code]]
		if self.vis_code == 0:
			plotfun = fc.visuals.polcurve
			curr = self.xcol
			pot = self.ycol
		elif self.vis_code == 1:
			plotfun = fc.visuals.plot_cv
			curr = self.ycol
			pot = self.xcol
		elif self.vis_code == 2:
			plotfun = fc.visuals.plot_lsv
			curr = self.ycol
			pot = self.xcol
		elif self.vis_code == 3:
			plotfun = fc.visuals.plot_eis
			curr = self.xcol
			pot = self.ycol
		else:
			return
		plotfun(data=self.plot_data, ax=ax, line=self.drawline, scatter=self.drawscatter, errs=self.drawerr, current_column=curr, potential_column=pot, err_column=self.ecol)

	### accessors ###
	def get_plot_data(self):
		return self.plot_data

	### modifiers ###
	def set_datafolder(self, new_folder):
		self.datafolder = new_folder

	def set_datafiles(self, new_files):
		self.datafiles = new_files

	def set_data(self, all_data, replace=False):
		if replace:
			self.data = all_data
			new_data = all_data
		else:
			current_names = [d.get_name() for d in self.data]
			new_data = [d for d in all_data if d.get_name() not in current_names]
		self.data.extend(new_data)

	def set_vis_code(self, new_code):
		self.vis_code = new_code
		new_data = [d for d in self.data if d.get_expt_type() in self.expt_codes[self.vis_code]]
		self.plot_data = new_data

	def set_xcol(self, new_col):
		self.xcol = new_col

	def set_ycol(self, new_col):
		self.ycol = new_col

	def set_ecol(self, new_col):
		self.ecol = new_col

	def set_drawline(self, new_state):
		self.drawline = new_state

	def set_drawscatter(self, new_state):
		self.drawscatter = new_state

	def set_drawerr(self, new_state):
		self.drawerr= new_state

class UploadHandler():
	def __init__(self):
		self.url = 'https://datahub.h2awsm.org/'
		self.apikey = '53596bad-6601-49c1-bf65-e02c7b379776'
		self.project = 'API Sandbox'
		self.institution = 'Lawrence Berkeley National Laboratory'
		self.package = 'foobar_sg'
		self.use_existing = True
		self.files = None
		self.records = None
		self.basedir = FuelcellUI.homedir

	# actions
	def upload(self):
		try:
			ckan = CKAN(self.url, self.apikey)
			ckan.set_dataset_info(self.project, self.institution)
			ckan.upload(name=self.package, files=self.files, records=self.records, basedir=self.basedir, use_existing=self.use_existing)
			return 'upload successful!'
		except Exception as e:
			return str(e)

	# accessors
	def get_url(self, new_url):
		return self.url

	def get_apikey(self, new_key):
		return self.apikey

	def get_project(self, new_proj):
		return self.project

	def get_institution(self, new_inst):
		return self.institution

	def get_package(self, new_pkg):
		return self.package

	def get_useexisting(self, newval):
		return self.useexisting

	def get_files(self, new_files):
		return self.files

	def get_records(self, new_records):
		return self.records

	def get_basedir(self, new_dir):
		return self.basedir
	
	# modifiers
	def set_url(self, new_url):
		self.url = new_url

	def set_apikey(self, new_key):
		self.apikey = new_key

	def set_project(self, new_proj):
		self.project = new_proj

	def set_institution(self, new_inst):
		self.institution = new_inst

	def set_package(self, new_pkg):
		self.package = new_pkg

	def set_useexisting(self, newval):
		self.useexisting = newval

	def set_files(self, new_files):
		self.files = new_files

	def set_records(self, new_records):
		self.records = new_records

	def set_basedir(self, new_dir):
		self.basedir = new_dir

class TableModel(QtCore.QAbstractTableModel):
	def __init__(self, data):
		super().__init__()
		self._data = data

	def data(self, index, role):
		if role == Qt.DisplayRole:
			value = self._data.iloc[index.row(), index.column()]
			if isinstance(value, float):
				value = "%.4f" % value
			return str(value)

	def rowCount(self, index):
		return self._data.shape[0]

	def columnCount(self, index):
		return self._data.shape[1]
		
	def headerData(self, section, orientation, role):
		# section is the index of the column/row.
		if role == Qt.DisplayRole:
			if orientation == Qt.Horizontal:
				return str(self._data.columns[section])
			if orientation == Qt.Vertical:
				return str(self._data.index[section])

class Settings():
    # APP SETTINGS
    # ///////////////////////////////////////////////////////////////
    ENABLE_CUSTOM_TITLE_BAR = True
    MENU_WIDTH = 240
    LEFT_BOX_WIDTH = 240
    RIGHT_BOX_WIDTH = 240
    TIME_ANIMATION = 500

    # BTNS LEFT AND RIGHT BOX COLORS
    BTN_LEFT_BOX_COLOR = "background-color: rgb(44, 49, 58);"
    BTN_RIGHT_BOX_COLOR = "background-color: #ff79c6;"

    # MENU SELECTED STYLESHEET
    MENU_SELECTED_STYLESHEET = """
    border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
    background-color: rgb(40, 44, 52);
    """
class FuelcellWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Fuel Cell UFF')
		self.menubar = self.menuBar()
		self.statusbar = self.statusBar()
		self.statusbar.showMessage('GUI launched successfully', 5000)
		self.make_menubar()
		self.set_size(1, 1)
		Settings.ENABLE_CUSTOM_TITLE_BAR = True

	def set_size(self, w, h):
		dw = QDesktopWidget()
		width = dw.availableGeometry(self).width()
		height = dw.availableGeometry(self).height()
		self.resize(width * w, height * h)

	def make_menubar(self):
		# create menus	
		file = self.menubar.addMenu('File')
		# create actions
		quit = QAction(' Exit', self)
		quit.triggered.connect(self.close) 
		# add actions to menus
		file.addAction(quit)

	def close(self):
		sys.exit()

class FuelcellUI(QTabWidget):

	tintin = ['blistering barnacles', 'thundering typhoon', 'my jewels!', 'woah!']
	refelecs = fc.datums.ref_electrodes
	thermo_potentials = fc.datums.thermo_potentials
	expt_types = {'Chronopotentiometry':'cp', 'Chronoamperometry': 'ca', 'Cyclic voltammetry': 'cv', 'Linear sweep voltammetry': 'lsv', 'Electrochemical impedance spectroscopy':'eis'}
	vis_types = {'Polarization curve':0, 'Cyclic voltammogram':1, 'Linear sweep voltammogram':2, 'Nyquist plot':3}
	expt_types_rev = {y:x for x,y in expt_types.items()}
	markerstyles_rev = {Line2D.markers[m]:m for m in Line2D.filled_markers}
	# vis_types = {'Cyclic Voltammagram':'cv', 'Polarization Curve':'cp'}
	homedir = str(Path.home())
	default_figsize = (7,5)
	default_figres = 300

	headerfont = QFont()
	default_size = headerfont.pointSize()
	headerfont.setPointSize(20)
	headerfont.setBold(True)

	valuefont = QFont()
	valuefont.setBold(True)

	notefont = QFont()
	notefont.setItalic(True)
	notefont.setBold(True)

	def __init__(self, main_window):
		super().__init__()
		# self.tintin = ['blistering barnacles', 'thundering typhoon', 'my jewels!', 'woah!']
		self.window = main_window
		self.window.setCentralWidget(self)
		self.datahandler = DataHandler()
		self.vishandler = VisualHandler()
		self.uploader = UploadHandler()

		self.data_tab = self.makeTab(self.datums_layout(), 'Data Processing')
		self.visuals_tab = self.makeTab(self.visuals_layout(), 'Visualization')

		self.data_dict = {}

		self.line_dict_vis = {}

	def makeTab(self, layout, name):
		tab = QWidget()
		tab.setLayout(layout)
		self.addTab(tab, name)
		return tab

	def update_status(self, message):
		self.window.statusbar.showMessage(message, 10000)

	def close(self):
		sys.exit()

	### general use methods ###
	def set_max_width(self, widget, scale=1):
		size = widget.sizeHint()
		w = size.width()
		widget.setMaximumWidth(int(w*scale))

	def set_min_width(self, widget, scale=1):
		size = widget.sizeHint()
		w = size.width()
		widget.setMinimumWidth(int(w*scale))

	def set_max_height(self, widget, scale=1):
		size = widget.sizeHint()
		h = size.height()
		widget.setMaximumHeight(int(h*scale))

	def set_min_height(self, widget, scale=1):
		size = widget.sizeHint()
		h = size.height()
		widget.setMinimumHeight(int(h*scale))
	
	def get_all_files(self, dir, valid=None):
		allfiles = os.listdir(dir)
		files = []
		for f in allfiles:
			if os.path.isdir(os.path.join(dir, f)) or f.startswith('.'):
				continue
			elif valid:
				try:
					name, filetype = f.split('.')
				except Exception:
					continue
				if filetype.lower() not in valid:
					continue
			files.append(f)
		return files

	###################
	# Data Processing #
	###################
	### data processing layout ###
	def datums_layout(self):
		# file selection header
		self.header_data = QLabel('Selecione os dados')
		self.header_data.setFont(FuelcellUI.headerfont)
		# folder selection widgets
		self.folder_lbl_data = QLabel('Pastas')
		self.folder_txtbx_data = QLineEdit(FuelcellUI.homedir)
		self.folder_btn_data = QPushButton('Escolha pasta...')
		# file selection widgets
		self.file_lbl_data = QLabel('Arquivos')
		self.file_txtbx_data = QLineEdit()
		self.file_btn_data = QPushButton('Escolha arquivo...')
		# experiment selection header
		self.header_expt = QLabel('Parametros do experimento')
		self.header_expt.setFont(FuelcellUI.headerfont)
		# experiment selection widgets
		self.protocol_lbl = QLabel('Protocolo de processamento de dados')
		self.protocol_menu = QComboBox()
		for n in FuelcellUI.expt_types.keys():
			self.protocol_menu.addItem(n)
		self.applytoall_chkbx = QCheckBox('Aplicar para todos os arquivos')
		self.applytoall_chkbx.setCheckState(Qt.Unchecked)
		self.applytoall_chkbx.setEnabled(False)
		# column selection layout
		self.colslayout_data = self.colselction_layout_data()
		# parameters layout
		self.paramslayout_data = self.param_layout_data()
		# data processing header
		self.header_process = QLabel('Processar dados')
		self.header_process.setFont(FuelcellUI.headerfont)
		# processing button
		self.process_btn = QPushButton('Processar dados')
		# export data widgets
		self.save_chkbx_data = QCheckBox('Exportar dados processados')
		self.save_chkbx_data.setLayoutDirection(Qt.RightToLeft)
		self.save_chkbx_data.setCheckState(Qt.Unchecked)
		self.saveloc_txtbx_data = QLineEdit(self.default_saveloc_data())
		self.saveloc_btn_data = QPushButton('Escolher local...')
		# data table layout
		self.tbllayout = self.table_layout()
		# connect widgets
		self.folder_txtbx_data.textChanged.connect(self.folder_action_data)
		self.folder_btn_data.clicked.connect(self.choose_folder_data)
		self.file_txtbx_data.textChanged.connect(self.file_action_data)
		self.file_btn_data.clicked.connect(self.choose_files_data)
		self.protocol_menu.currentTextChanged.connect(self.protocol_action)
		self.process_btn.clicked.connect(self.process_action)
		self.save_chkbx_data.stateChanged.connect(self.savechkbx_action)
		self.saveloc_txtbx_data.textChanged.connect(self.saveloc_action_data)
		self.saveloc_btn_data.clicked.connect(self.choose_saveloc_data)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.header_data, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.folder_lbl_data, row, 0, Qt.AlignRight)
		layout.addWidget(self.folder_txtbx_data, row, 1)
		layout.addWidget(self.folder_btn_data, row, 2)
		row += 1
		layout.addWidget(self.file_lbl_data, row, 0, Qt.AlignRight)
		layout.addWidget(self.file_txtbx_data, row, 1)
		layout.addWidget(self.file_btn_data, row, 2)
		row += 1
		layout.addWidget(self.header_expt, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.protocol_lbl, row, 0, Qt.AlignRight)
		layout.addWidget(self.protocol_menu, row, 1,)
		layout.addWidget(self.applytoall_chkbx, row, 2)
		row += 1
		layout.addLayout(self.colslayout_data, row, 0, 1, -1, Qt.AlignLeft)
		row += 1
		layout.addLayout(self.paramslayout_data, row, 0, 1, -1, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.header_process, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.save_chkbx_data, row, 0, Qt.AlignRight)
		layout.addWidget(self.saveloc_txtbx_data, row, 1)
		layout.addWidget(self.saveloc_btn_data, row, 2)
		row += 1
		layout.addWidget(self.process_btn, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addLayout(self.tbllayout, row, 0, 1, -1, Qt.AlignHCenter)
		return layout

	def colselction_layout_data(self):
		# column selection widgets
		self.colone_lbl = QLabel('Coluna Potencial (label or index)')
		self.colone_txtbx = QLineEdit('1')
		self.coltwo_lbl = QLabel('Current column (label or index)')
		self.coltwo_txtbx = QLineEdit('2')
		# col id note
		self.colnote_lbl = QLabel('Note: Column indexing starts at 0')
		self.colnote_lbl.setFont(FuelcellUI.notefont)
		# connect widgets
		self.colone_txtbx.textChanged.connect(self.colone_action)
		self.coltwo_txtbx.textChanged.connect(self.coltwo_action)
		# build layout
		layout = QGridLayout()
		layout.addWidget(self.colone_lbl, 0, 0, Qt.AlignLeft)		
		layout.addWidget(self.colone_txtbx, 0, 1, Qt.AlignLeft)
		layout.addWidget(self.coltwo_lbl, 0, 2, Qt.AlignLeft)
		layout.addWidget(self.coltwo_txtbx, 0, 3, Qt.AlignLeft)
		layout.addWidget(self.colnote_lbl, 0, 4, Qt.AlignLeft)
		# resize widgets
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_max_width(w, 1.5)
		return layout

	def param_layout_data(self):
		# mea area widgets
		self.area_lbl = QLabel(f'MEA area [cm<sup>2</sup>]')
		self.area_txtbx = QLineEdit('5')
		# reference electrode widgets
		self.refelec_lbl = QLabel('Reference electrode')
		self.refelec_menu = QComboBox()
		for name, val in FuelcellUI.refelecs.items():
			thislabel = name.upper() + f' ({str(val)} V)'
			self.refelec_menu.addItem(thislabel)
		self.refelec_menu.addItem('custom')
		self.refelec_txtbx = QLineEdit(str(list(FuelcellUI.refelecs.values())[0]))
		self.refelec_txtbx.setEnabled(False)
		# reaction widgets
		self.rxn_lbl = QLabel('Reaction (thermodynamic Potencial)')
		self.rxn_menu = QComboBox()
		for name, val in FuelcellUI.thermo_potentials.items():
			thislabel = name.upper() + f' ({str(val)} V)'
			self.rxn_menu.addItem(thislabel)
		self.rxn_menu.addItem('custom')
		self.rxn_txtbx = QLineEdit(str(list(FuelcellUI.thermo_potentials.values())[0]))
		self.rxn_txtbx.setEnabled(False)
		# pyramid widgets
		self.pyr_lbl = QLabel('Pyramid')
		self.pyr_chkbx = QCheckBox()
		self.pyr_chkbx.setCheckState(Qt.Checked)
		# points to average
		self.ststpts_lbl = QLabel('Points to average')
		self.ststpts_txtbx = QLineEdit('300')
		# connect widgets
		self.area_txtbx.textChanged.connect(self.area_action)
		self.refelec_menu.currentTextChanged.connect(self.refelec_menu_action)
		self.refelec_txtbx.textChanged.connect(self.refelec_txtbx_action)
		self.rxn_menu.currentTextChanged.connect(self.rxn_menu_action)
		self.rxn_txtbx.textChanged.connect(self.rxn_txtbx_action)
		self.pyr_chkbx.stateChanged.connect(self.pyr_action)
		self.ststpts_txtbx.textChanged.connect(self.ststpts_action)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.area_lbl, row, 0, Qt.AlignLeft)
		layout.addWidget(self.area_txtbx, row, 1, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.refelec_lbl, row, 0, Qt.AlignLeft)
		layout.addWidget(self.refelec_menu, row, 1, Qt.AlignLeft)
		layout.addWidget(self.refelec_txtbx, row, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.rxn_lbl, row, 0, Qt.AlignLeft)
		layout.addWidget(self.rxn_menu, row, 1, Qt.AlignLeft)
		layout.addWidget(self.rxn_txtbx, row, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.pyr_lbl, row, 0, Qt.AlignLeft)
		layout.addWidget(self.pyr_chkbx, row, 1, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.ststpts_lbl, row, 0, Qt.AlignLeft)
		layout.addWidget(self.ststpts_txtbx, row, 1, Qt.AlignLeft)
		# resize widgets
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_max_width(w, 0.75)
			elif isinstance(w, QComboBox):
				self.set_max_width(w)
		return layout

	def table_layout(self):
		# table widget
		self.datatable = QTableView()
		# data selector
		self.datatable_selector = QComboBox()
		self.datatable_selector.setEnabled(False)
		# connect widgets
		self.datatable_selector.currentTextChanged.connect(self.datatable_selector_action)
		# build layout
		layout = QGridLayout()
		layout.addWidget(self.datatable, 0, 0, Qt.AlignHCenter)
		layout.addWidget(self.datatable_selector, 0, 1, Qt.AlignHCenter)
		self.set_min_width(self.datatable, 2)
		self.set_min_width(self.datatable_selector, 3)
		return layout

	### data processing actions ###
	def choose_folder_data(self):
		fd = QFileDialog()
		filepath = fd.getExistingDirectory(self, 'Pastas', FuelcellUI.homedir)
		if filepath:
			self.folder_txtbx_data.setText(filepath)
			self.file_txtbx_data.setText('')

	def choose_files_data(self):
		fd = QFileDialog()
		files, _ = fd.getOpenFileNames(self, 'Arquivos', FuelcellUI.homedir)
		if files:
			names = [os.path.basename(f) for f in files]
			folder = os.path.dirname(files[0])
			self.file_txtbx_data.setText('; '.join(names))
			self.folder_txtbx_data.setText(folder)

	def folder_action_data(self):
		try:
			folder = self.folder_txtbx_data.text()
			self.datahandler.set_folder(folder)
			self.file_action_data()
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def file_action_data(self):
		file_str = self.file_txtbx_data.text()
		folder = self.folder_txtbx_data.text()
		try:
			if not file_str:
				files = self.get_all_files(folder, valid=fc.utils.valid_types)
				self.file_txtbx_data.setText('; '.join(files))
			else:
				files = file_str.split('; ')
			files = [os.path.join(folder, f) for f in files]
			self.datahandler.set_files(files)
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def protocol_action(self):
		new_protocol = self.protocol_menu.currentText()
		protocol_code = FuelcellUI.expt_types[new_protocol]
		self.datahandler.expt_type = protocol_code
		if protocol_code == 'cv' or protocol_code == 'lsv':
			self.colone_lbl.setText('Coluna Potencial')
			self.colone_txtbx.setText('0')
			self.coltwo_lbl.setText('Current column')
			self.coltwo_txtbx.setText('1')
			self.area_txtbx.setEnabled(True)
			self.refelec_menu.setEnabled(True)
			self.rxn_menu.setEnabled(True)
			self.pyr_chkbx.setEnabled(False)
			self.ststpts_txtbx.setEnabled(False)
		elif protocol_code == 'ca' or protocol_code == 'cp':
			self.colone_lbl.setText('Coluna Potencial')
			self.colone_txtbx.setText('1')
			self.coltwo_lbl.setText('Current column')
			self.coltwo_txtbx.setText('2')
			self.area_txtbx.setEnabled(True)
			self.refelec_menu.setEnabled(True)
			self.rxn_menu.setEnabled(True)
			self.pyr_chkbx.setEnabled(True)
			self.ststpts_txtbx.setEnabled(True)
		elif protocol_code=='eis':
			self.colone_lbl.setText('Real column')
			self.colone_txtbx.setText('0')
			self.coltwo_lbl.setText('Imaginary column')
			self.coltwo_txtbx.setText('1')
			self.area_txtbx.setEnabled(False)
			self.refelec_menu.setEnabled(False)
			self.rxn_menu.setEnabled(False)
			self.pyr_chkbx.setEnabled(False)
			self.ststpts_txtbx.setEnabled(False)
	
	def colone_action(self):
		col = self.colone_txtbx.text()
		if col.isdigit():
			col = int(col)
		self.datahandler.set_colone(col)

	def coltwo_action(self):
		col = self.coltwo_txtbx.text()
		if col.isdigit():
			col = int(col)
		self.datahandler.set_coltwo(col)

	def area_action(self):
		area = self.area_txtbx.text()
		try:
			area = float(area)
			self.datahandler.set_area(area)
		except ValueError as e:
			self.update_status('MEA area must be a number')

	def refelec_menu_action(self):
		elec = self.refelec_menu.currentText()
		for name in FuelcellUI.refelecs.keys():
			if name in elec.lower():
				val = FuelcellUI.refelecs[name]
				self.refelec_txtbx.setEnabled(False)
				break
		else:
			val = 0
			self.refelec_txtbx.setEnabled(True)
		self.refelec_txtbx.setText(str(val))

	def refelec_txtbx_action(self):
		val = self.refelec_txtbx.text()
		try:
			val = float(val)
		except ValueError:
			val = 0
			self.update_status('Referência do eletrodo potencial deve ser um número')
		self.datahandler.set_refelec(val)

	def rxn_menu_action(self):
		rxn = self.rxn_menu.currentText()
		for name in FuelcellUI.thermo_potentials.keys():
			if name in rxn.lower():
				val = FuelcellUI.thermo_potentials[name]
				self.rxn_txtbx.setEnabled(False)
				break
		else:
			val = 0
			self.rxn_txtbx.setEnabled(True)
		self.rxn_txtbx.setText(str(val))

	def rxn_txtbx_action(self):
		val = self.rxn_txtbx.text()
		try:
			val = float(val)
		except ValueError:
			val = 0
			self.update_status('Termodinâmica deve ser um número.')
		self.datahandler.set_rxn(val)

	def pyr_action(self):
		state = self.pyr_chkbx.isChecked()
		self.datahandler.set_pyr(state)

	def ststpts_action(self):
		pts = self.ststpts_txtbx.text()
		try:
			pts = int(pts)
			self.datahandler.set_pts_to_avg(pts)
		except ValueError:
			self.update_status('Steady state points must be a number')

	def savechkbx_action(self):
		state = self.save_chkbx_data.isChecked()
		self.saveloc_txtbx_data.setEnabled(state)
		self.saveloc_btn_data.setEnabled(state)
		self.datahandler.set_export_data(state)

	def choose_saveloc_data(self):
		fd = QFileDialog()
		folder = fd.getExistingDirectory(self, 'Salvar Local', self.default_saveloc_data())
		if not folder:
			folder = self.default_saveloc_data()
		self.saveloc_txtbx_data.setText(folder)

	def saveloc_action_data(self):
		folder = self.saveloc_txtbx_data.text()
		self.datahandler.set_saveloc(folder)
		# self.folder_txtbx_upload.setText(folder)

	def process_action(self):
		try:
			self.datahandler.process_data()
			data = self.datahandler.get_data()
			self.vishandler.set_data(data)
			self.datatable_selector.clear()
			if data:
				self.datatable_selector.setEnabled(True)
				self.data_dict = {d.get_name():d.get_processed_data() for d in data if d.get_processed_data() is not None}
				for name in self.data_dict.keys():
					self.datatable_selector.addItem(name)
				self.datatable_selector.setCurrentText(list(self.data_dict.keys())[0])
				self.update_table(list(self.data_dict.values())[0])
				self.useexisting_chkbx_vis.setCheckState(Qt.Checked)
			else:
				self.datatable_selector.setEnabled(False)
				self.useexisting_chkbx_vis.setCheckState(Qt.Unchecked)
			self.update_status('Dados processados com sucesso')
			self.draw_plot_vis()
		except AttributeError as e:
			self.update_status('Todos os arquivos selecionados se enquadram no tipo de experimento escolhido.')
		except Exception as e:
			self.update_status('ERRO: ' + str(e))

	def datatable_selector_action(self):
		try:
			name = self.datatable_selector.currentText()
			data = self.data_dict[name]
			self.update_table(data)
		except Exception as e:
			self.update_status('ERRO: ' + str(e))

	def update_table(self, data):
		self.datamodel = TableModel(data)
		self.datatable.setModel(self.datamodel)
		header = self.datatable.horizontalHeader()
		header.setSectionResizeMode(QHeaderView.Stretch)
		for i in range(header.count()):
			w = header.sectionSize(i)
			header.setSectionResizeMode(i, QHeaderView.Interactive)
			header.resizeSection(i, w)

	def default_saveloc_data(self):
		dataloc = self.folder_txtbx_data.text()
		saveloc = os.path.join(dataloc, 'processado')
		if not os.path.exists(saveloc):
			os.mkdir(saveloc)
		return saveloc

	######################
	# Data Visualization #
	######################
	### data visualization layout ###
	def visuals_layout(self):
		# data selection header
		self.header_visdata = QLabel('Selecionar dados')
		self.header_visdata.setFont(FuelcellUI.headerfont)
		# use existing widgets
		self.useexisting_chkbx_vis = QCheckBox('Use últimos dados salvos.')
		self.useexisting_chkbx_vis.setCheckState(Qt.Unchecked)
		# folder selection widgets
		self.folder_lbl_vis = QLabel('Pasta de dados')
		self.folder_txtbx_vis = QLineEdit(FuelcellUI.homedir)
		self.folder_btn_vis = QPushButton('Escolha pasta...')
		#file selection widgets
		self.file_lbl_vis = QLabel('Arquivos de dados')
		self.file_txtbx_vis = QLineEdit()
		self.file_btn_vis = QPushButton('Escolha arquivos...')
		# load data button
		self.loaddata_btn_vis = QPushButton('Carregar ')
		#figure layout
		self.figlayout_vis = self.figure_layout_vis()
		# save plot header
		self.header_saveplot_vis = QLabel('Salvar Plot')
		self.header_saveplot_vis.setFont(FuelcellUI.headerfont)
		# save plot widgets
		self.saveloc_lbl_vis = QLabel('Save location')
		self.saveloc_txtbx_vis = QLineEdit(self.default_saveloc_vis())
		self.saveloc_btn_vis = QPushButton('Escolha local...')
		self.save_btn_vis = QPushButton('Salvar imagem')
		# connect widgets
		self.useexisting_chkbx_vis.stateChanged.connect(self.useexisting_action_vis)
		self.folder_txtbx_vis.textChanged.connect(self.folder_action_vis)
		self.folder_btn_vis.clicked.connect(self.choose_folder_vis)
		self.file_txtbx_vis.textChanged.connect(self.file_action_vis)
		self.file_btn_vis.clicked.connect(self.choose_files_vis)
		self.loaddata_btn_vis.clicked.connect(self.loaddata_action_vis)
		self.saveloc_btn_vis.clicked.connect(self.choose_saveloc_vis)
		self.save_btn_vis.clicked.connect(self.save_action_vis)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.header_visdata, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.useexisting_chkbx_vis, row, 0, 1, -1, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.folder_lbl_vis, row, 0)
		layout.addWidget(self.folder_txtbx_vis, row, 1)
		layout.addWidget(self.folder_btn_vis, row, 2)
		row += 1
		layout.addWidget(self.file_lbl_vis, row, 0)
		layout.addWidget(self.file_txtbx_vis, row, 1)
		layout.addWidget(self.file_btn_vis, row, 2)
		row += 1
		layout.addWidget(self.loaddata_btn_vis, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addLayout(self.figlayout_vis, row, 0, 1, -1, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.header_saveplot_vis, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.saveloc_lbl_vis, row, 0)
		layout.addWidget(self.saveloc_txtbx_vis, row, 1)
		layout.addWidget(self.saveloc_btn_vis, row, 2)
		row += 1
		layout.addWidget(self.save_btn_vis, row, 0, 1, -1, Qt.AlignHCenter)
		return layout

	def figure_layout_vis(self):
		# plot features header
		self.header_plotparams_vis = QLabel('Opções de plot')
		self.header_plotparams_vis.setFont(FuelcellUI.headerfont)
		# visualization selection widgets
		self.vistype_lbl = QLabel('Tipo de vizualização')
		self.vistype_menu = QComboBox()
		for name in list(FuelcellUI.vis_types.keys()):
			self.vistype_menu.addItem(name)
		# column selection layout
		self.colslayout_vis = self.colselection_layout_vis()
		# plot features
		self.plotfeatures_vis = self.plotfeatures_layout_vis()
		# actual figure
		self.figcanvas_vis  = FigureCanvasQTAgg(Figure(figsize=FuelcellUI.default_figsize))
		self.figcanvas_vis.figure.subplots()
		# line properties header
		self.header_lineprops_vis = QLabel('Opções de linha')
		self.header_lineprops_vis.setFont(FuelcellUI.headerfont)
		# line selector menu
		self.lineselector_lbl_vis = QLabel('linha')
		self.lineselector_menu_vis = QComboBox()
		# line properties layout
		self.lineprops_vis = self.lineprops_layout_vis()
		# figure properties
		self.figprops_vis = self.figprops_layout_vis()
		# connect widgets
		self.vistype_menu.currentTextChanged.connect(self.vistype_action)
		self.lineselector_menu_vis.currentTextChanged.connect(self.lineselector_action_vis)
		# build layout
		layout = QGridLayout()
		layout.addWidget(self.header_plotparams_vis, 0, 0, 1, 2, Qt.AlignHCenter)
		layout.addWidget(self.vistype_lbl, 1, 0, Qt.AlignLeft)
		layout.addWidget(self.vistype_menu, 1, 1, Qt.AlignLeft)
		layout.addLayout(self.colslayout_vis, 2, 0, 1, 2, Qt.AlignLeft)
		layout.addLayout(self.plotfeatures_vis, 3, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.figcanvas_vis, 0, 2, 4, 1, Qt.AlignHCenter)
		layout.addLayout(self.figprops_vis, 4, 2, 1, 1, Qt.AlignHCenter)
		layout.addWidget(self.header_lineprops_vis, 0, 3, 1, 2, Qt.AlignHCenter)
		layout.addWidget(self.lineselector_lbl_vis, 1, 3, Qt.AlignLeft)
		layout.addWidget(self.lineselector_menu_vis, 1, 4, Qt.AlignLeft)
		layout.addLayout(self.lineprops_vis, 2, 3, 2, 2, Qt.AlignLeft)
		self.set_min_width(self.lineselector_menu_vis, 2)
		return layout

	def colselection_layout_vis(self):
		# x column
		self.xcol_lbl_vis = QLabel('x column')
		self.xcol_txtbx_vis = QLineEdit('0')
		# y column 
		self.ycol_lbl_vis = QLabel('y column')
		self.ycol_txtbx_vis = QLineEdit('1')
		# error column
		self.ecol_lbl_vis = QLabel('error column')
		self.ecol_txtbx_vis = QLineEdit('3')
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.xcol_lbl_vis, row, 0, Qt.AlignLeft)
		layout.addWidget(self.xcol_txtbx_vis, row, 1, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.ycol_lbl_vis, row, 0, Qt.AlignLeft)
		layout.addWidget(self.ycol_txtbx_vis, row, 1, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.ecol_lbl_vis, row, 0, Qt.AlignLeft)
		layout.addWidget(self.ecol_txtbx_vis, row, 1, Qt.AlignLeft)
		# connect widgets
		self.xcol_txtbx_vis.textChanged.connect(self.xcol_action_vis)
		self.ycol_txtbx_vis.textChanged.connect(self.ycol_action_vis)
		self.ecol_txtbx_vis.textChanged.connect(self.ecol_action_vis)
		# resize widgets
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_max_width(w, 1.5)
		return layout

	def plotfeatures_layout_vis(self):
		# draw lines
		self.drawline_lbl_vis = QLabel('Desenhar linhas')
		self.drawlines_chkbx_vis = QCheckBox()
		self.drawlines_chkbx_vis.setCheckState(Qt.Unchecked)
		# draw data points
		self.drawscatter_lbl_vis = QLabel('Desenhar pontos')
		self.drawscatter_chkbx_vis = QCheckBox()
		self.drawscatter_chkbx_vis.setCheckState(Qt.Checked)
		#draw error bars
		self.drawerror_lbl_vis = QLabel('Desenhar barras de erros')
		self.drawerror_chkbx_vis = QCheckBox()
		self.drawerror_chkbx_vis.setCheckState(Qt.Unchecked)
		# raw data selector
		self.showleg_lbl_vis = QLabel('Exibir legenda')
		self.showleg_chkbx_vis = QCheckBox()
		self.showleg_chkbx_vis.setCheckState(Qt.Checked)
		self.showleg_chkbx_vis.setEnabled(True)
		# x-axis label
		self.xlabel_lbl_vis = QLabel('x-axis label')
		self.xlabel_txtbx_vis = QLineEdit('Densidade de Conrrente [$mA/cm^2$]')
		# y-axis label	
		self.ylabel_lbl_vis = QLabel('y-axis label')
		self.ylabel_txtbx_vis = QLineEdit('Potencial [V]')
		# x-axis limits
		self.xmin_lbl_vis = QLabel('x min')
		self.xmin_txtbx_vis = QLineEdit()
		self.xmax_lbl_vis = QLabel('x max')
		self.xmax_txtbx_vis = QLineEdit()
		# y-axis limits
		self.ymin_lbl_vis = QLabel('y min')
		self.ymin_txtbx_vis = QLineEdit()
		self.ymax_lbl_vis = QLabel('y max')
		self.ymax_txtbx_vis = QLineEdit()
		# clear plot
		self.clear_lbl_vis = QLabel('Limpar dados plotados')
		self.clear_btn_vis = QPushButton('Limpar Plot')
		self.clear_lbl_vis.setFont(FuelcellUI.valuefont)
		# connect widgets
		self.drawlines_chkbx_vis.stateChanged.connect(self.drawlines_action_vis)
		self.drawscatter_chkbx_vis.stateChanged.connect(self.drawscatter_action_vis)
		self.drawerror_chkbx_vis.stateChanged.connect(self.drawerror_action_vis)
		self.showleg_chkbx_vis.stateChanged.connect(self.shwowleg_action_vis)
		self.xlabel_txtbx_vis.textChanged.connect(self.xlabel_action_vis)
		self.ylabel_txtbx_vis.textChanged.connect(self.ylabel_action_vis)
		self.xmin_txtbx_vis.textChanged.connect(self.xlim_action_vis)
		self.xmax_txtbx_vis.textChanged.connect(self.xlim_action_vis)
		self.ymin_txtbx_vis.textChanged.connect(self.ylim_action_vis)
		self.ymax_txtbx_vis.textChanged.connect(self.ylim_action_vis)
		self.clear_btn_vis.clicked.connect(self.clear_action_vis)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.drawline_lbl_vis, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.drawlines_chkbx_vis, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.drawscatter_lbl_vis, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.drawscatter_chkbx_vis, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.drawerror_lbl_vis, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.drawerror_chkbx_vis, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.showleg_lbl_vis, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.showleg_chkbx_vis, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.xlabel_lbl_vis, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.xlabel_txtbx_vis, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.ylabel_lbl_vis, row, 0, 1, 2, Qt.AlignLeft)
		layout.addWidget(self.ylabel_txtbx_vis, row, 2, 1, 2, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.xmin_lbl_vis, row, 0, Qt.AlignLeft)		
		layout.addWidget(self.xmin_txtbx_vis, row, 1, Qt.AlignLeft)
		layout.addWidget(self.xmax_lbl_vis, row, 2, Qt.AlignLeft)
		layout.addWidget(self.xmax_txtbx_vis, row, 3, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.ymin_lbl_vis, row, 0, Qt.AlignLeft)		
		layout.addWidget(self.ymin_txtbx_vis, row, 1, Qt.AlignLeft)
		layout.addWidget(self.ymax_lbl_vis, row, 2, Qt.AlignLeft)
		layout.addWidget(self.ymax_txtbx_vis, row, 3, Qt.AlignLeft)
		row += 1
		layout.addWidget(self.clear_lbl_vis, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.clear_btn_vis, row, 0, 1, -1, Qt.AlignHCenter)
		# resize widgets
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_min_height(w)
				# self.set_min_width(w)
		self.set_max_width(self.xmin_txtbx_vis, 0.5)
		self.set_max_width(self.xmax_txtbx_vis, 0.5)
		self.set_max_width(self.ymin_txtbx_vis, 0.5)
		self.set_max_width(self.ymax_txtbx_vis, 0.5)
		return layout

	def figprops_layout_vis(self):
		# fig width
		self.figw_lbl_vis = QLabel('Figure width')
		self.figw_txtbx_vis = QLineEdit(str(FuelcellUI.default_figsize[0]))
		# fig height
		self.figh_lbl_vis = QLabel('Figue height')
		self.figh_txtbx_vis = QLineEdit(str(FuelcellUI.default_figsize[1]))
		# fig resolution
		self.figres_lbl_vis = QLabel('Resolução (DPI)')
		self.figres_txtbx_vis = QLineEdit(str(FuelcellUI.default_figres))
		# connect widgets
		self.figw_txtbx_vis.textChanged.connect(self.figsize_action_vis)
		self.figh_txtbx_vis.textChanged.connect(self.figsize_action_vis)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.figw_lbl_vis, row, 0, Qt.AlignHCenter)
		layout.addWidget(self.figh_lbl_vis, row, 1, Qt.AlignHCenter)
		layout.addWidget(self.figres_lbl_vis, row, 2, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.figw_txtbx_vis, row, 0, Qt.AlignHCenter)
		layout.addWidget(self.figh_txtbx_vis, row, 1, Qt.AlignHCenter)
		layout.addWidget(self.figres_txtbx_vis, row, 2, Qt.AlignHCenter)
		for i in range(layout.count()):
			w = layout.itemAt(i).widget()
			if isinstance(w, QLineEdit):
				self.set_max_width(w, 0.75)
		return layout

	def lineprops_layout_vis(self):
		# label
		self.linelbl_lbl_vis = QLabel('Legenda')
		self.linelbl_txtbx_vis = QLineEdit()
		# line color
		self.linecolor_lbl_vis = QLabel('Cor')
		self.linecolor_btn_vis = QPushButton('Escolha cor...')
		# line style
		self.linestyle_lbl_vis = QLabel('Estilo de linha')
		self.linestyle_menu_vis = QComboBox()
		for ls in Line2D.lineStyles.keys():
			if Line2D.lineStyles[ls] != '_draw_nothing'	:
				self.linestyle_menu_vis.addItem(ls)
		self.linestyle_menu_vis.addItem('Nada')
		# line width
		self.linewidth_lbl_vis = QLabel('Line width')
		self.linewidth_txtbx_vis = QDoubleSpinBox()
		self.linewidth_txtbx_vis.setDecimals(1)
		self.linewidth_txtbx_vis.setMinimum(0.1)
		self.linewidth_txtbx_vis.setSingleStep(0.5)
		self.linewidth_txtbx_vis.setValue(1)
		# marker style
		self.marekerstyle_lbl_vis = QLabel('Marker style')
		self.markerstyle_menu_vis = QComboBox()
		for ms in Line2D.filled_markers:
			self.markerstyle_menu_vis.addItem(Line2D.markers[ms])
		self.markerstyle_menu_vis.addItem('Nada')
		# marker size
		self.markersize_lbl_vis = QLabel('Marker size')
		self.markersize_txtbx_vis = QSpinBox()
		self.markersize_txtbx_vis.setMinimum(1)
		# connect widgets
		self.linelbl_txtbx_vis.textChanged.connect(self.linelbl_action_vis)
		self.linecolor_btn_vis.clicked.connect(self.linecolor_action_vis)
		self.linestyle_menu_vis.currentTextChanged.connect(self.linestyle_action_vis)
		self.linewidth_txtbx_vis.valueChanged.connect(self.linewidth_action_vis)
		self.markerstyle_menu_vis.currentTextChanged.connect(self.markerstyle_action_vis)
		self.markersize_txtbx_vis.valueChanged.connect(self.markersize_action_vis)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.linelbl_lbl_vis, row, 0)
		layout.addWidget(self.linelbl_txtbx_vis, row, 1)
		row += 1
		layout.addWidget(self.linecolor_lbl_vis, row, 0)
		layout.addWidget(self.linecolor_btn_vis, row, 1)
		row += 1
		layout.addWidget(self.linestyle_lbl_vis, row, 0)
		layout.addWidget(self.linestyle_menu_vis, row, 1)
		row += 1
		layout.addWidget(self.linewidth_lbl_vis, row, 0)
		layout.addWidget(self.linewidth_txtbx_vis, row, 1)
		row += 1
		layout.addWidget(self.marekerstyle_lbl_vis, row, 0)
		layout.addWidget(self.markerstyle_menu_vis, row, 1)
		row += 1
		layout.addWidget(self.markersize_lbl_vis, row, 0)
		layout.addWidget(self.markersize_txtbx_vis, row, 1)
		return layout
	
	### data visualization actions ###
	def useexisting_action_vis(self):
		state = self.useexisting_chkbx_vis.isChecked()
		if state:
			if not self.datahandler.get_data():
				self.update_status('Nenhum dados disponível para ser vizualizado')
				self.useexisting_chkbx_vis.setCheckState(Qt.Unchecked)
				state = False
			else:
				self.vishandler.set_data(self.datahandler.get_data())
		self.folder_lbl_vis.setEnabled(not state)
		self.folder_txtbx_vis.setEnabled(not state)
		self.folder_btn_vis.setEnabled(not state)
		self.file_lbl_vis.setEnabled(not state)
		self.file_txtbx_vis.setEnabled(not state)
		self.file_btn_vis.setEnabled(not state)
		self.loaddata_btn_vis.setEnabled(not state)
		if state:
			self.draw_plot_vis()

	def choose_folder_vis(self):
		fd = QFileDialog()
		filepath = fd.getExistingDirectory(self, 'Pasta de Dados', FuelcellUI.homedir)
		if filepath:
			self.folder_txtbx_vis.setText(filepath)
			self.file_txtbx_vis.setText('')			

	def choose_files_vis(self):
		fd = QFileDialog()
		files, _ = fd.getOpenFileNames(self, 'Arquivos', FuelcellUI.homedir)
		if files:
			names = [os.path.basename(f) for f in files]
			folder = os.path.dirname(files[0])
			self.file_txtbx_vis.setText('; '.join(names))
			self.folder_txtbx_vis.setText(folder)

	def folder_action_vis(self):
		try:
			folder = self.folder_txtbx_vis.text()
			self.vishandler.set_datafolder(folder)
			self.file_action_vis()
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def file_action_vis(self):
		file_str = self.file_txtbx_vis.text()
		folder = self.folder_txtbx_vis.text()
		try:
			if not file_str:
				files = self.get_all_files(folder, valid=fc.utils.valid_types)
				self.file_txtbx_vis.setText('; '.join(files))
			else:
				files = file_str.split('; ')
			files = [os.path.join(folder, f) for f in files]
			self.vishandler.set_datafiles(files)
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def loaddata_action_vis(self):
		try:
			self.vishandler.load_data()
			self.draw_plot_vis()
		except Exception as e:
			self.update_status('ERROR: ' + str(e))

	def vistype_action(self):
		vistype = self.vistype_menu.currentText()
		viscode = FuelcellUI.vis_types[vistype]
		if viscode == 0:
			self.xcol_lbl_vis.setText('Current Column')
			self.xcol_txtbx_vis.setText('0')
			self.ycol_lbl_vis.setText('Potential Column')
			self.ycol_txtbx_vis.setText('1')
			self.ecol_txtbx_vis.setText('3')
			self.drawlines_chkbx_vis.setCheckState(Qt.Checked)
			self.drawscatter_chkbx_vis.setCheckState(Qt.Checked)
			self.drawerror_chkbx_vis.setCheckState(Qt.Unchecked)
			self.showleg_chkbx_vis.setCheckState(Qt.Checked)
			self.xlabel_txtbx_vis.setText('Current Density [$mA/cm^2$]')
			self.ylabel_txtbx_vis.setText('Potential [V]')
		elif viscode == 1:
			self.xcol_lbl_vis.setText('Coluna Potencial')
			self.xcol_txtbx_vis.setText('1')
			self.ycol_lbl_vis.setText('Coluna Corrente')
			self.ycol_txtbx_vis.setText('0')
			self.ecol_txtbx_vis.setText('3')
			self.drawlines_chkbx_vis.setCheckState(Qt.Checked)
			self.drawscatter_chkbx_vis.setCheckState(Qt.Unchecked)
			self.drawerror_chkbx_vis.setCheckState(Qt.Unchecked)
			self.showleg_chkbx_vis.setCheckState(Qt.Checked)
			self.xlabel_txtbx_vis.setText('Potencial [V]')
			self.ylabel_txtbx_vis.setText('Densidade de Corrente [$mA/cm^2$]')
		elif viscode == 2:
			self.xcol_lbl_vis.setText('Coluna Potencial')
			self.xcol_txtbx_vis.setText('2')
			self.ycol_lbl_vis.setText('Coluna Corrente')
			self.ycol_txtbx_vis.setText('1')
			self.ecol_txtbx_vis.setText('')
			self.drawlines_chkbx_vis.setCheckState(Qt.Unchecked)
			self.drawscatter_chkbx_vis.setCheckState(Qt.Checked)
			self.drawerror_chkbx_vis.setCheckState(Qt.Unchecked)
			self.showleg_chkbx_vis.setCheckState(Qt.Checked)
			self.xlabel_txtbx_vis.setText('Sobrepotencial [V]')
			self.ylabel_txtbx_vis.setText('Densidade de Corrente [$mA/cm^2$]')
		elif viscode == 3:
			self.xcol_lbl_vis.setText('Coluna Real')
			self.xcol_txtbx_vis.setText('0')
			self.ycol_lbl_vis.setText('Coluna Imaginária')
			self.ycol_txtbx_vis.setText('1')
			self.ecol_txtbx_vis.setText('')
			self.drawlines_chkbx_vis.setCheckState(Qt.Unchecked)
			self.drawscatter_chkbx_vis.setCheckState(Qt.Checked)
			self.drawerror_chkbx_vis.setCheckState(Qt.Unchecked)
			self.showleg_chkbx_vis.setCheckState(Qt.Checked)
			self.xlabel_txtbx_vis.setText(r'$R_{Re} [\ Omega]$')
			self.ylabel_txtbx_vis.setText(r'$R_{Im} [\ Omega]$')
		self.vishandler.set_vis_code(viscode)
		if viscode == 3:
			self.useexisting_chkbx_eis.setCheckState(Qt.Checked)
			self.draw_plot_eis()
		self.draw_plot_vis()

	def xcol_action_vis(self):
		col = self.xcol_txtbx_vis.text()
		if col.isdigit():
			col = int(col)
		self.vishandler.set_xcol(col)
		self.draw_plot_vis()

	def ycol_action_vis(self):
		col = self.ycol_txtbx_vis.text()
		if col.isdigit():
			col = int(col)
		self.vishandler.set_ycol(col)
		self.draw_plot_vis()

	def ecol_action_vis(self):
		col = self.ecol_txtbx_vis.text()
		if col.isdigit():
			col = int(col)
		self.vishandler.set_ecol(col)
		self.draw_plot_vis()

	def drawlines_action_vis(self):
		state = self.drawlines_chkbx_vis.isChecked()
		self.vishandler.set_drawline(state)
		if state:
			ls = '-'
		else:
			ls = ''
		ax = self.get_ax_vis()
		lines = ax.get_lines()
		for i, l in enumerate(lines):
			if self.drawerror_chkbx_vis.isChecked() and i%3 != 0:
				continue
			l.set_linestyle(ls)
		self.figcanvas_vis.draw()

	def drawscatter_action_vis(self):
		state = self.drawscatter_chkbx_vis.isChecked()
		self.vishandler.set_drawscatter(state)
		if state:
			ms = '.'
		else:
			ms = ''
		ax = self.get_ax_vis()
		lines = ax.get_lines()
		for i, l in enumerate(lines):
			if self.drawerror_chkbx_vis.isChecked() and i%3 !=0:
				continue
			l.set_marker(ms)
		self.figcanvas_vis.draw()

	def drawerror_action_vis(self):
		state = self.drawerror_chkbx_vis.isChecked()
		self.vishandler.set_drawerr(state)
		self.draw_plot_vis()

	def shwowleg_action_vis(self):
		state = self.showleg_chkbx_vis.isChecked()
		ax = self.get_ax_vis()
		if state:
			ax.legend(loc='Melhor', edgecolor='#000000')
		else:
			ax.legend().remove()
		self.figcanvas_vis.draw()
	
	def xlabel_action_vis(self):
		new_label = self.xlabel_txtbx_vis.text()
		ax = self.get_ax_vis()
		ax.set_xlabel(new_label)
		self.figcanvas_vis.draw()

	def ylabel_action_vis(self):
		new_label = self.ylabel_txtbx_vis.text()
		ax = self.get_ax_vis()
		ax.set_ylabel(new_label)
		self.figcanvas_vis.draw()

	def xlim_action_vis(self):
		xmin_text = self.xmin_txtbx_vis.text()
		xmax_text = self.xmax_txtbx_vis.text()
		ax = self.get_ax_vis()
		try:
			xmin = float(xmin_text)
			ax.set_xbound(lower=xmin)
		except ValueError:
			self.update_status('xmin deve ser um número')
		try:
			xmax = float(xmax_text)
			ax.set_xbound(upper=xmax)
		except ValueError:
			self.update_status('xmax deve ser um número')
		self.figcanvas_vis.draw()

	def ylim_action_vis(self):
		ymin_text = self.ymin_txtbx_vis.text()
		ymax_text = self.ymax_txtbx_vis.text()
		ax = self.get_ax_vis()
		try:
			ymin = float(ymin_text)
			ax.set_ybound(lower=ymin)
		except ValueError:
			self.update_status('ymin deve ser um número')
		try:
			ymax = float(ymax_text)
			ax.set_ybound(upper=ymax)
		except ValueError:
			self.update_status('ymax deve ser um número')
		self.figcanvas_vis.draw()

	def clear_action_vis(self):
		self.vishandler.set_data([], replace=True)
		fig = self.figcanvas_vis.figure
		fig.clf()
		self.lineselector_menu_vis.clear()
		self.useexisting_chkbx_vis.setCheckState(Qt.Unchecked)

	def figsize_action_vis(self):
		fig = self.figcanvas_vis.figure
		width = self.figw_txtbx_vis.text()
		height = self.figh_txtbx_vis.text()
		try:
			width = float(width)
			height = float(height)
			fig.set_figwidth(width)
			fig.set_figheight(height)
			self.figcanvas_vis.draw()
		except ValueError:
			self.update_status('Largura e altura da imagem devem ser números.')

	def lineselector_action_vis(self):
		try:
			label = self.lineselector_menu_vis.currentText()
			data = self.line_dict_vis[label]
			line = data.get_line()
			linestyle = line.get_linestyle()
			linewidth = line.get_linewidth()
			markerstyle = line.get_marker()
			markersize = line.get_markersize()
			self.linelbl_txtbx_vis.setText(label)
			self.linestyle_menu_vis.setCurrentText(linestyle)
			self.linewidth_txtbx_vis.setValue(linewidth)
			self.markerstyle_menu_vis.setCurrentText(Line2D.markers[markerstyle])
			self.markersize_txtbx_vis.setValue(int(markersize))
		except KeyError:
			pass

	def linelbl_action_vis(self):
		try:
			old_label = self.lineselector_menu_vis.currentText()
			new_label = self.linelbl_txtbx_vis.text()
			if old_label != new_label:
				data = self.line_dict_vis[old_label]
				ax = self.get_ax_vis()
				line = data.get_line()
				line.set_label(new_label)
				data.set_label(new_label)
				self.shwowleg_action_vis()
				self.figcanvas_vis.draw()
				self.line_dict_vis = {d.get_label():d for d in self.vishandler.get_plot_data()}
				self.lineselector_menu_vis.clear()
				for n in self.line_dict_vis.keys():
					self.lineselector_menu_vis.addItem(n)
				self.lineselector_menu_vis.setCurrentText(new_label)
		except KeyError:
			pass

	def linecolor_action_vis(self):
		try:
			label = self.lineselector_menu_vis.currentText()
			data = self.line_dict_vis[label]
			line = data.get_line()
			old_color = line.get_color()
			qd = QColorDialog()
			new_color = qd.getColor(initial=QColor(old_color)).name(QColor.HexRgb)
			line.set_color(new_color)
			self.shwowleg_action_vis()
			self.figcanvas_vis.draw()
		except KeyError:
			pass

	def linestyle_action_vis(self):
		try:
			label = self.lineselector_menu_vis.currentText()
			ls = self.linestyle_menu_vis.currentText()
			data = self.line_dict_vis[label]
			line = data.get_line()
			line.set_linestyle(ls)
			self.shwowleg_action_vis()
			self.figcanvas_vis.draw()
		except KeyError:
			pass

	def linewidth_action_vis(self):
		try:
			label = self.lineselector_menu_vis.currentText()
			lw = self.linewidth_txtbx_vis.value()
			data = self.line_dict_vis[label]
			line = data.get_line()
			line.set_linewidth(lw)
			self.shwowleg_action_vis()
			self.figcanvas_vis.draw()
		except KeyError:
			pass

	def markerstyle_action_vis(self):
		try:
			label = self.lineselector_menu_vis.currentText()
			m = self.markerstyle_menu_vis.currentText()
			data = self.line_dict_vis[label]
			line = data.get_line()
			line.set_marker(FuelcellUI.markerstyles_rev[m])
			self.shwowleg_action_vis()
			self.figcanvas_vis.draw()
		except KeyError:
			pass

	def markersize_action_vis(self):
		try:
			label = self.lineselector_menu_vis.currentText()
			ms = self.markersize_txtbx_vis.value()
			data = self.line_dict_vis[label]
			line = data.get_line()
			line.set_markersize(int(ms))
			self.shwowleg_action_vis()
			self.figcanvas_vis.draw()
		except KeyError:
			pass

	def choose_saveloc_vis(self):
		fd = QFileDialog()
		fd.setViewMode(QFileDialog.Detail)
		fd.setDefaultSuffix('png')
		filename, _ = fd.getSaveFileName(self, 'Salvar Local', self.default_saveloc_vis())
		if not filename:
			filename = self.default_saveloc_vis()
		self.saveloc_txtbx_vis.setText(filename)

	def save_action_vis(self):
		try:
			fig = self.figcanvas_vis.figure
			loc = self.saveloc_txtbx_vis.text()
			dpi = self.figres_txtbx_vis.text()
			if not dpi.isdigit():
				self.update_status('A resolução da imagem deve ser um número ínteiro')
				dpi = 300
			else:
				dpi = int(dpi)
			fig.savefig(loc, dpi=dpi)
			self.update_status('Imagem salva com sucesso')
		except Exception as e:
			self.update_status('ERRO: ' + str(e))

	def draw_plot_vis(self):
		fig = self.figcanvas_vis.figure
		fig.clf()
		ax = fig.subplots()
		self.vishandler.draw_plot(ax)
		self.xlabel_txtbx_vis.setText(ax.get_xlabel())
		self.ylabel_txtbx_vis.setText(ax.get_ylabel())
		# self.xmin_txtbx_vis.setText(f'{ax.get_xlim()[0]:.2f}')
		# self.xmax_txtbx_vis.setText(f'{ax.get_xlim()[1]:.2f}')
		# self.ymin_txtbx_vis.setText(f'{ax.get_ylim()[0]:.2f}')
		# self.ymax_txtbx_vis.setText(f'{ax.get_ylim()[1]:.2f}')
		self.line_dict_vis = {d.get_label():d for d in self.vishandler.get_plot_data()}
		self.lineselector_menu_vis.clear()
		for n in self.line_dict_vis.keys():
			self.lineselector_menu_vis.addItem(n)
		self.shwowleg_action_vis()
		ax.tick_params(axis='both', direction='in')
		self.figcanvas_vis.draw()

	def get_ax_vis(self):
		fig = self.figcanvas_vis.figure
		ax = fig.get_axes()
		return ax[0]

	def default_saveloc_vis(self):
		dataloc = self.folder_txtbx_data.text()
		saveloc = os.path.join(dataloc, 'figuras')
		if not os.path.exists(saveloc):
			os.mkdir(saveloc)
		return saveloc

	###########
	# DATAHUB #
	###########
	### datahub layout ###
	def datahub_layout(self):
		layout = QGridLayout()
		# datahub header
		self.header_datahub = QLabel('Datahub Uploader')
		self.header_datahub.setFont(FuelcellUI.headerfont)
		self.set_max_height(self.header_datahub)
		# upload url
		self.uploadurl_lbl = QLabel('Datahub URL')
		self.uploadurl_txtbx = QLineEdit()
		self.uploadurl_txtbx.setEnabled(False)
		# api key
		self.apikey_lbl = QLabel('API Key')
		self.apikey_txtbx = QLineEdit()
		self.apikey_txtbx.setEnabled(False)
		# institution
		self.inst_lbl = QLabel('Instituição')
		self.inst_txtbx = QLineEdit()
		self.inst_txtbx.setEnabled(False)
		# project
		self.project_lbl = QLabel('Projeto (Nome ou ID)')
		self.project_txtbx = QLineEdit()
		self.project_txtbx.setEnabled(False)
		# package
		self.package_lbl = QLabel('Pacote')
		self.package_txtbx = QLineEdit('foobar_sg')
		self.package_txtbx.setEnabled(False)
		self.package_chkbx = QCheckBox('Use um pacote existente')
		self.package_chkbx.setCheckState(Qt.Checked)
		self.package_chkbx.setEnabled(False)
		# local folder selection
		self.folder_lbl_upload = QLabel('Local da Pasta')
		self.folder_txtbx_upload = QLineEdit(self.default_saveloc_data())
		self.folder_btn_upload = QPushButton('Escolha Posição...')
		# local file selection
		self.file_lbl_upload = QLabel('Arquivos')
		self.file_txtbx_upload = QLineEdit()
		self.file_btn_upload = QPushButton('Escolha o Arquivo...')
		# upload button
		self.upload_btn = QPushButton('Upload')
		# connect widgets
		self.folder_txtbx_upload.textChanged.connect(self.folder_action_upload)
		self.folder_btn_upload.clicked.connect(self.choose_folder_upload)
		self.file_txtbx_upload.textChanged.connect(self.file_action_upload)
		self.file_btn_upload.clicked.connect(self.choose_files_upload)
		self.upload_btn.clicked.connect(self.upload_action)
		# build layout
		layout = QGridLayout()
		row = 0
		layout.addWidget(self.header_datahub, row, 0, 1, -1, Qt.AlignHCenter)
		row += 1
		layout.addWidget(self.uploadurl_lbl, row, 0)
		layout.addWidget(self.uploadurl_txtbx, row, 1, 1, -1)
		row += 1
		layout.addWidget(self.apikey_lbl, row, 0)
		layout.addWidget(self.apikey_txtbx, row, 1, 1, -1)
		row += 1
		layout.addWidget(self.inst_lbl, row, 0)
		layout.addWidget(self.inst_txtbx, row, 1, 1, -1)
		row += 1
		layout.addWidget(self.project_lbl, row, 0)
		layout.addWidget(self.project_txtbx, row, 1, 1, -1)
		row += 1
		layout.addWidget(self.package_lbl, row, 0)
		layout.addWidget(self.package_txtbx, row, 1)
		layout.addWidget(self.package_chkbx, row, 2)
		row += 1
		layout.addWidget(self.folder_lbl_upload, row, 0)
		layout.addWidget(self.folder_txtbx_upload, row, 1)
		layout.addWidget(self.folder_btn_upload, row, 2)
		row += 1
		layout.addWidget(self.file_lbl_upload, row, 0)
		layout.addWidget(self.file_txtbx_upload, row, 1)
		layout.addWidget(self.file_btn_upload, row, 2)
		row += 1
		layout.addWidget(self.upload_btn, row, 0, 1, -1, Qt.AlignHCenter)
		return layout

	### datahub actions ###
	def choose_folder_upload(self):
		fd = QFileDialog()
		filepath = fd.getExistingDirectory(self, 'Pastas', FuelcellUI.homedir)
		if filepath:
			self.folder_txtbx_upload.setText(filepath)
			self.file_txtbx_upload.setText('')

	def choose_files_upload(self):
		fd = QFileDialog()
		files, _ = fd.getOpenFileNames(self, 'Arquivos', FuelcellUI.homedir)
		if files:
			names = [os.path.basename(f) for f in files]
			folder = os.path.dirname(files[0])
			self.file_txtbx_upload.setText('; '.join(names))
			self.folder_txtbx_upload.setText(folder)

	def folder_action_upload(self):
		try:
			folder = self.folder_txtbx_upload.text()
			self.uploader.set_basedir(folder)
			self.file_action_upload()
		except Exception as e:
			self.update_status('ERRO: ' + str(e))

	def file_action_upload(self):
		file_str = self.file_txtbx_upload.text()
		folder = self.folder_txtbx_upload.text()
		try:
			if not file_str:
				files = self.get_all_files(folder)
				self.file_txtbx_upload.setText('; '.join(files))
			else:
				files = file_str.split('; ')
			self.uploader.set_files(files)
		except Exception as e:
			self.update_status('ERRO: ' + str(e))

	def upload_action(self):
		message = self.uploader.upload()
		self.update_status(message)

import qdarkstyle

def main():
	app = QApplication(sys.argv)
	app.setStyleSheet(qdarkstyle.load_stylesheet())
	window = FuelcellWindow()
	ui = FuelcellUI(window)
	window.show()
	app.exec_()

if __name__ == "__main__":
	sys.exit(main())