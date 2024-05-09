export default class Car {
  constructor(brand, motor, color) {
    this._brand = brand;
    this._motor = motor;
    this._color = color;
  }

  static get [Symbol.species]() {
    return this;
  }

  cloneCar() {
    const ClonedCar = this.constructor[Symbol.species];
    return new ClonedCar(undefined, undefined, undefined);
  }
}
