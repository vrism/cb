import shutil
import os
import logging
import json
import threading
import time

# list_big = ['raw']
# list_etc = ['blender', 'modeling', 'texture', 'motion']
# list_del = ['jpg', 'jpgm']

CONFIG_JSON = 'config.json'


class ConfigJson:
	BIG = "big"
	ETC = "etc"
	DEL = "del"


stop = False


def copy_content(src, dst, func):
	global stop
	i = 1
	num_files = sum(1 for item in os.listdir(src) if os.path.isfile(os.path.join(src, item)))
	for f in os.listdir(src):
		if stop:
			break
		src_file = os.path.join(src, f)
		if not os.path.isfile(src_file):
			continue
		shutil.copy2(src_file, dst)
		if func is not None:
			msg = '(%d/%d) files in %s transmitted.' % (i, num_files, src)
			func(msg)
			i += 1


def validate_dir(file, src, dst):
	src_dir = os.path.join(src, file)
	dst_dir = os.path.join(dst, file)
	if not os.path.exists(dst_dir):
		os.mkdir(dst_dir)
	return src_dir, dst_dir


def backup(src, dst_big, dst_etc, func):
	cf = open(CONFIG_JSON, 'r')
	config = json.load(cf)
	list_big = config[ConfigJson.BIG]
	list_etc = config[ConfigJson.ETC]
	list_del = config[ConfigJson.DEL]

	global stop
	for f in os.listdir(src):
		if stop:
			break
		fl = f.lower()
		if fl in list_big:
			src_dir, dst_dir = validate_dir(fl, src, dst_big)
			copy_content(src_dir, dst_dir, func)
		elif fl in list_etc:
			src_dir, dst_dir = validate_dir(fl, src, dst_etc)
			copy_content(src_dir, dst_dir, func)
		elif fl in list_del:
			# todo
			continue
		else:
			continue


def run(src_root, dst_big, dst_etc, callback):
	global stop

	if not os.path.exists(src_root):
		return
	if not os.path.exists(dst_big):
		return
	if not os.path.exists(dst_etc):
		return

	callback("Starting...")
	for i in range(3):
		if stop:
			break
		callback(str(i + 1))
		time.sleep(1)
	stop = False
	callback("Done...", False)
	return

	logger = logging.getLogger()

	try:
		for file in os.listdir(src_root):
			if stop:
				break
			src_cid = os.path.join(src_root, file)				# src_root/{content_id}
			if os.path.isdir(src_cid):
				dst_big_cid = os.path.join(dst_big, file)		# dst_big/{content_id}
				dst_etc_cid = os.path.join(dst_etc, file)		# dst_etc/{content_id}

				if not os.path.exists(dst_big_cid):
					os.mkdir(dst_big_cid)
				if not os.path.exists(dst_etc_cid):
					os.mkdir(dst_etc_cid)

				backup(src_cid, dst_big_cid, dst_etc_cid, callback)
	except Exception as e:
		logger.exception(e)
		print(e)

	stop = False
	callback('Done.', False)
