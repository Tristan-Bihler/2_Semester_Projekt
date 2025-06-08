#pragma once
#include "raylib.h"
#include "Enemy.hpp"
#include "Player.hpp"
#include "string"
#include <vector>
#include <ctime>
#define VIS_Count 10

using namespace std;

class Rooms {

private:
    Rectangle door;
    //Texture2D visuals [VIS_Count] = {};
    string dateiname;
    int enemyAmount;

public: 
    //Texture2D visuals [VIS_Count] = {};
    string pfad; 
    bool enemyAlive;
    int getEnemyAmount()const {return enemyAmount;};
    void preLoadTextures(const std::string& pfad,Texture2D* visuals);
    void kickTextures(Texture2D* visuals);
    void setDoor(bool enemyAlive);
    void changeRoom(Texture2D& background, Texture2D* visuals, Player& player, int currentlevel, bool enemyAlve, vector<Enemy>& enemies);
};