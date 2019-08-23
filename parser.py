
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
	return char not in string.ascii_letters and char not in string.digits and char not in '_$'

def parse_indentation(file_string, starting_index):

	assert file_string[starting_index] == '\n'

	indent_val = ''
	current_index = starting_index
	while current_index < len(file_string) and file_string[current_index] in string.whitespace:
		indent_val += file_string[current_index]
		current_index += 1

	return indent_val

def parse_multi_line_comment(file_string, starting_index):

	assert file_string[starting_index:starting_index+2] == '/*'

	comment_val = ''
	current_index = starting_index
	while file_string[current_index:current_index+2] != '*/':
		comment_val += file_string[current_index]
		current_index += 1
	comment_val += '*/'

	return comment_val

def parse_single_line_comment(file_string, starting_index):

	assert file_string[starting_index:starting_index+2] == '//'

	comment_val = ''
	current_index = starting_index
	while current_index < len(file_string) and file_string[current_index] != '\n':
		comment_val += file_string[current_index]
		current_index += 1

	comment_val += '\n'

	return comment_val

def parse_string_literal(file_string, starting_index):

	assert file_string[starting_index] == '"'

	string_val = '"'
	current_index = starting_index + 1
	while file_string[current_index] != '"' or (file_string[current_index-1] == '\\' and file_string[current_index-2] != '\\'):
		string_val += file_string[current_index]
		current_index += 1
	string_val += '"'

	return string_val

def parse_character_literal(file_string, starting_index):

	assert file_string[starting_index] == '\''

	character_val = '\''
	current_index = starting_index + 1
	while file_string[current_index] != '\'' or (file_string[current_index-1] == '\\' and file_string[current_index-2] != '\\'):
		character_val += file_string[current_index]
		current_index += 1
	character_val += '\''

	return character_val

def parse_delimiter(file_string, starting_index):

	if starting_index + 2 < len(file_string):
		val = file_string[starting_index:starting_index+3]
		if val in three_character_operators:
			return val

	if starting_index + 1 < len(file_string):
		val = file_string[starting_index:starting_index+2]
		if val in two_character_operators:
			return val

	return file_string[starting_index]

def parse_precompiler_command(file_string, starting_index):

	assert file_string[starting_index] == '#'

	command_val = '#'
	current_index = starting_index + 1

	# Corner case for the precompiler concat comand '##'.
	if file_string[current_index] == '#':
		return '##'

	while file_string[current_index] in string.whitespace:
		command_val += file_string[current_index]
		current_index += 1

	while current_index < len(file_string) and not is_delimiter(file_string[current_index]):
		command_val += file_string[current_index]
		current_index += 1

	# Corner case for the #error command.
	if command_val.endswith('error'):
		while current_index < len(file_string) and (file_string[current_index] != '\n' or file_string[current_index-1] == '\\'):
			command_val += file_string[current_index]
			current_index += 1

	return command_val

def parse_file(file_string):

	retval = ''

	current_token = ''
	current_index = 0
	tokens = []

	while current_index < len(file_string):

		if is_delimiter(file_string[current_index]):

			if current_token != '':
				tokens.append((current_token, True))
				current_token = ''

			# Corner case where a new line character is escaped for something lika a multi-line preprocessor command.		
			if file_string[current_index] == '\\' and file_string[current_index+1] == '\n':
				
				indent_val = parse_indentation(file_string, current_index+1)
				current_index += len(indent_val) + 1
				tokens.append(('\\' + indent_val, False))

			elif file_string[current_index] == '#':

				command_val = parse_precompiler_command(file_string, current_index)
				current_index += len(command_val)
				tokens.append((command_val + ' ', False))

			elif file_string[current_index] == '"':

				string_val = parse_string_literal(file_string, current_index)
				current_index += len(string_val)
				tokens.append((string_val, True))

			elif file_string[current_index] == '\'':

				string_val = parse_character_literal(file_string, current_index)
				current_index += len(string_val)
				tokens.append((string_val, True))

			elif current_index + 2 < len(file_string) and file_string[current_index:current_index+2] == '//':

				single_line_comment_val = parse_single_line_comment(file_string, current_index)
				current_index += len(single_line_comment_val)
				tokens.append((single_line_comment_val, False))

			elif current_index + 2 < len(file_string) and file_string[current_index:current_index+2] == '/*':

				multi_line_comment_val = parse_multi_line_comment(file_string, current_index)
				current_index += len(multi_line_comment_val)
				tokens.append((multi_line_comment_val, False))

			elif file_string[current_index] not in string.whitespace:

				delimiter_val = parse_delimiter(file_string, current_index)
				current_index += len(delimiter_val)
				tokens.append((delimiter_val, True))

			elif file_string[current_index] == '\n':

				indent_val = parse_indentation(file_string, current_index)
				current_index += len(indent_val)
				tokens.append((indent_val, False))

			else:
				current_index += 1


		else:
			current_token += file_string[current_index]
			current_index += 1

	return tokens

