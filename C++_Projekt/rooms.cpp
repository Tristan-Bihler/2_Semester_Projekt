#include "raylib.h"



void WechselRaum(Texture2D* background, const char* neuerRaumPfad);

    Texture2D backround = LoadTexture("XXXXXXXXassets/bild.png");
    Texture2D playerTexture = LoadTexture("XXXXXXXplayer.png");
    Texture2D backround = LoadTexture("C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/assets/raum1.png");
    Texture2D playerTexture = LoadTexture("C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/assets/player.png");
    Rectangle door = { 750, 450, 50, 100 }; // z. B. rechte Seite des Raums
    Vector2 position = { 201.0f, 201.0f };


        /*if (CheckCollisionRecs(player, door)) {
        WechselRaum(&backround, "C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/assets/raum2.png");
        player.x = 10; // Spieler neu positionieren
        player.y = 450;*/

        bool collision = CheckCollisionRecs(player, enemy);



        //DrawText("Bewege das blaue Rechteck mit den Pfeiltasten", 10, 10, 20, DARKGRAY);
        DrawTexture(backround, 0, 201, WHITE);
        DrawTextureEx(playerTexture, (Vector2){player.x,player.y}, 0.0f, 1.0f, WHITE);
        DrawTextureEx(playerTexture, (Vector2){player.x,player.y}, 0.0f, 0.1f, WHITE);
        DrawRectangleRec(enemy, RED);
        DrawRectangleRec(door, BROWN);

        
        if (CheckCollisionRecs(player, door)) {
        WechselRaum(&backround, "C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/assets/raum2.png");
        player.x = 10; // Spieler neu positionieren
        player.y = 450;
}


        EndDrawing();
    }

while (!WindowShouldClose()) {
    UnloadTexture(backround);
    return 0;
}

void WechselRaum(Texture2D* background, const char* neuerRaumPfad) {
    UnloadTexture(*background);
    *background = LoadTexture(neuerRaumPfad);
}