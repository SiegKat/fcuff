import numpy as np
import pandas as pd
import os
import re
import logging

from fcuff.model import Datum

_log = logging.getLogger(__name__)
_log_fmt = "%(levelname)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=_log_fmt)

valid_types = ['csv', 'xls', 'xlsx', 'txt']
export_types = ['csv', 'xls', 'xlsx']
excel_types = ['xls', 'xlsx']
csv_types = ['csv', 'txt']
dlm_default = '\t'
default_savetype = 'csv'
label_dict = {'v':'v', 'ma':'i', 'a':'i', 's':'t', 'mv':'v', 'v vs. sce':'v', 'mv vs. sce':'v', 'v vs. she':'v', 'mv vs. she':'v'}
default_names = ['tintin', 'snowy', 'haddock', 'calculus', 'castafiore', 'thomson', 'thompson']

def check_type(filetype):

	filetype = filetype.lower().replace('.', '')
	if filetype not in valid_types:
		raise ValueError('Arquivos aceitos ' + ', '.join(valid_types))
	return filetype

def check_export_type(filetype):

	filetype = filetype.lower().replace('.','')
	if filetype not in export_types:
		_log.warning(filetype + 'não é um dos formatos aceitos. Os formatos disponíveis para exportação são: ' + ', '.join(export_types) + '. Exportando dados com formato csv.')
		filetype = 'csv'
	return filetype

def check_list(var):

	result = (type(var) == list) or (type(var) == np.ndarray)
	return result

def check_dict(var):

	result = type(var) == dict
	return result

def check_str(var):

	result = type(var) == str
	return result

def check_float(var):

	result = type(var) == float
	return result

def check_int(var):

	result = type(var) == int
	return result

def check_scalar(var):

	try:
		len(var)
		return False
	except:
		return True

def check_savedir(folder):

	if os.path.exists(folder):
		path = os.path.realpath(folder)
	else:
		try:
			os.mkdir(folder)
			path = os.path.realpath(folder)
		except FileNotFoundError:
			_log.warning('Não foi possível acessar ' + folder + '. Salvando os dados no atual diretório.')
			if os.path.exists('processado'):
				path = os.path.realpath('processado')
			else:
				os.mkdir('processado')
				path = os.path.realpath('processado')
	return path

def check_labels(data):

	cols = [c.lower() for c in data.columns]
	newcols = []
	for c in cols:
		try:
			units = c.split('/')[1]
			if units == 'ohm':
				if 're' in c:
					newcols.append('real')
				elif 'im' in c:
					newcols.append('imag')
				else:
					newcols.append(c)
			elif units in label_dict.keys():
				newcols.append(label_dict[units])
			else:
				newcols.append(c)
		except Exception:
			newcols.append(c)
	return newcols

def get_files(path=None, pattern='', filetype='', files=None):

	if files is None:
		files = os.listdir(path)
	files.sort()
	if pattern:
		files = [f for f in files if re.match(pattern, f)]
	if filetype:
		filetype = filetype.lower().replace('.', '')
		files = [f for f in files if re.match(r'.*\.'+filetype, f)]
	return files

def read_file(filename, dlm=dlm_default):

	data = name = None	
	try:
		name = os.path.basename(filename)
		name, filetype = name.split('.')
		filetype = check_type(filetype)
		if filetype in excel_types:
			data = pd.read_excel(filename)
		elif filetype in csv_types:
			if filetype == 'csv':
				data = pd.read_csv(filename)
			elif filetype == 'txt':
				data = pd.read_csv(filename, delimiter=dlm)
		return Datum(name, data)
	except:
		if not os.path.isdir(filename):
			if filename.split('.')[0] in valid_types:
				_log.warning(f'Não foi possível ler {os.path.basename(filename)}')
	return None

def get_testdir():
	fcdir = os.path.dirname(os.path.realpath(__file__))
	datapath = os.path.join(fcdir, 'testdata')
	return datapath

def save_data(data, filename=None, folder=None):

	if filename:
		path, name = os.path.split(filename)
		name, fmt = name.split('.')
		filetype = check_export_type(fmt)
		name = name + '.' + filetype
	else:
		name = np.random.choice(default_names) + str(np.random.randint(100))
		if folder:
			path = folder
		else:
			path = 'processado'
		filetype = default_savetype
		_log.warning('Nome do arquivo não específicado. Salvando os dados como ' + name + '.' + filetype)
	if path:
		savedir = check_savedir(path)
	elif folder:
		savedir = check_savedir(folder)
	else:
		if os.path.exists('processado'):
			savedir = os.path.realpath('processado')
		else:
			os.mkdir('processado')
			savedir = os.path.realpath('processado')
	full_path = os.path.join(savedir, name)
	if os.path.exists(full_path):
		while os.path.exists(full_path):
			name = name.replace('.', str(np.random.randint(1000))+'.')
			full_path = os.path.join(savedir, name)
		_log.warning('Salvados os dados como ' + name + ' para evitar sob escrever arquivo criado anteriormente.')
	if filetype in excel_types:
		data.to_excel(full_path, index=False)
	else:
		data.to_csv(full_path, index=False)
