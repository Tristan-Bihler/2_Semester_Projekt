#include "raylib.h"
#include "Rooms.hpp"
#include "Enemy.hpp"
#include "string"
#include <vector>
#include <ctime>
#define VIS_Count 10

using namespace std;

void Rooms::preLoadTextures(const string& pfad,Texture2D* visuals){
    for(int i = 0; i<VIS_Count; i++){
        string dateiname = pfad + "/raum" + to_string(i) + ".png";
        visuals[i] = LoadTexture(dateiname.c_str());
    }
}

void Rooms::kickTextures(Texture2D* visuals){
    for(int x = 0; x<VIS_Count; x++){
        UnloadTexture(visuals[x]);
    }
}

void Rooms:: setDoor(bool enemyAlive){
    Rectangle door ={350, 201, 100, 30};
    if (!enemyAlive){DrawRectangleRec(door, GOLD);}                //enemyAlive Variable muss noch erstellt werden
    else {DrawRectangleRec(door, GRAY);}
}


void Rooms::WechselRaum(Texture2D& background, Texture2D* visuals, Rectangle& player, Rectangle door, int currentlevel) {
    int distribX = 0;
    int distribY = 0;
    if (CheckCollisionRecs(player, door)) {
        int raumIndex = currentlevel / 10;     //Alle 10 Level ändert sich der Hintergrund
        if (raumIndex < VIS_Count) {           //Check das Index < 10
            UnloadTexture(background);
            background = visuals[raumIndex];
        }
        player.x = 400;                         //Respawn player
        player.y = player.height + 35;
        
        int enemyAmount = 0;
        if(currentlevel<5){enemyAmount=2;}
        if(currentlevel<10){enemyAmount=4;}
        if(currentlevel<15){enemyAmount=6;}
        if(currentlevel<20){enemyAmount=10;}

        for(int c=0; c<enemyAmount; c++){
            distribX = rand() % 1000 + 800;
            distribY = rand() % 750 + 50;
            enemies.emplace_back(distribX, distribY, 50, 50, GREEN, 30, 100.0f); // Random X, above screen, 30 health, 100 speed
        }
        }
        //TODO Respawn Hindernisse
}