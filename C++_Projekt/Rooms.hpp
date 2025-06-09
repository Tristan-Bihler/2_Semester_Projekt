#pragma once
#include "raylib.h"
#include "Enemy.hpp"
#include "Player.hpp"
#include "Hindernisse.hpp"
#include "string"
#include <vector>
#include <ctime>

using namespace std;

class Rooms {

private:
    
    int enemyAmount;
    int monitor = GetCurrentMonitor();  
    int ScreenPositionX;
    int ScreenPositionY;
    Rectangle door;

public:
    bool enemyAlive;
    Rooms(int screenWidth,int screenHeight);
    int getEnemyAmount()const {return enemyAmount;};
    void setDoor(bool enemyAlive);
    void changeRoom(Player& player, int currentlevel,bool enemyAlive, vector<Enemy>& enemies, vector<Hindernisse>& boxes, int* screenWidth, int* screenHeight, int screenWidth_o, int screenHeight_o);
    
};