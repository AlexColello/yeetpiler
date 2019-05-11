import sys, getopt, os, traceback
from yeet_generator import YeetGenerator
import parser


def main(argv):
	inputfile = ''
	outputfile = ''

	try:
		opts, args = getopt.getopt(argv,"yi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('Failed with arguments', argv)
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-y':
			print('Writing fully yeeted file')
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	if inputfile == '':
		print('Please enter a file to be yeeted.')
		sys.exit(2)
	if outputfile == '':
		print('Please enter the location to yeet to.')
		sys.exit(2)


	inputfile = os.path.abspath(inputfile)

	if not os.path.isfile(inputfile): # isdir for directory
		print('The file {} does not exist.'.format(inputfile))
		sys.exit(1)

	with open(inputfile, "r") as fi:
		lines = fi.readlines()

	line_tokens = []
	indentation = []
	for line in lines:
		tokens = parser.get_tokens(line)
		#print(tokens)
		line_tokens.append(tokens)
		indentation.append(parser.get_indentation(line))

	outputfile = os.path.abspath(outputfile)
	yeetfile = os.path.join(os.path.dirname(outputfile), 'yeet.h')

	yeet_generator = YeetGenerator()

	try:
		with open(outputfile, "w") as fo:

			yeet_table = {}

			fo.write('#include "yeet.h"\n')

			for tokens, indent in zip(line_tokens, indentation):
				fo.write(indent)
				tokens_iter = iter(tokens)
				for token in tokens_iter:
					
					if len(token) != 0 and token[0] == '#':
						yeet = token + next(tokens_iter)
					elif token in yeet_table:
						yeet = yeet_table[token]
					else:
						yeet = yeet_generator.next()
						yeet_table[token] = yeet

					fo.write(yeet + ' ')
				fo.write('\n')

	except OSError as e:
		print('Could not yeet file {} to {}'.format(inputfile, outputfile))
		print(e)

	try:

		with open(yeetfile, "w") as fo:

			for token in yeet_table.keys():
				fo.write('#define {} {}\n'.format(yeet_table[token], token))

	except OSError as e:
		print('Could not yeet file yeet.h to {}'.format(yeetfile))
		print(e)


if __name__ == "__main__":
    main(sys.argv[1:])