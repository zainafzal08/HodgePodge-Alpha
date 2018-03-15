class Trigger():
	def __init__(self,regex,access):
		self.regex = regex
		self.access = access
		self.initalised = False
	def __call__(self,f,**args):
		def wrapped_f(*args):
			if not self.initalised:
				args[0].getParser().register(args[0],self.regex,self.access)
				self.initalised = True
			f(*args)
		return wrapped_f
