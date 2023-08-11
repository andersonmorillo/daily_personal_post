#python guide

#create a Class 

class clase:
    x = 5 # con una propuedad llamada x con un valor de 5

#con las clases que son un blueprint se pueden crear objetos 
p1 = clase()
print(p1.x)

#para crear una clase que se a util se utiliza la funcion __init__ para asignar los valores a las propiedades de los objetos
class person:
    def __init__(self, age, name):
        self.age = age 
        self.name = name

    def funcion(self):#self hace referencia a una misma instancia de la clase
        print ("my name is " + self.name)


    def __str__(self): #establecer el return al llamar el objeto como un string 
        return f"{self.name} is {self.age} years old"

p1 = person(10, "pedro")




print(p1)
print(p1.name)
print(p1.age)
print(p1.funcion())

#modify objects properities
p1.name = "pepe"
print(p1.name)

#delete objects properities
del p1.name 

#delete objects
del p1


#create a child class from person
class student(person):
    pass


s1 =student(12,"carla")
print(s1)


#add methods to class student
class Student(person):
    def __init__(self, age, name, lname):#the method init add new methods to the class strudent, but stop the inherits from the funtion init from the parent
        super().__init__(age, name)#super add the properties and methods from the parent
        self.lastname = lname

    def student_info(self):
        print(f"{self.name} {self.lastname} is {self.age} years old")


s2 = Student(21,"angie", "patricia")

s2.student_info()

print(s2)

#polymorfismo we use the class vehicle to make it work with several clases
class Vehicle:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

  def move(self):
    print("Move!")

class Car(Vehicle):
  pass

class Boat(Vehicle):
  def move(self):
    print("Sail!")

class Plane(Vehicle):
  def move(self):
    print("Fly!")

car1 = Car("Ford", "Mustang") #Create a Car object
boat1 = Boat("Ibiza", "Touring 20") #Create a Boat object
plane1 = Plane("Boeing", "747") #Create a Plane object

for x in (car1, boat1, plane1):
  print(x.brand)
  print(x.model)
  x.move()