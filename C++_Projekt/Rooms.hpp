#pragma once
#include "raylib.h"
#include "string"
#define VIS_Count 10

using namespace std;

class Rooms {

private:
    Rectangle door;
    Texture2D visuals [VIS_Count] = {};
    string dateiname;

public: 
    string pfad; 
    bool enemyAlive;
    void preLoadTextures(const std::string& pfad,Texture2D* visuals);
    void kickTextures(Texture2D* visuals);
    void setDoor(bool enemyAlive);
    void WechselRaum(Texture2D& background, Texture2D* visuals, Rectangle& player,
         Rectangle door, int currentlevel);
};