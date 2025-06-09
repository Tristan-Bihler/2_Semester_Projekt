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

Rooms::Rooms(){
    monitor = GetCurrentMonitor();                                              // Aktuellen Monitor festlegen     
    
    InitWindow(screenWidth, screenHeight, "DHBW SURVIVAL! Exams of Doom");          //Intialisierung notwendig, um Monitorgröße auslesen zu können
    screenWidth_o = GetMonitorWidth(monitor) * 0.66f;                                 //Monitorbreite auslesen mulitpliziert mit 2/3
    screenHeight_o = GetMonitorHeight(monitor) * 0.66f;                               //Monitorhöhe auslesen mulitpliziert mit 2/3
    screenWidth = screenWidth_o;
    screenHeight = screenHeight_o;
    ScreenPositionX = (GetMonitorWidth(monitor) - screenWidth) / 2;
    ScreenPositionY = (GetMonitorHeight(monitor) - screenHeight) / 2;
    SetWindowSize(screenWidth, screenHeight);                                       // Größe des Fensters setzen 2/3 des Monitors
    SetWindowPosition(ScreenPositionX, ScreenPositionY);                            // Fenster Mittig positionieren
    door = {screenWidth * 0.9f, screenHeight * 0.5f, 30, 100};
}

void Rooms:: setDoor(bool enemyAlive){
    if (!enemyAlive){DrawRectangleRec(door, GOLD);}                //enemyAlive Variable muss noch erstellt werden
    else {DrawRectangleRec(door, GRAY);}
}

void Rooms::changeRoom(Player& player, int currentlevel,bool enemyAlive, vector<Enemy>& enemies, vector<Hindernisse>& boxes) {
    int distribX = 0;
    int distribY = 0;
    if (CheckCollisionRecs(player.GetRect(), this-> door)&&!enemyAlive) {
        player.SetPosition(100, player.GetRect().height + 35);
        player.Increase_Level();
        player.Increase_Mental_Health_Points();

        screenWidth = screenWidth_o + screenWidth_o * GetRandomValue(-3, 3) / 10;
        screenHeight = screenHeight_o + screenHeight_o * GetRandomValue(-3, 3) / 10;
        int monitor = GetCurrentMonitor();   
        ScreenPositionX = (GetMonitorWidth(monitor) - screenWidth) / 2;
        ScreenPositionY = (GetMonitorHeight(monitor) - screenHeight) / 2;

        SetWindowSize(screenWidth, screenHeight);
        SetWindowPosition(ScreenPositionX, ScreenPositionY);  

        door.x = screenWidth / 10 * 9;                                            // Tür soll immer Rechts erscheinen
        door.y = GetRandomValue (screenHeight / 10 * 1, screenHeight / 10 * 9);   // Höhe der Tür soll varieren
        door.height = 100;
        door.width = 30;
        //door = {screenWidth * 0.7 , GetRandomValue (screenHeight / 10 * 1, screenHeight / 10 *9), 30, 100};

        for (int i = 0; i < int(boxes.size()); i++) // Notice no increment here
        {
            boxes.erase(boxes.begin()); // Removes the element and shifts everything after it
                                        // 'i' does not increment, as the next element slides into 'i'
        }

        vector<Bullet>& playerBullets = player.GetBulletsMutable();
        for (size_t i = 0; i < playerBullets.size(); ) {
            playerBullets.erase(playerBullets.begin() + i);
        }

        int enemyAmount = 0;
        int hindernisseAmount = 4;

        if(currentlevel<100){enemyAmount=10;}
        if(currentlevel<15){enemyAmount=6;}
        if(currentlevel<10){enemyAmount=4;}
        if(currentlevel<5){enemyAmount=2;}
        
        for(int c= 1; c<hindernisseAmount; c++){
            distribX = GetRandomValue(screenWidth * 0.4f, screenWidth * 0.6f);
            distribY = GetRandomValue(screenHeight * 0.1f, screenHeight * 0.9f);
            boxes.emplace_back(distribX, distribY, 50, 50, BROWN);
        }

        for(int c=0; c<enemyAmount; c++){
            distribX = GetRandomValue(screenWidth  * 0.7f, screenWidth  * 0.8f);
            distribY = GetRandomValue(screenHeight * 0.1f, screenHeight * 0.9f);
            enemies.emplace_back(distribX, distribY, 50, 50, GREEN, 30 + 2 * (player.GetLevel() - 1), 100.0f);
        }
    }
}