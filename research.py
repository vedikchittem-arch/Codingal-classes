
import cv2
import mediapipe as mp
import numpy as np
import random
import time
import math
import os

# ============================================================
# SETTINGS
# ============================================================

WIDTH = 900
HEIGHT = 650

MODEL_FILE = "hand_landmarker.task"

# ============================================================
# CHECK MODEL
# ============================================================

if not os.path.exists(MODEL_FILE):
    print("ERROR: hand_landmarker.task is missing!")
    print("Put it in the same folder as this program.")
    exit()

# ============================================================
# MEDIAPIPE 1.0.1
# ============================================================

BaseOptions = mp.tasks.BaseOptions
RunningMode = mp.tasks.vision.RunningMode
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_FILE
    ),
    running_mode=RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.4,
    min_hand_presence_confidence=0.4,
    min_tracking_confidence=0.4
)

landmarker = HandLandmarker.create_from_options(options)

# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera is not opened")
    exit()

# ============================================================
# PLAYER
# ============================================================

player_x = 180
player_y = 470

player_health = 100

player_width = 70
player_height = 120

player_attack = False
player_block = False
player_special = False

# ============================================================
# ENEMY
# ============================================================

enemy_x = 700
enemy_y = 470

enemy_health = 100

enemy_width = 70
enemy_height = 120

enemy_attack = False
enemy_block = False

# ============================================================
# GAME VARIABLES
# ============================================================

game_over = False

winner = ""

last_enemy_attack = time.time()

attack_cooldown = 0

special_cooldown = 0

hit_effect = 0

hit_x = 0
hit_y = 0

# ============================================================
# FUNCTIONS
# ============================================================

def distance(p1, p2):

    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )


