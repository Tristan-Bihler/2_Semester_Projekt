#include "raylib.h"
#include "Rooms.hpp"
#include "Enemy.hpp"
#include "Player.hpp"
#include "string"
#include <vector>
#include <ctime>
#define VIS_Count 10

using namespace std;

void Rooms::preLoadTextures(const string& pfad,Texture2D* visuals){
    for(int i = 0; i<VIS_Count; i++){
        string dateiname = pfad + "/raum" + to_string(i) + ".png";
        //visuals[i] = LoadTexture(dateiname.c_str());
    }
}

void Rooms::kickTextures(Texture2D* visuals){
    for(int x = 0; x<VIS_Count; x++){
        //UnloadTexture(visuals[x]);
    }
}

void Rooms:: setDoor(bool enemyAlive){
    this-> door ={350, 201, 100, 30};
    if (!enemyAlive){DrawRectangleRec(door, GOLD);}                //enemyAlive Variable muss noch erstellt werden
    else {DrawRectangleRec(door, GRAY);}
}


void Rooms::changeRoom(Texture2D& background, Texture2D* visuals, Player& player, int currentlevel, vector<Enemy>& enemies) {
    int distribX = 0;
    int distribY = 0;
    if (CheckCollisionRecs(player.GetRect(), this-> door)) {
        int raumIndex = currentlevel / 10;     //Alle 10 Level ändert sich der Hintergrund
        if (raumIndex < VIS_Count) {           //Check das Index < 10
            //UnloadTexture(background);
            //background = visuals[raumIndex];
        }
        player.SetPosition(400, player.GetRect().height + 35);
        player.Increase_Level();
        
        int enemyAmount = 0;
        if(currentlevel<20){enemyAmount=10;}
        if(currentlevel<15){enemyAmount=6;}
        if(currentlevel<10){enemyAmount=4;}
        if(currentlevel<5){enemyAmount=2;}
        

        for(int c=0; c<enemyAmount; c++){
            distribX = rand() % 1000 + 800;
            distribY = rand() % 750 + 50;
            printf("Enemy spawned");
            enemies.emplace_back(distribX, distribY, 50, 50, GREEN, 30, 100.0f);
        }
        }
        //TODO Respawn Hindernisse
}