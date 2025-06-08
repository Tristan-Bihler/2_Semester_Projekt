#include "raylib.h"
#include "Rooms.hpp"
#include "Enemy.hpp"
#include "Player.hpp"
#include "Hindernisse.hpp"
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

// void Rooms:: setDoor(bool enemyAlive){
//     this-> door ={350, 201, 100, 30};
//     if (!enemyAlive){DrawRectangleRec(door, GOLD);}                //enemyAlive Variable muss noch erstellt werden
//     else {DrawRectangleRec(door, GRAY);}
// }

void Rooms:: setDoor(bool enemyAlive){
    //printf("door.x: %d, door.y: %d\n", door.x, door.y);
    //printf("ScreenWidth: %d, ScreenHeight: %d\n", screenWidth, screenHeight);
        
    if (!enemyAlive){DrawRectangleRec(door, GOLD);}                //enemyAlive Variable muss noch erstellt werden
    else {DrawRectangleRec(door, GRAY);}
}

void Rooms::changeRoom(Texture2D& background, Texture2D* visuals, Player& player, int currentlevel,bool enemyAlive, vector<Enemy>& enemies, vector<Hindernisse>& boxes, float screenWidth, float screenHeight) {
    int distribX = 0;
    int distribY = 0;
    if (CheckCollisionRecs(player.GetRect(), this-> door)&&!enemyAlive) {
        int raumIndex = currentlevel / 10;     //Alle 10 Level ändert sich der Hintergrund
        if (raumIndex < VIS_Count) {           //Check das Index < 10
            //UnloadTexture(background);
            //background = visuals[raumIndex];
        }
        player.SetPosition(400, player.GetRect().height + 35);
        player.Increase_Level();
        player.Increase_Mental_Health_Points();

        int monitor = GetCurrentMonitor();                                // Muss neu ausgelesen werden, da sonst screenWidth dauerhaft 0 ist
        int screenWidth = GetMonitorWidth(monitor);                 
        int screenHeight = GetMonitorHeight(monitor);
        door.x = screenWidth / 10 * 7;                                         // Tür soll immer Rechts erscheinen
        door.y = GetRandomValue (screenHeight / 10 * 1, screenHeight / 10 *9);   // Höhe der Tür soll varieren
        door.height = 100;
        door.width = 30;
        //door = {screenWidth * 0.7 , GetRandomValue (screenHeight / 10 * 1, screenHeight / 10 *9), 30, 100};
        printf("door.x: %d, door.y: %d\n", door.x, door.y);
        printf("ScreenWidth: %d, ScreenHeight: %d\n", screenWidth, screenHeight);


        for (int i = 0; i < int(boxes.size()); i++) // Notice no increment here
        {
            boxes.erase(boxes.begin()); // Removes the element and shifts everything after it
                                                // 'i' does not increment, as the next element slides into 'i'
        }

        int enemyAmount = 0;
        int hindernisseAmount = 2;

        if(currentlevel<20){enemyAmount=10;}
        if(currentlevel<15){enemyAmount=6;}
        if(currentlevel<10){enemyAmount=4;}
        if(currentlevel<5){enemyAmount=2;}
        
        for(int c= 0; c<hindernisseAmount; c++){
            distribX = rand() % (int(screenWidth / 10 * 6) - int(screenWidth / 10 * 4)) + int(screenWidth / 10 * 4);
            distribY = rand() % (int(screenWidth / 10 * 6) - int(screenWidth / 10 * 1)) + int(screenHeight / 10 * 1);
            boxes.emplace_back(distribX, distribY, 50, 50, BROWN);
        }

        for(int c=0; c<enemyAmount; c++){
            distribX = rand() % (int(screenWidth / 10 * 8) - int(screenWidth / 10 * 7)) + int(screenWidth / 10 * 7);
            distribY = rand() % (int(screenWidth / 10 * 6) - int(screenWidth / 10 * 1)) + int(screenHeight / 10 * 1);
            enemies.emplace_back(distribX, distribY, 50, 50, GREEN, 30, 100.0f);
        }
        }
        //TODO Respawn Hindernisse
}