def count_fingers(hand):

    fingers = []

    # Thumb
    if hand[4].x < hand[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tips = [8, 12, 16, 20]
    joints = [6, 10, 14, 18]

    for tip, joint in zip(tips, joints):

        if hand[tip].y < hand[joint].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def get_gesture(hand):

    fingers = count_fingers(hand)

    total = sum(fingers)

    # FIST
    if total == 0:
        return "PUNCH"

    # POINT
    if fingers == [0, 1, 0, 0, 0]:
        return "MOVE"

    # PEACE
    if fingers == [0, 1, 1, 0, 0]:
        return "SPECIAL"

    # OPEN HAND
    if total == 5:
        return "BLOCK"

    # THUMBS UP
    if fingers == [1, 0, 0, 0, 0]:

        if hand[4].y < hand[3].y:
            return "POWER"

    return "MOVE"


def draw_fighter(
    frame,
    x,
    y,
    health,
    name,
    enemy=False,
    attack=False,
    block=False
):

    # ========================================================
    # BODY
    # ========================================================

    if enemy:
        body_color = (0, 0, 255)
    else:
        body_color = (255, 100, 0)

    # Head
    cv2.circle(
        frame,
        (x, y - 100),
        25,
        (200, 180, 150),
        -1
    )

    # Body
    cv2.rectangle(
        frame,
        (x - 30, y - 75),
        (x + 30, y),
        body_color,
        -1
    )

    # Legs
    cv2.line(
        frame,
        (x - 15, y),
        (x - 25, y + 60),
        body_color,
        12
    )

    cv2.line(
        frame,
        (x + 15, y),
        (x + 25, y + 60),
        body_color,
        12
    )

    # ========================================================
    # ARMS
    # ========================================================

    if attack:

        if enemy:

            cv2.line(
                frame,
                (x - 25, y - 60),
                (x - 90, y - 65),
                body_color,
                12
            )

        else:

            cv2.line(
                frame,
                (x + 25, y - 60),
                (x + 90, y - 65),
                body_color,
                12
            )

    elif block:

        # Arms in front
        cv2.line(
            frame,
            (x - 25, y - 60),
            (x - 5, y - 40),
            body_color,
            12
        )

        cv2.line(
            frame,
            (x + 25, y - 60),
            (x + 5, y - 40),
            body_color,
            12
        )

    else:

        cv2.line(
            frame,
            (x - 25, y - 60),
            (x - 55, y - 25),
            body_color,
            10
        )

        cv2.line(
            frame,
            (x + 25, y - 60),
            (x + 55, y - 25),
            body_color,
            10
        )

    # ========================================================
    # HEALTH BAR
    # ========================================================

    bar_width = 160

    bar_x = x - 80
    bar_y = y - 145

    cv2.rectangle(
        frame,
        (bar_x, bar_y),
        (bar_x + bar_width, bar_y + 20),
        (50, 50, 50),
        -1
    )

    health_width = int(
        bar_width * max(health, 0) / 100
    )

    cv2.rectangle(
        frame,
        (bar_x, bar_y),
        (bar_x + health_width, bar_y + 20),
        (0, 200, 0),
        -1
    )

    cv2.putText(
        frame,
        name,
        (bar_x, bar_y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


def reset_game():

    global player_x
    global player_health
    global enemy_x
    global enemy_health
    global game_over
    global winner
    global hit_effect
    global attack_cooldown
    global special_cooldown

    player_x = 180
    player_health = 100

    enemy_x = 700
    enemy_health = 100

    game_over = False
    winner = ""

    hit_effect = 0

    attack_cooldown = 0
    special_cooldown = 0


# ============================================================
# MAIN LOOP
# ============================================================

last_timestamp = 0

while True:

    ret, camera = cap.read()

    if not ret:
        print("Failed to capture image")
        break

    # Mirror camera
    camera = cv2.flip(camera, 1)

    camera = cv2.resize(
        camera,
        (WIDTH, HEIGHT)
    )

    # ========================================================
    # MEDIA PIPE
    # ========================================================

    rgb = cv2.cvtColor(
        camera,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    timestamp = int(
        time.time() * 1000
    )

    if timestamp <= last_timestamp:
        timestamp = last_timestamp + 1

    last_timestamp = timestamp

    results = landmarker.detect_for_video(
        mp_image,
        timestamp
    )

    gesture = "NO HAND"

    # ========================================================
    # HAND DETECTED
    # ========================================================

    if results.hand_landmarks:

        hand = results.hand_landmarks[0]

        # ====================================================
        # DRAW HAND LANDMARKS
        # ====================================================

        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (5, 6), (6, 7), (7, 8),
            (5, 9), (9, 10), (10, 11), (11, 12),
            (9, 13), (13, 14), (14, 15), (15, 16),
            (13, 17), (17, 18), (18, 19), (19, 20),
            (0, 17)
        ]

        for a, b in connections:

            x1 = int(hand[a].x * WIDTH)
            y1 = int(hand[a].y * HEIGHT)

            x2 = int(hand[b].x * WIDTH)
            y2 = int(hand[b].y * HEIGHT)

            cv2.line(
                camera,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                3
            )

        for i, point in enumerate(hand):

            x = int(point.x * WIDTH)
            y = int(point.y * HEIGHT)

            if i in [4, 8, 12, 16, 20]:

                cv2.circle(
                    camera,
                    (x, y),
                    9,
                    (0, 255, 255),
                    -1
                )

            else:

                cv2.circle(
                    camera,
                    (x, y),
                    5,
                    (255, 255, 255),
                    -1
                )

        # Highlight index finger
        index_x = int(hand[8].x * WIDTH)
        index_y = int(hand[8].y * HEIGHT)

        cv2.circle(
            camera,
            (index_x, index_y),
            25,
            (0, 255, 255),
            3
        )

        # ====================================================
        # GESTURE
        # ====================================================

        gesture = get_gesture(hand)

        # ====================================================
        # MOVE PLAYER
        # ====================================================

        if gesture == "MOVE":

            # Map hand position to left/right side
            player_x = int(
                hand[8].x * 600
            ) + 50

            player_x = max(
                80,
                min(400, player_x)
            )

        # ====================================================
        # PUNCH
        # ====================================================

        if gesture == "PUNCH":

            if attack_cooldown <= 0:

                player_attack = True

                # Check enemy distance
                if abs(player_x - enemy_x) < 170:

                    damage = 10

                    if not enemy_block:

                        enemy_health -= damage

                        hit_effect = 8

                        hit_x = enemy_x
                        hit_y = enemy_y - 70

                attack_cooldown = 20

        else:

            player_attack = False

        # ====================================================
        # SPECIAL
        # ====================================================

        if gesture == "SPECIAL":

            if special_cooldown <= 0:

                player_special = True

                if abs(player_x - enemy_x) < 250:

                    damage = 25

                    if not enemy_block:

                        enemy_health -= damage

                        hit_effect = 15

                        hit_x = enemy_x
                        hit_y = enemy_y - 70

                special_cooldown = 80

        else:

            player_special = False

        # ====================================================
        # BLOCK
        # ====================================================

        if gesture == "BLOCK":

            player_block = True

        else:

            player_block = False

        # ====================================================
        # POWER
        # ====================================================

        if gesture == "POWER":

            player_health = min(
                100,
                player_health + 1
            )

    # ========================================================
    # COOLDOWNS
    # ========================================================

    if attack_cooldown > 0:
        attack_cooldown -= 1

    if special_cooldown > 0:
        special_cooldown -= 1

    # ========================================================
    # ENEMY AI
    # ========================================================

    if not game_over:

        # Move toward player
        if enemy_x > player_x + 100:

            enemy_x -= 2

        elif enemy_x < player_x - 100:

            enemy_x += 2

        # Random attack
        if (
            abs(enemy_x - player_x) < 150 and
            time.time() - last_enemy_attack > 1
        ):

            enemy_attack = True

            if not player_block:

                player_health -= random.randint(
                    5,
                    12
                )

                hit_effect = 8

                hit_x = player_x
                hit_y = player_y - 70

            last_enemy_attack = time.time()

        else:

            enemy_attack = False

    # ========================================================
    # GAME OVER
    # ========================================================

    if player_health <= 0:

        player_health = 0
        game_over = True
        winner = "ENEMY WINS!"

    if enemy_health <= 0:

        enemy_health = 0
        game_over = True
        winner = "YOU WIN!"

    # ========================================================
    # DRAW FIGHTERS
    # ========================================================

    draw_fighter(
        camera,
        player_x,
        player_y,
        player_health,
        "YOU",
        False,
        player_attack or player_special,
        player_block
    )

    draw_fighter(
        camera,
        enemy_x,
        enemy_y,
        enemy_health,
        "ENEMY",
        True,
        enemy_attack,
        enemy_block
    )

    # ========================================================
    # SPECIAL ATTACK EFFECT
    # ========================================================

    if player_special:

        cv2.circle(
            camera,
            (enemy_x, enemy_y - 70),
            70,
            (255, 0, 255),
            5
        )

        cv2.putText(
            camera,
            "SPECIAL!",
            (enemy_x - 70, enemy_y - 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 255),
            3
        )

    # ========================================================
    # HIT EFFECT
    # ========================================================

    if hit_effect > 0:

        cv2.circle(
            camera,
            (hit_x, hit_y),
            30 + hit_effect * 2,
            (0, 255, 255),
            4
        )

        cv2.putText(
            camera,
            "HIT!",
            (hit_x - 35, hit_y - 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            3
        )

        hit_effect -= 1

    # ========================================================
    # HUD
    # ========================================================

    cv2.rectangle(
        camera,
        (0, 0),
        (WIDTH, 80),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        camera,
        f"GESTURE: {gesture}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        camera,
        "POINT=MOVE  FIST=PUNCH  PEACE=SPECIAL  OPEN=BLOCK",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2
    )

    # ========================================================
    # GAME OVER SCREEN
    # ========================================================

    if game_over:

        cv2.rectangle(
            camera,
            (180, 210),
            (720, 440),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            camera,
            winner,
            (280, 300),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.3,
            (255, 255, 255),
            3
        )

        cv2.putText(
            camera,
            "PRESS R TO RESTART",
            (285, 360),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    # ========================================================
    # SHOW
    # ========================================================

    cv2.imshow(
        "Hand Controlled Fighting Game",
        camera
    )

    # ========================================================
    # KEYBOARD
    # ========================================================

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == ord("r"):
        reset_game()

# ============================================================
# CLEAN UP
# ============================================================

cap.release()
cv2.destroyAllWindows()
landmarker.close()

