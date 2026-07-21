user_1 = input("Greetings, enter your name please ")
chat_1 = "yes"
while chat_1 == "yes":
  mood_1 = input("How are you today ").lower()
  if mood_1 == "good":
    print("That is great to hear")
  elif mood_1 == "neutral":
    print("That is okay")
  elif mood_1 == "bad":
    print("I am sorry to hear that, I hope it will get better soon")
  
  hobb_1 = input("What are your favourite hobbies ")
  print(f"I also like {hobb_1}")
  chat_1 = input("Would you like to continue chatting ").lower()
  if chat_1 == "no":
    print(f"Goodbye {user_1}")
    break
  else:
    chat_1 == 'yes'
  


