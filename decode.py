#!/usr/bin/env python3
import os, re

def main():
	dir_r = os.path.dirname(os.path.realpath(__file__))
	dir_encoded = os.path.join(dir_r, 'def')
	print('Encoded dir path: ', dir_encoded)
	dir_decoded = os.path.join(dir_r, 'def_decoded')
	print('Decoded dir path: ', dir_decoded)

	for item in os.listdir(dir_decoded):
		path = os.path.join(dir_decoded, item)
		print('Deliting old: ', path)
		os.remove(path)

	for path, dirs, files in os.walk(dir_encoded):
		for file_name in files:
			try:
				file_in = os.path.join(path, file_name)
				file_out = os.path.join(dir_decoded, os.path.relpath(file_in, start=dir_encoded))
				print('Processing: ', file_in, ' -> ', file_out)
				with open(file_in, mode='rb') as f_in:
					s = f_in.read()
					s = s.decode(encoding='utf-8', errors='ignore')
					s = re.sub(r'\x00\x01.', r'', s, flags=re.DOTALL) # Replace 1-symbol strings
					s = re.sub(r'\0[\x00-\xFF]', r'\n\n', s) # Split strings
					s = re.sub(r'[\x00-\x08\x0B-\x1F\x7F]', r'', s) # Replace specials, except [\t\n]
					with open(file_out, mode='w', encoding='utf-8') as f_out:
						f_out.write(s)
			except Exception as e:
				print(e)
			

if __name__ == '__main__':
	main()