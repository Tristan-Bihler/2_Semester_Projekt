#include "Player.hpp" // Include the header file for MyClass
#include <iostream>  // For std::cout

// Constructor definition
MyClass::MyClass() : _name("DefaultName") {
    // Constructor body
}

// Overloaded constructor definition
MyClass::MyClass(std::string name) : _name(name) {
    // Constructor body
}

// Member function definitions
void MyClass::greet() const {
    std::cout << "Hello from " << _name << "!" << std::endl;
}

void MyClass::setName(std::string name) {
    _name = name;
}

std::string MyClass::getName() const {
    return _name;
}