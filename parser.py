
import string

two_character_operators = [
	'++', '--',
	'==', '!=', '>=', '<=',
	'&&', '||',
	'<<', '>>',
	'+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=',
	'->', '.*',
	'::', 
	'//', '/*', '*/'
]

three_character_operators = [
	'<<=', '>>=', '...', '->*'
]

def is_delimiter(char):
	return char not in string.ascii_letters and char not in string.digits and char != '_'

def get_indentation(line):
	return line.replace(line.lstrip(), '').replace('\n', '')

def get_tokens(line):

	left = 0
	right = 0
	token_start = -1
	tokens = []

	while left <= right and right < len(line):

		if is_delimiter(line[right]):
			token = line[left:right]
			if token != '':
				tokens.append(token)
			if line[right] == '"':
				string_val = '"'
				right += 1
				while right < len(line) and line[right] != '"':
					string_val += line[right]
					right += 1
				if not right < len(line):
					string_val += '"'
				tokens.append(string_val)
			elif line[right] not in string.whitespace:

				if right + 2 < len(line):
					val = line[right:right+3]
					if val in three_character_operators:
						tokens.append(val)
						right += 3
						left = right
						continue

				if right + 1 < len(line):
					val = line[right:right+2]
					if val in two_character_operators:
						tokens.append(val)
						right += 2
						left = right
						continue

				tokens.append(line[right])

			right += 1
			left = right

		else:
			right += 1

	return tokens


	

