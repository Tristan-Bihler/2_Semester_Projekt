#include "raylib.h"
#include "Player.hpp"
#include "Enemy.hpp"
#include "Bullet.hpp"
#include <vector>
#include <random>
#include <algorithm> // For std::remove_if

<<<<<<< Updated upstream
using namespace std;

int main() {
=======
#define G 400  //Gravitaiton
#define PLAYER_JUMP_SPD 350.0f   // Sprunghöhe
#define PLAYER_HOR_SPD 200.0f    //Geschwindigkeit 

typedef struct Player {
    Vector2 position;
    float speed;
    bool canJump;
} Player;

typedef struct EnvItem {
    Rectangle rect;
    int blocking;
    Color color;
} EnvItem;

//----------------------------------------------------------------------------------
// Module functions declaration
//----------------------------------------------------------------------------------
void UpdatePlayer(Player *player, EnvItem *envItems, int envItemsLength, float delta);
void UpdateCameraCenter(Camera2D *camera, Player *player, EnvItem *envItems, int envItemsLength, float delta, int width, int height);

void UpdateCameraCenterInsideMap(Camera2D *camera, Player *player, EnvItem *envItems, int envItemsLength, float delta, int width, int height);

//------------------------------------------------------------------------------------
// Program main entry point
//------------------------------------------------------------------------------------
int main(void)
{
    // Initialization
    //--------------------------------------------------------------------------------------
>>>>>>> Stashed changes
    const int screenWidth = 800;
    const int screenHeight = 450;

    InitWindow(screenWidth, screenHeight, "DHBW SURVIVAL Exams of Doom");

<<<<<<< Updated upstream
    Player player(screenWidth / 2 - 25, screenHeight - 75, 50, 50, RED, 100, 10);
=======
    Player player = { 0 };
    player.position = (Vector2){ 200, 280 };
    player.speed = 0;
    player.canJump = false;
    EnvItem envItems[] = {
        {{ 0, 0, 1000, 400 }, 0, LIGHTGRAY },
        {{ 0, 400, 400, 10 }, 1, GRAY }, // Boden // { x, y, width, height }  //1 - kollidierbares Objekt
        {{ 400, 0, 10, 400 }, 1, GRAY }, //rechter balken
        {{ 0, 0, 10, 400 }, 1, GRAY },  //linker Blaken
        {{ 650, 300, 100, 10 }, 1, GRAY }
    };
>>>>>>> Stashed changes

    vector<Enemy> enemies;
    float enemySpawnTimer = 0.0f;
    float enemySpawnRate = 2.0f;

<<<<<<< Updated upstream
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> distribX(0, screenWidth - 50);
=======
    Camera2D camera = { 0 };
    camera.target = player.position;
    camera.offset = (Vector2){ screenWidth/2.0f, screenHeight/2.0f };
    camera.rotation = 0.0f;
    camera.zoom = 1.0f;

    // Store pointers to the multiple update camera functions
    void (*cameraUpdaters[])(Camera2D*, Player*, EnvItem*, int, float, int, int) = {
        UpdateCameraCenter,
    };

    int cameraOption = 0;
    int cameraUpdatersLength = sizeof(cameraUpdaters)/sizeof(cameraUpdaters[0]);

   /* char *cameraDescriptions[] = {
        "Follow player center",
        "Follow player center, but clamp to map edges",
        "Follow player center; smoothed",
        "Follow player center horizontally; update player center vertically after landing",
        "Player push camera on getting too close to screen edge"
    };*/
>>>>>>> Stashed changes

    // Set target FPS for smooth animation
    SetTargetFPS(60);

    // Game loop
    while (!WindowShouldClose()) {
        // Get frame time for consistent movement across different frame rates
        float deltaTime = GetFrameTime();

        // Update
        //----------------------------------------------------------------------------------
        player.Update(deltaTime);

        // Update enemies
        for (auto& enemy : enemies) {
            enemy.Update(deltaTime, {player.GetRect().x, player.GetRect().y});
        }

        // Spawn enemies
        enemySpawnTimer += deltaTime;
        if (enemySpawnTimer >= enemySpawnRate) {
            enemies.emplace_back(distribX(gen), -50.0f, 50, 50, GREEN, 30, 100.0f); // Random X, above screen, 30 health, 100 speed
            enemySpawnTimer = 0.0f;
        }

        // Bullet-Enemy Collision
        // Iterate through bullets and enemies for collision detection
        vector<Bullet>& playerBullets = player.GetBulletsMutable();
        for (size_t i = 0; i < playerBullets.size(); ) {
            bool bulletHit = false;
            for (size_t j = 0; j < enemies.size(); ) {
                if (CheckCollisionRecs(playerBullets[i].GetRect(), enemies[j].GetRect())) {
                    enemies[j].TakeDamage(20); // Bullet deals 20 damage
                    player.Increase_Level();
                    bulletHit = true; // Mark bullet for removal
                    // If enemy is dead, remove it
                    if (!enemies[j].IsActive()) {
                        enemies.erase(enemies.begin() + j);
                    } else {
                        ++j; // Move to next enemy
                    }
                } else {
                    ++j; // Move to next enemy
                }
            }
            if (bulletHit) {
                playerBullets.erase(playerBullets.begin() + i);
            } else {
                ++i; // Move to next bullet
            }
        }


        // Player-Enemy Collision (Player takes damage)
        for (auto& enemy : enemies) {
            if (enemy.IsActive() && CheckCollisionRecs(player.GetRect(), enemy.GetRect())) {
                player.TakeDamage(1 * player.GetLevel()); // Player takes 1 damage per frame if colliding
                // Optional: Push enemy away or make it stop for a moment
            }
        }

        // Remove dead enemies (using erase-remove idiom)
        enemies.erase(std::remove_if(enemies.begin(), enemies.end(),
                                     [](const Enemy& e){ return !e.IsActive(); }),
                      enemies.end());

        // Game over check
        if (player.GetHealth() <= 0) {
            // Handle game over (e.g., display message, restart game)
            // For now, we'll just close the window
            TraceLog(LOG_INFO, "GAME OVER! Player defeated.");
            break; // Exit game loop
        }

        BeginDrawing();

            ClearBackground(RAYWHITE);

            player.Draw(); 

            for (const auto& enemy : enemies) {
                enemy.Draw();
            }

<<<<<<< Updated upstream
            DrawText(TextFormat("Health: %i", player.GetHealth()), 10, 10, 20, BLACK);
            DrawText(TextFormat("Level: %i", player.GetLevel()), 500, 10, 20, BLACK);
=======
                Rectangle playerRect = { player.position.x - 20, player.position.y - 40, 40.0f, 40.0f };
                DrawRectangleRec(playerRect, RED);
                
                DrawCircleV(player.position, 5.0f, GOLD);

            EndMode2D();

            DrawText("Controls:", 20, 20, 10, BLACK);
            DrawText("- Right/Left to move", 40, 40, 10, DARKGRAY);
            DrawText("- Space to jump", 40, 60, 10, DARKGRAY);
            DrawText("- Mouse Wheel to Zoom in-out, R to reset zoom", 40, 80, 10, DARKGRAY);
            DrawText("- C to change camera mode", 40, 100, 10, DARKGRAY);
            DrawText("Current camera mode:", 20, 120, 10, BLACK);
           // DrawText(cameraDescriptions[cameraOption], 40, 140, 10, DARKGRAY);
>>>>>>> Stashed changes

        EndDrawing();
    }

    CloseWindow();

    return 0;
<<<<<<< Updated upstream
}
=======
}

