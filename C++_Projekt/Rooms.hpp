#pragma once
#include "raylib.h"
#include "Enemy.hpp"
#include "Player.hpp"
#include "Hindernisse.hpp"
#include "string"
#include <vector>
#include <ctime>
#define VIS_Count 10

using namespace std;

class Rooms {

private:
    Rectangle door ={350, 201, 100, 30};
    //Texture2D visuals [VIS_Count] = {};
    string dateiname;
    int enemyAmount;
    int screenWidth;
    int screenHeight;
    int monitor;

public: 
    //Texture2D visuals [VIS_Count] = {};
    string pfad; 
    bool enemyAlive;
    int getEnemyAmount()const {return enemyAmount;};
    void preLoadTextures(const std::string& pfad,Texture2D* visuals);
    void kickTextures(Texture2D* visuals);
    void setDoor(bool enemyAlive);
    void changeRoom(Texture2D& background, Texture2D* visuals, Player& player, int currentlevel, bool enemyAlve, vector<Enemy>& enemies, vector<Hindernisse>& boxes, float screenWidth, float screenHeight);

};