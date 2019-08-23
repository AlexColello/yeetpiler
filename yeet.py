import sys, getopt, os, traceback, glob
from word_generator import YeetGenerator
import parser
from chardet.universaldetector import UniversalDetector

def yeet_file(file_string, yeet_table, yeet_generator):

	file_tokens = parser.parse_file(file_string)

	yeeted_file_string = ''

	for token, yeetable in file_tokens:

		if not yeetable:

			yeeted_file_string += token

		else:

			if token not in yeet_table:
				yeet_table[token] = yeet_generator.next()
				
			yeeted_file_string += '{} '.format(yeet_table[token])

	return yeeted_file_string

def get_yeet_path(root_directory, file_path):
	relative_path = file_path.replace(root_directory, '') 

	depth = relative_path.count('/') - 1

	retval = '../'*depth
	retval += 'yeet.h'

	return retval

def main(argv):
	
	# Collect command options
	try:
		opts, args = getopt.getopt(argv,"ri:o:",["ifile=","odir="])
	except getopt.GetoptError:
		print('Failed with arguments', argv)
		sys.exit(2)

	# Read command options
	input_file = ''
	output_directory = ''
	recurse = False
	for opt, arg in opts:
		if opt == '-r':
			recurse = True
		elif opt in ("-i", "--ifile"):
			input_file = arg
		elif opt in ("-o", "--odir"):
			output_directory = arg

	# Set default values
	if input_file == '':
		input_file = '.'
	if output_directory == '':
		output_directory = './yeet/'

	# Determine absolute paths
	input_path = os.path.abspath(input_file)
	output_directory = os.path.abspath(output_directory)

	# Make sure the input file or directory exists
	if not os.path.exists(input_path):
		print('The input path {} does not exist.'.format(input_path))
		sys.exit(1)

	# Determine which files will be used as input
	inputs = []
	if os.path.isdir(input_path):
		input_directory = input_path
		for extension in ('h', 'hpp', 'c', 'cpp'):
			
			if recurse: # Check input and sub directories
				path = os.path.join(input_path, '**/*.' + extension)
				files = glob.glob(path, recursive=True)
			else:
				# Check input directory only
				path = os.path.join(input_path, '*.' + extension)
				files = glob.glob(path)
			
			inputs.extend(files)
	else:
		input_directory = os.path.dirname(input_path)
		inputs.append(input_path)

	yeet_table = {}
	yeet_generator = YeetGenerator()

	detector = UniversalDetector()
	for input_file in inputs:

		print('Yeeting {}'.format(input_file))

		# Attempt to find the encoding of the file that is being read.
		try:
			detector.reset()
			for line in open(input_file, 'rb'):
				detector.feed(line)
				if detector.done: break
			detector.close()
		except UnicodeDecodeError:
			print('Could not decode file {}'.format(input_file))
			detector.close()
			continue

		try:
			with open(input_file, "r", encoding=detector.result['encoding']) as fi:
				file_string = fi.read()
		except UnicodeDecodeError:
			print('Could not read file {} \n Expected encode was: {}'.format(input_file, detector.result['encoding']))
			continue

		yeeted_file_string = yeet_file(file_string, yeet_table, yeet_generator)

		file_name = input_file.replace(input_directory, '')[1:]
		output_file_path = os.path.join(output_directory, file_name)

		try:
			os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

			yeet_header_path = get_yeet_path(output_directory, output_file_path)

			with open(output_file_path, "w") as fo:
				fo.write('#include "{}"\n'.format(yeet_header_path))
				fo.write(yeeted_file_string)

		except OSError as e:
			print('Could not yeet file {} to {}'.format(input_file, output_file_path))
			print(e)



	# Output header file with the macro definitions for all of the input files
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