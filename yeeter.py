import sys, getopt, os, traceback
from yeet_generator import YeetGenerator

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

	outputfile = os.path.abspath(outputfile)

	try:
		with open(inputfile, "r") as fi, open(outputfile, "w") as fo:
			print(fi.read())

	except OSError as e:
		print('Could not yeet file {} to {}'.format(inputfile, outputfile))
		print(e)



if __name__ == "__main__":
    main(sys.argv[1:])