#ifndef MYCLASS_H
#define MYCLASS_H

#include <string> // If MyClass uses std::string

class MyClass {
public:
    // Constructor declaration
    MyClass();
    // Overloaded constructor declaration
    MyClass(std::string name);

    // Member function declarations
    void greet() const;
    void setName(std::string name);
    std::string getName() const;

private:
    std::string _name; // Member variable
};

#endif // MYCLASS_H