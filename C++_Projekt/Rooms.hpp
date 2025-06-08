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
    
    //Texture2D visuals [VIS_Count] = {};
    string dateiname;
    int enemyAmount;
    int monitor = GetCurrentMonitor();  
    float screenWidth = GetMonitorWidth(monitor) * 0.66f;                                 //Monitorbreite auslesen mulitpliziert mit 2/3
    float screenHeight = GetMonitorHeight(monitor) * 0.66f;   
    int ScreenPositionX;
    int ScreenPositionY;
    Rectangle door ={screenWidth * 0.9f, screenHeight * 0.5f, 30, 100};

public: 
    //Texture2D visuals [VIS_Count] = {};
    string pfad; 
    bool enemyAlive;
    int getEnemyAmount()const {return enemyAmount;};
    void setDoor(bool enemyAlive);
    void changeRoom(Player& player, int currentlevel,bool enemyAlive, vector<Enemy>& enemies, vector<Hindernisse>& boxes, int* screenWidth, int* screenHeight, int screenWidth_o, int screenHeight_o);

};