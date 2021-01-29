import shutil
import os

list_big = ['raw']
list_work = ['blender', 'modeling', 'texture', 'motion']
list_delete = ['jpg', 'jpgm']


def copy_in_dir(src, dst):
	for f in os.listdir(src):
		shutil.copy2(f, dst)


def backup(src, dst_big_root, dst_work_root):
	for f in os.listdir(src):
		fl = f.lower()
		if fl in list_delete:
			print('del : ' + f)
		elif fl in list_big:
			print('big : ' + f)
			src_dir = os.path.join(src, fl)
			dst_dir = os.path.join(dst_big_root, fl)
			print(src_dir)
			print(dst_dir)
			os.mkdir(dst_dir)
			copy_in_dir(src_dir, dst_dir)
		elif fl in list_work:
			print('work : ' + f)
			src_dir = os.path.join(src, fl)
			dst_dir = os.path.join(dst_work_root, fl)
			print(src_dir)
			print(dst_dir)
			os.mkdir(dst_dir)
			copy_in_dir(src_dir, dst_dir)
		else:
			continue


def run(src, dst_big, dst_work):
	for f in os.listdir(src):
		cid_path = os.path.join(src, f)  					# src_root/content_id
		if os.path.isdir(cid_path):
			dst_big_c_id = os.path.join(dst_big, f)			# raw/content_id
			dst_work_c_id = os.path.join(dst_work, f)		# work/content_id
			if not os.path.exists(dst_big_c_id):
				os.mkdir(dst_big_c_id)
			if not os.path.exists(dst_work_c_id):
				os.mkdir(dst_work_c_id)

			backup(cid_path, dst_big_c_id, dst_work_c_id)


run('/Users/vrism/work/tester/python/shell_util/sh_src',
	'/Users/vrism/work/tester/python/shell_util/sh_dst_raw',
	'/Users/vrism/work/tester/python/shell_util/sh_dst_work')
