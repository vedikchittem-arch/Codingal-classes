# You are creating a crazy mood machine
# The machine starts with a normal face 
#  the user can press different keys to change the character's mood 
#  h -> happy 
#  s -> sad 
#  a -> angry 
#  t -> tired 
#  r -> reset to normal 
#  q -> quit 
#  the program should have a function "change_mood" (this is to pass the mood value) and this function
# should return the new emoji and mood message



import cv2
import numpy as np

def change_mood(mood):
    if mood == "happy":
        return "The character is feeling happy!"
    elif mood == "sad":
        return "The character is feeling sad!"
    elif mood == "angry":
        return "The character is feeling angry!"
    elif mood == "tired":
        return "The character is feeling tired!"
    elif mood == "normal":
        return "The character is feeling normal!"
    elif mood == "envious":
        return "The character is feeling envious"

mood = "normal"

print("Press the following keys to change the mood:")
print("h-happy")
print("s-sad")
print("a-angry")
print("t-tired")
print("r-reset to normal")
print("q-quit")

while True:

    message = change_mood(mood)

    image = np.ones((300, 500, 3), dtype=np.uint8) * 255

    cv2.putText(image, message, (40, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    cv2.imshow("Crazy Mood Machine", image)

    key = cv2.waitKey(0) & 0xFF

    if key == ord('h'):
        mood = "happy"
    elif key == ord('s'):
        mood = "sad"
    elif key == ord('a'):
        mood = "angry"
    elif key == ord('t'):
        mood = "tired"
    elif key == ord('r'):
        mood = "normal"
    elif key == ord('e'):
        mood = "envious"
    elif key == ord('q'):
        print("exiting ...")
        break
    else:
        print("Invalid key! Please use h,s,a,t,r,e,q")

cv2.destroyAllWindows()