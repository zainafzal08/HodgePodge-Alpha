class Trigger():
	def __init__(self,regex,access,validation):
		self.regex = regex
		self.access = access
		self.initalised = False
		self.validation = validation
	def __call__(self,f,**args):
		def wrapped_f(*args):
			if not self.initalised:
				args[0].getParser().register(args[0],self.regex,self.access,f.__name__,self.validation)
				self.initalised = True
			else:
				return f(*args)
		return wrapped_f