void UpdatePlayer(Player *player, EnvItem *envItems, int envItemsLength, float delta)
{
    if (IsKeyDown(KEY_LEFT)) player->position.x -= PLAYER_HOR_SPD*delta;
    if (IsKeyDown(KEY_RIGHT)) player->position.x += PLAYER_HOR_SPD*delta;
    if (IsKeyDown(KEY_SPACE) && player->canJump)
    {
        player->speed = -PLAYER_JUMP_SPD;
        player->canJump = false;
    }

   bool hitObstacle = false;
    for (int i = 0; i < envItemsLength; i++)
    {
        EnvItem *ei = envItems + i;
        Vector2 *p = &(player->position);
           // Überprüfen, ob das Objekt ein Hindernis ist und die Spielfigur mit ihm kollidiert
     
    // Überprüfen, ob das Objekt ein Hindernis ist und die Spielfigur mit ihm kollidiert
    if (ei->blocking &&
        ei->rect.x <= p->x &&
        ei->rect.x + ei->rect.width >= p->x &&
        ei->rect.y >= p->y &&
        ei->rect.y <= p->y + player->speed * delta)
    {
        hitObstacle = true;
        player->speed = 0.0f;
        p->y = ei->rect.y;
        break; // Sobald eine Kollision erkannt wird, wird die Schleife beendet
    }
}
if (!hitObstacle)
{
    player->position.y += player->speed * delta;
    player->speed += G * delta;
    player->canJump = false;
}
else player->canJump = true;
}

void UpdateCameraCenter(Camera2D *camera, Player *player, EnvItem *envItems, int envItemsLength, float delta, int width, int height)
{
    camera->offset = (Vector2){ width/2.0f, height/2.0f };
    camera->target = player->position;
}
>>>>>>> Stashed changes
