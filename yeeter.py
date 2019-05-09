import sys, getopt
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
    	print('Please enter where to yeet to.')
    	sys.exit(2)


if __name__ == "__main__":
   main(sys.argv[1:])