#include <raylib.h>
#include <time.h>
#define ROOM_CNT 5

void WechselRaum(Texture2D* background, const char* neuerRaumPfad);

int main(){

    //Fenstergröße & StartRaum festlegen 
    const int screenWidth = 800;
    const int screenHeight = 1000;
    InitWindow(screenWidth, screenHeight, "DHBW SURVIVAL - Exams of Doom!");
    Texture2D startRaum = LoadTexture("C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/assets/raum1.png");
    Texture2D backround = startRaum;

    //Player einfügen
    Rectangle player = {400, 600, 50, 50};
    Texture2D playerTexture = LoadTexture("C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/assets/player.png");
    Vector2 position = {400, 600};
    const float speed = 4.0f;

    //Räume definieren
    typedef struct Room{
        int num;
        const char* pfad;
        Texture2D textur;
        int nachbarn[4]; //0=oben, 1=rechts, 2=unten, 3=links, -1 keine Tür in diese Richtung
    } Room;

    Room raeume [ROOM_CNT];
    int currentRoom = 0;



    //Türen definieren
    int doorcnt= GetRandomValue(1,5); 
    Rectangle doorLeft = {0,551, 30, 100};
    Rectangle doorTop = {350, 201, 100, 30};
    Rectangle doorRight = {770,551, 30, 100};
    Rectangle doorBottom = {350, 970, 100, 30};

    SetTargetFPS(60);

while(!WindowShouldClose()){
//Anpassungen
        // Bewegung des Spielers mit WASD
        if (IsKeyDown(KEY_D)&& (player.x<screenWidth-player.width)) player.x += speed;
        if (IsKeyDown(KEY_A)&& (player.x>0)) player.x -= speed;
        if (IsKeyDown(KEY_S)&& (player.y<screenHeight-player.height)) player.y += speed;
        if (IsKeyDown(KEY_W)&& (player.y>200)) player.y -= speed;

//Zeichnen

    //Fesnter Zeichnen
    BeginDrawing();
    ClearBackground(RAYWHITE);

    //Raum zeichnen
    DrawTexture(backround, 0, 201, WHITE);
    DrawRectangleRec(doorLeft, BROWN);
    DrawRectangleRec(doorTop, BROWN);
    DrawRectangleRec(doorRight, BROWN);
    DrawRectangleRec(doorBottom, BROWN);



    //Player zeichnen
    DrawTextureEx(playerTexture, (Vector2){player.x,player.y}, 0.0f, 0.1f, WHITE);



    EndDrawing();
}
CloseWindow();
UnloadTexture(playerTexture);
UnloadTexture(startRaum);
return 0;
}

void WechselRaum(Texture2D* background, const char* neuerRaumPfad) {
    UnloadTexture(*background);
    *background = LoadTexture(neuerRaumPfad);
}