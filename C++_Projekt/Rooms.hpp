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
    int screenWidth = 0;     
    int screenHeight = 0;
    int screenWidth_o;
    int screenHeight_o;
    int ScreenPositionX;
    int ScreenPositionY;
    int enemyAmount;
    int monitor;  
    Rectangle door;

public:
    bool enemyAlive;
    Rooms();
    int getEnemyAmount()const {return enemyAmount;};
    int getscreenWidth()const {return screenWidth;};
    int getscreenHeight()const {return screenHeight;};
    void setDoor(bool enemyAlive);
    void changeRoom(Player& player, int currentlevel,bool enemyAlive, vector<Enemy>& enemies, vector<Hindernisse>& boxes);

};