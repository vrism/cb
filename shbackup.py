import shutil
import os
import logging
import json
import threading
import time


CONFIG_JSON = 'conf/config.json'


class JsonConfig:
	BIG = "big"
	ETC = "etc"
	DEL = "del"
	DELETE = "delete"


stop = False


def copy_files(src, dst, func):
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


def backup_dir(src, dst_big, dst_etc, func):
	cf = open(CONFIG_JSON, 'r')
	config = json.load(cf)
	list_big = config[JsonConfig.BIG]
	list_etc = config[JsonConfig.ETC]
	list_del = config[JsonConfig.DEL]

	global stop
	for f in os.listdir(src):
		if stop:
			break
		fl = f.lower()
		if fl in list_big:
			src_dir, dst_dir = validate_dir(fl, src, dst_big)
			copy_files(src_dir, dst_dir, func)
		elif fl in list_etc:
			src_dir, dst_dir = validate_dir(fl, src, dst_etc)
			copy_files(src_dir, dst_dir, func)
		elif fl in list_del:
			if config[JsonConfig.DELETE]:
				src_dir, dst_dir = validate_dir(fl, src, dst_etc)
				shutil.rmtree(src_dir)
		else:
			continue


def run(src_root, dst_big, dst_etc, callback):
	if not os.path.exists(src_root) or \
	   not os.path.exists(dst_big) or \
	   not os.path.exists(dst_etc):
		callback("Failed. err = Invalid Path.", False)
		return

	global stop

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
				backup_dir(src_cid, dst_big_cid, dst_etc_cid, callback)
			else:
				pass

	except Exception as e:
		logger.exception(e)
		print(e)

	stop = False
	callback('Done.', False)
