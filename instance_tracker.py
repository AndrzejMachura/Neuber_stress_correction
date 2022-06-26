""" 
Decorator used to count number of calls of decorated function or created instances of the class

"""

class InstanceTracker:
    def __init__(self, object, counter=0):
        self._object = object
        self._counter=counter
        self._name = object.__name__     
       
    def __call__(self,*args,**kwargs):
        self._counter+=1
        return self._object(*args,**kwargs)

if __name__ == "__main__":

    @InstanceTracker
    def first_test():
        return "g"

    for x in range(10):
        print(first_test()+" "+str(x+1))
        print(f'number of calls of {first_test._name} function: {first_test._counter}\n')

    @InstanceTracker
    def second_test(n):
        return n**2

    for x in range(10):
        print(second_test(x)+x)
        print(f'number of calls of {second_test._name} function: {second_test._counter}\n')

    @InstanceTracker
    class ExampleClass:
        def __init__(self, value):
            self.atr = value
        def method(self):
            return self.atr+" e"
        
    x= ExampleClass("x")
    y= ExampleClass("y")

    print(x.method())
    print(y.method())


    for x in range(10):
        print(ExampleClass("s").method()+" "+str(x+1))
        print(f'number of calls of {ExampleClass._name}: {ExampleClass._counter}\n')