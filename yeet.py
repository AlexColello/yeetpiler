import sys, getopt, os, traceback, glob
from yeet_generator import YeetGenerator
import parser


def main(argv):
	input_file = ''
	output_directory = ''

	try:
		opts, args = getopt.getopt(argv,"ri:o:",["ifile=","odir="])
	except getopt.GetoptError:
		print('Failed with arguments', argv)
		sys.exit(2)

	recurse = False
	for opt, arg in opts:
		if opt == '-r':
			recurse = True
		elif opt in ("-i", "--ifile"):
			input_file = arg
		elif opt in ("-o", "--odir"):
			output_directory = arg

	if input_file == '':
		# print('Please enter a file to be yeeted.')
		# sys.exit(2)
		input_file = '.'
	if output_directory == '':
		# print('Please enter the location to yeet to.')
		# sys.exit(2)
		output_directory = './yeet/'
		#os.path.dirname

	input_path = os.path.abspath(input_file)
	output_directory = os.path.abspath(output_directory)

	if not os.path.exists(input_path):
		print('The input path {} does not exist.'.format(input_path))
		sys.exit(1)

	try:
		os.makedirs(output_directory, exist_ok=True)
	except OSError as e:
		print('Could not create directory {}'.format(output_directory))
		print(e)
		sys.exit(i)

	inputs = []
	if os.path.isdir(input_path):
		input_directory = input_path
		for extension in ['h', 'hpp', 'c', 'cpp']:
			
			if recurse: # Check input and sub directories
				path = os.path.join(input_path, '**/*.' + extension)
				files = glob.glob(path, recursive=True)
			else:
				# Check input directory
				path = os.path.join(input_path, '*.' + extension)
				files = glob.glob(path)
			
			inputs.extend(files)
	else:
		input_directory = os.path.dirname(input_path)
		inputs.append(input_path)

	for input_file in inputs:

		with open(input_file, "r") as fi:
			lines = fi.readlines()

		line_tokens = []
		indentation = []
		for line in lines:
			tokens = parser.get_tokens(line)
			line_tokens.append(tokens)
			indentation.append(parser.get_indentation(line))

		file_name = input_file.replace(input_directory, '')[1:]
		output_file_path = os.path.join(output_directory, file_name)

		yeet_generator = YeetGenerator()
		yeet_table = {}

		try:
			os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
			with open(output_file_path, "w") as fo:

				fo.write('#include "yeet.h"\n')

				for tokens, indent in zip(line_tokens, indentation):
					fo.write(indent)
					tokens_iter = iter(tokens)
					for token in tokens_iter:
						
						if token in ['//', '/*', '*/']:
							yeet = token
						elif len(token) != 0 and token[0] == '#':
							yeet = token + next(tokens_iter)
						elif token in yeet_table:
							yeet = yeet_table[token]
						else:
							yeet = yeet_generator.next()
							yeet_table[token] = yeet

						fo.write(yeet + ' ')
					fo.write('\n')

		except OSError as e:
			print('Could not yeet file {} to {}'.format(input_file, output_file_path))
			print(e)


	try:
		yeetfile = os.path.join(output_directory, 'yeet.h')
		with open(yeetfile, "w") as fo:

			for token in yeet_table.keys():
				fo.write('#define {} {}\n'.format(yeet_table[token], token))

	except OSError as e:
		print('Could not yeet file yeet.h to {}'.format(yeetfile))
		print(e)


if __name__ == "__main__":
    main(sys.argv[1:])