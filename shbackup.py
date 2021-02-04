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
	DEPTH = "depth"


stop = False


def callback_status(func, i, num_files, src):
	if func is not None:
		msg = '(%d/%d) files copied from %s.' % (i, num_files, src)
		func(msg, True)
	else:
		pass


def copy_all(src, dst, func):
	global stop
	i = 1
	num_files = sum(1 for item in os.listdir(src) if os.path.isfile(os.path.join(src, item)))
	for file in os.listdir(src):
		if stop:
			break
		else:
			src_file = os.path.join(src, file)
			if os.path.isfile(src_file):
				shutil.copy2(src_file, dst)
				callback_status(func, i, num_files, src)
				i += 1
			elif os.path.isdir(src_file):
				src_sub, dst_sub = validate_dir(file, src, dst)
				copy_all(src_sub, dst_sub, func)
			else:
				pass


def validate_dir(file, src, dst):
	src_dir = os.path.join(src, file)
	dst_dir = os.path.join(dst, file)
	if not os.path.exists(dst_dir):
		os.mkdir(dst_dir)
	else:
		pass
	return src_dir, dst_dir


def sync_dir(src, dst_big, dst_etc, func):
	cf = open(CONFIG_JSON, 'r')
	conf = json.load(cf)
	dirs_big = list(map(lambda x: x.lower(), conf[JsonConfig.BIG]))
	dirs_del = list(map(lambda x: x.lower(), conf[JsonConfig.DEL]))
	# list_etc = list(map(lambda x: x.lower(), conf[JsonConfig.ETC]))
	delete = conf[JsonConfig.DELETE]

	for f_name in os.listdir(src):
		f_name_l = f_name.lower()
		if f_name_l in dirs_del:
			if delete:
				src_sub = os.path.join(src, f_name)
				shutil.rmtree(src_sub)
			else:
				pass
		elif f_name_l in dirs_big:
			# per file
			src_sub, dst_sub = validate_dir(f_name, src, dst_big)
			copy_all(src_sub, dst_sub, func)
			# # per directory
			# src_sub = os.path.join(src, f_name)
			# dst_sub = os.path.join(dst_big, f_name)
			# # fail if dst_sub exists.
			# shutil.copytree(src_sub, dst_sub)
		else:
			# per file
			src_sub, dst_sub = validate_dir(f_name, src, dst_etc)
			copy_all(src_sub, dst_sub, func)
			# # per directory
			# src_sub = os.path.join(src, f_name)
			# dst_sub = os.path.join(dst_etc, f_name)
			# # fail if dst_sub exists.
			# shutil.copytree(src_sub, dst_sub)


def sync_path(depth_level, src, dst_big, dst_etc, callback):
	for file in os.listdir(src):
		if os.path.isdir(src):
			src_sub = os.path.join(src, file)
			big_sub = os.path.join(dst_big, file)
			etc_sub = os.path.join(dst_etc, file)

			if not os.path.exists(big_sub):
				os.mkdir(big_sub)
			if not os.path.exists(etc_sub):
				os.mkdir(etc_sub)

			if depth_level > 0:
				sync_path(depth_level - 1,
						  src_sub,
						  big_sub, etc_sub, callback)
			else:
				sync_dir(src_sub, big_sub, etc_sub, callback)
		else:
			pass


def run(src, dst_big, dst_etc, callback):
	if not os.path.exists(src) or \
	   not os.path.exists(dst_big) or \
	   not os.path.exists(dst_etc):
		callback("Failed. err = Invalid Path.", False)
		return

	global stop

	msg = 'Done.'
	try:
		file = open(CONFIG_JSON, 'r')
		conf = json.load(file)
		depth = conf[JsonConfig.DEPTH]

		sync_path(depth, src, dst_big, dst_etc, callback)
	except Exception as e:
		logging.getLogger().exception(e)
		print(e)
		msg = e

	stop = False
	callback(msg, False)


def cb_func(msg, running):
	print(msg)


run(os.path.join(os.getcwd(), 'sh_src'),
	os.path.join(os.getcwd(), 'sh_dst_raw'),
	os.path.join(os.getcwd(), 'sh_dst_etc'), cb_func)
