# ES6 classes

1. **How to define a Class:**
   - In JavaScript, you can define a class using the `class` keyword followed by the class name. Inside the class, you can define properties and methods.

   ```javascript
   class Person {
     constructor(name, age) {
       this.name = name;
       this.age = age;
     }

     greet() {
       return `Hello, my name is ${this.name} and I'm ${this.age} years old.`;
     }
   }
   ```

2. **How to add methods to a class:**
   - Methods can be added to a class by defining functions within the class body.

   ```javascript
   class Person {
     constructor(name, age) {
       this.name = name;
       this.age = age;
     }

     greet() {
       return `Hello, my name is ${this.name} and I'm ${this.age} years old.`;
     }

     celebrateBirthday() {
       this.age++;
     }
   }
   ```

3. **Why and how to add a static method to a class:**
   - Static methods are attached to the class itself, rather than to instances of the class. They can be useful for utility functions or methods that don't require access to instance-specific data.

   ```javascript
   class MathUtils {
     static add(a, b) {
       return a + b;
     }
   }

   console.log(MathUtils.add(2, 3)); // Output: 5
   ```

4. **How to extend a class from another:**
   - You can extend a class by using the `extends` keyword, followed by the name of the class you want to extend.

   ```javascript
   class Student extends Person {
     constructor(name, age, grade) {
       super(name, age);
       this.grade = grade;
     }

     study() {
       return `${this.name} is studying hard for their exams.`;
     }
   }
   ```

5. **Metaprogramming and symbols:**
   - Metaprogramming in JavaScript involves writing code that can manipulate the structure of code at runtime. Symbols are a primitive data type introduced in ES6 that can be used as unique identifiers.

   ```javascript
   const mySymbol = Symbol('mySymbol');

   const obj = {
     [mySymbol]: 'Hello, Symbol!',
   };

   console.log(obj[mySymbol]); // Output: Hello, Symbol!
   ```

   Symbols are often used in metaprogramming to create unique keys for object properties, as they are guaranteed to be unique and not accessible through normal object property access.
