class MyClass:

    def __new__(cls, *args, **kwargs) -> 'MyClass':
        print(f'Args -> {args}')
        print(f'Kwargs -> {kwargs}')

        my_class_instance: 'MyClass' = super().__new__(cls)
        print(f'Object Creation Done -> {my_class_instance}')
        print(f'Dir -> {dir(my_class_instance)}')

        return my_class_instance
    
    # args or kwargs are unpacked into these params
    # if these params are explicitely defined in the function signature like below
    # if function signature is like def __init__(self, *args, **kwargs)
    # then no brainer args and kwargs from new -> args and kwargs of init

    # Python automatically calls the __init__() once __new__() is executed
    # Python populates self with my_class_instance during call
    # may be like my_class_instance.__init__(params)

    def __init__(self, param1: int, param2: int) -> None:

        # Basically adding param1 and param2 to object namespace formally
        print(f'Initializing Params...')
        self.param1 = param1
        self.param2 = param2
        print(f'Dir -> {dir(self)}')

# Args will be populated and kwargs will be empty
# Parameters in init will be unpacked in order: 
# 10 will be filled in param1 and 20 will be filled in param2
my_class_instace1: MyClass = MyClass(10, 20)

# Args will be empty and kwargs will have the key-value pair
# Since kwargs are already key-value and we specifically define for
# which paramter what should be the value, ofcourse order of paramerts
# is not taken into consideration while unpacking
my_class_instace2: MyClass = MyClass(param2=100, param1=200)
