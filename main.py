from models.pet import Dog, Cat, Bird

dog = Dog("D01", "Lucky", "Poodle", 5, 3000000)
cat = Cat("C01", "Mimi", "British Shorthair", 3, 2500000)
bird = Bird("B01", "Rio", "Parrot", 1, 800000)

print(dog.get_info())
print(cat.get_info())
print(bird.get_info())