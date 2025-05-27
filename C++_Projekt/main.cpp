#include "Player.hpp" // Include the header for MyClass
#include <iostream>

int main() {
    MyClass obj1;           // Calls default constructor
    obj1.greet();           // Outputs: Hello from DefaultName!

    MyClass obj2("Gemini"); // Calls overloaded constructor
    obj2.greet();           // Outputs: Hello from Gemini!

    obj1.setName("ChatGPT");
    obj1.greet();           // Outputs: Hello from ChatGPT!

    std::cout << "Object 2's name: " << obj2.getName() << std::endl;

    return 0;
}