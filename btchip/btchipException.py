class BTChipException(Exception):

	def __init__(self, message):
		self.message = message

	def __str__(self):
		buf = "Exception : " + self.message
		return buf

	def message(self):
		return self.message
