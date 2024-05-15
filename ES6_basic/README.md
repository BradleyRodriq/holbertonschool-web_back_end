# ES6 Basics

ES6, or ECMAScript 2015, is the sixth major version of the ECMAScript language specification, which is the standard for JavaScript. It introduced several new features and syntax improvements to the language.

1. **New features introduced in ES6:**
   - Arrow functions
   - Classes
   - Template literals
   - Let and const for variable declaration
   - Enhanced object literals
   - Default parameters
   - Rest and spread operators
   - Destructuring assignment
   - Modules

2. **The difference between a constant and a variable:**
   - Constants (declared with `const`) cannot be reassigned a new value once they are initialized. Variables (declared with `let` or `var`) can be reassigned.

   ```javascript
   const PI = 3.14159;
   let count = 1;
   count = 2; // Valid
   PI = 3; // Invalid, will throw a TypeError
   ```

3. **Block-scoped variables:**
   - Variables declared with `let` and `const` are block-scoped, meaning they are only accessible within the block (e.g., within curly braces `{}`) where they are defined.

   ```javascript
   if (true) {
     let x = 10;
     console.log(x); // Output: 10
   }
   console.log(x); // ReferenceError: x is not defined
   ```

4. **Arrow functions and function parameters default to them:**
   - Arrow functions provide a more concise syntax compared to traditional function expressions and lexically bind the `this` value.

   ```javascript
   // Traditional function
   function add(a, b) {
     return a + b;
   }

   // Arrow function
   const add = (a, b) => a + b;
   ```

5. **Rest and spread function parameters:**
   - The rest parameter (`...`) allows you to represent an indefinite number of arguments as an array, while the spread operator (`...`) allows you to expand an array into individual elements.

   ```javascript
   function sum(...numbers) {
     return numbers.reduce((total, num) => total + num, 0);
   }

   const numbers = [1, 2, 3];
   console.log(sum(...numbers)); // Output: 6
   ```

6. **String templating in ES6:**
   - Template literals allow for easy interpolation of variables and expressions within strings, along with multiline strings.

   ```javascript
   const name = 'Alice';
   const greeting = `Hello, ${name}!`;
   console.log(greeting); // Output: Hello, Alice!
   ```

7. **Object creation and their properties in ES6:**
   - ES6 introduced shorthand property names, computed property names, and method definitions in object literals.

   ```javascript
   const name = 'Alice';
   const age = 30;

   const person = {
     name, // Shorthand property name
     ['age']: age, // Computed property name
     greet() { // Method definition
       return `Hello, my name is ${this.name} and I'm ${this.age} years old.`;
     }
   };
   console.log(person.greet()); // Output: Hello, my name is Alice and I'm 30 years old.
   ```

8. **Iterators and for-of loops:**
   - Iterators allow you to define custom iteration behavior for objects, while the `for...of` loop is used to iterate over iterable objects like arrays, strings, maps, sets, etc.

   ```javascript
   const iterable = [1, 2, 3];

   // Using iterator
   const iterator = iterable[Symbol.iterator]();
   console.log(iterator.next()); // Output: { value: 1, done: false }

   // Using for...of loop
   for (const value of iterable) {
     console.log(value); // Output: 1, 2, 3
   }
   ```

These examples demonstrate some of the key features introduced in ES6 and how they can be used in JavaScript code.
