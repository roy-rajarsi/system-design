class MyClass:
	
	def __init__(self):
		self.a = 10
		self.b = 20


my_class_obj = MyClass()
print(f'Original Initial Namespace -> {dir(my_class_obj)}')

# Adding an attribute c to namespace
my_class_obj.c = 30
print(f'\n\nc added to NameSpace of my_class_obj -> {dir(my_class_obj)}')
print(f'my_class_object.c -> {my_class_obj.c}')

my_class_obj2 = MyClass()
print(f'\n\nNo other object\'s namespace is hampered -> {dir(my_class_obj2)}')
