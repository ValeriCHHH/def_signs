import os, shutil, fsb795, zipfile, re 

#получаем путь до архива

def search_zip(r_path):
	pattern_z = r"\w+[- ]*\w*[ -.\s]?\w*[ -.\s]?\w*.zip"
	sequence_z = str(os.listdir(r_path))
	z_search = re.search(pattern_z, sequence_z).group()
	return f'{r_path}{z_search}'

#получаем файл сертификата из архива

def get_cer():
	pattern_cer = r"\w+[- ]?\w+[ -\.]?\w+[ -\.]?\w+[ -\.]?\w+[ -\.]?\w+[ -\.]?\w+[ -\.]?\w+\.cer"
	f = open(search_zip('./'), 'rb')
	z =zipfile.ZipFile(search_zip('./'), 'r')
	zfile = zipfile.ZipFile(f, 'r')
	sequence_c = str(z.namelist())
	result_search = re.search(pattern_cer, sequence_c).group()
	for zc in zfile.namelist():
		zfile.extract(result_search, './')
		sequence_c_unzip = str(os.listdir('./'))
		result_search_c_unzip = re.search(pattern_cer, sequence_c_unzip).group()
	return f'./{result_search_c_unzip}'

#получаем информацию из сертификата и перемещаем архив в личную папку серта

def get_info():
	tk_c = fsb795.Certificate(get_cer())
	valid = tk_c.validityCert()
	sub, usr_c = tk_c.subjectCert()
	iss, dst_c = tk_c.issuerCert()
	for key in sub.keys():
		lst = {key:sub[key]}
	for key in iss.keys():
		dst = {key:iss[key]}
	sub_name = lst.get('CN')
	dst_name = dst.get('CN')
	end_date = valid['not_after']
	clear_dn = str(dst_name).replace(' ', '_')
	clear_sn = str(sub_name).replace(' ', '_')
	new_p_cer_dir = str(f'./{clear_dn}/{clear_sn}')
	if not os.path.exists(new_p_cer_dir):
		os.makedirs(new_p_cer_dir, 0o777) 
	shutil.copy(search_zip('./'), str(new_p_cer_dir))

get_info()