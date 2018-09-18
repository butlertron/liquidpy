
class LiquidLine(object):
	"""
	Line of compiled code
	"""
	
	def __init__(self, line, src = '', lineno = 0, indent = 0):
		"""
		Constructor of line
		@params:
			`line`  : The compiled line
			`src`   : The source of the line
			`indent`: Number of indent of the line 
		"""
		self.line   = line
		self.src    = src or line
		self.lineno = lineno
		self.ndent  = indent

	def __repr__(self):
		"""
		For exceptions
		"""
		return "Line {}: {}".format(self.lineno, self.src)
	
	def __str__(self):
		return "{}{}\n".format("\t" * self.ndent, self.line)

class LiquidCode(object):
	"""
	Build source code conveniently.
	"""

	INDENT_STEP = 1

	def __init__(self, indent = 0):
		"""
		Constructor of code builder
		@params:
			`envs`  : The envs to compile the template
			`indent`: The initial indent level
		"""
		self.codes = []
		self.ndent = indent

	def __str__(self):
		"""
		Concatnate of the codes
		@returns:
			The concatnated string
		"""
		return "".join(str(c) for c in self.codes)

	def addLine(self, line):
		"""
		Add a line of source to the code.
		Indentation and newline will be added for you, don't provide them.
		@params:
			`line`: The line to add
		"""
		if not isinstance(line, LiquidLine):
			line = LiquidLine(line)
		line.ndent = self.ndent
		self.codes.append(line)
	'''
	def addSection(self):
		"""
		Add a section, a sub-CodeBuilder.
		@returns:
			The section added.
		"""
		section = LiquidCode(self.ndent)
		self.codes.append(section)
		return section
	'''
	
	def indent(self):
		"""
		Increase the current indent for following lines.
		"""
		self.ndent += self.INDENT_STEP

	def dedent(self):
		"""
		Decrease the current indent for following lines.
		"""
		self.ndent -= self.INDENT_STEP

	def _nlines(self):
		"""
		Get the number of lines in the builder
		@returns:
			The number of lines.
		"""
		return sum(1 if isinstance(c, LiquidLine) else c._nlines() for c in self.codes)

	def lineByNo(self, lineno):
		"""
		Get the line by line number
		@params:
			`lineno`: The line number
		@returns:
			The LiquidLine object at `lineno`.
		"""
		if lineno <= 0: return None

		n = 0
		for c in self.codes:
			if isinstance(c, LiquidLine):
				n += 1
				if n == lineno: 
					return c
			else:
				nlines = c._nlines()
				n += nlines
				if n >= lineno:
					return c.lineByNo(lineno - n + nlines)


