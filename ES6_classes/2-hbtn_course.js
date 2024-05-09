export default class HolbertonCourse {
  constructor(name, length, students) {
    if (typeof name !== 'string')
      throw TypeError('name must be a string');
    if (typeof length !== 'number')
      throw TypeError('length must be a number');
    if (!Array.isArray(students))
        throw TypeError('students must be an array');;
    this._name = name;
    this._length = length;
    this._students = students;
  }

  get name() {
    return this._name;
  }

  get length() {
    return this._length;
  }

  get students() {
    return this._students;
  }

  set name(new_name) {
    if (typeof new_name !== 'string')
      throw TypeError('name must be a string');
    this._name = new_name;
  }

  set length(new_length) {
    if (typeof new_length !== 'number')
      throw TypeError('length must be a number');
    this._length = new_length;
  }

  set students(new_students) {
    if (!Array.isArray(new_students))
      throw TypeError('students must be an array');
    this._students = new_students;
  }

}
