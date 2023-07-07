#This program is a text-based RPG about exploring a haunted mansion and solving the mystery
import csv

class Room():

    def __init__(self, name, description, exits, items, monster):
        self.name = name
        self.description = description
        self.exits = exits
        self.room_items = items
        self.monster = monster

    def display_room(self, dict_of_items, dict_of_monsters):
        print("")
        print(self.name, end="\n\n")
        print(self.description, end="\n\n")
        if len(self.room_items) > 0:
            for i in range(len(self.room_items)):
                print(self.room_items[i], "\n")
                print(dict_of_items[self.room_items[i]], "\n")
        else:
            print("There are no items in this room.\n")
        if len(self.monster) > 0:
            print(self.monster[0], "\n")
            print(dict_of_monsters[self.monster[0]], "\n" )
        else:
            print("Whew, no monsters in here.\n")


    def move_room(self, direction):
        if direction in self.exits:
            return self.exits[direction]
    
    def get_exits(self):
        return self.exits

    def get_normal_exits(self):
        normal_exits = list(self.exits.items())[:4]
        return normal_exits

    def unabbr_input(uInput):
        if uInput == "n":
            return "north"
        elif uInput == "e":
            return "east"
        elif uInput == "s":
            return "south"
        elif uInput == "w":
            return "west"

    def place_item(self, item):
        self.room_items.append(item)

    def checkForItem(self):
        if len(self.room_items) != 0:
            return True
        else:
            return False

    def get_items(self):
        item_list = self.room_items
        return item_list

    def grab_item(self, item):
        self.room_items.remove(item)

    def checkForWin(self):
        if len(self.room_items) == 3:
            return True
        else:
            return False

    def checkForMonsters(self):
        if len(self.monster) != 0:
            return True
        else:
            return False

    def defeat_monster(self):
        del self.monster[0]

    def handle_input(room_dict, item_dict, monster_dict):
        hasNotQuit = True
        hasNotBeatGhost = True
        hasNotBeatSpider = True
        hasNotBeatSkele = True
        currentRoom = "Foyer"
        directions = ["north", "east", "south", "west"]
        abbr_directions = ["n", "e", "s", "w"]
        special_actions = ["jump", "crawl"]
        monster_rooms = ["Kitchen", "Den", "Cigar Lounge"]
        quit_commands = ["quit", "q"]
        user_inventory = []

        while hasNotQuit == True:
            room_exits = Room.get_exits(room_dict[currentRoom])
            if currentRoom == "Foyer" and Room.checkForWin(room_dict[currentRoom]) == True:
                print("You Win!")
                hasNotQuit = False
                quit()
            
            elif currentRoom in monster_rooms:
                if currentRoom == "Kitchen" and Room.checkForMonsters(room_dict[currentRoom]) == True:
                    while hasNotBeatGhost == True:
                        print("Ahhhh, there's a ghost in here! What will you do?\n")
                        choice = input(">").lower()
                        print("")
                        if choice == "run":
                            print("No, running away from him...\n")
                        elif choice == "fight":
                            print("You swipe at the ghost with a broom and he vanishes, nice work!\n")
                            Room.defeat_monster(room_dict[currentRoom])
                            hasNotBeatGhost = False
                        elif choice == "hide":
                            print("I think this ghost can still see you... try something else.\n")

                elif currentRoom == "Den" and Room.checkForMonsters(room_dict[currentRoom]) == True:
                    while hasNotBeatSpider == True:
                        print("Whoa, there's a giant spider in here! What will you do?\n")
                        choice = input(">").lower()
                        print("")
                        if choice == "run":
                            print("With that many legs, no way a human can out run this spider...\n")
                        elif choice == "fight":
                            print("You throw a rock at the spider... it does nothing.\n")
                        elif choice == "hide":
                            print("You hide behind the couch, the spider sees nothing and leaves the mansion.\n")
                            hasNotBeatSpider = False
                            Room.defeat_monster(room_dict[currentRoom])

                elif currentRoom == "Cigar Lounge" and Room.checkForMonsters(room_dict[currentRoom]) == True:
                    while hasNotBeatSkele == True:
                        print("Yikes, there's a skeleton in the doorway! What will you do?\n")
                        choice = input(">").lower()
                        print("")
                        if choice == "run":
                            print("You charge into the doorway and burst the skeleton into pieces.\n")
                            hasNotBeatSkele = False
                            Room.defeat_monster(room_dict[currentRoom])
                        elif choice == "fight":
                            print("You go to throw a punch but... you miss.\n")
                        elif choice == "hide":
                            print("You close your eyes and hope the skeleton doesn't see you... he sees you.\n")

            userInput = input(">").lower()
             
            if userInput in quit_commands:
                hasNotQuit = False

            elif userInput == "look":
                print("")
                print(Room.get_normal_exits(room_dict[currentRoom]))

            elif userInput == "locate":
                Room.display_room(room_dict[currentRoom], item_dict, monster_dict)

            elif userInput == "grab":
                if Room.checkForItem(room_dict[currentRoom]) == True:
                    print("Which item would you like to grab?\n")
                    room_items = Room.get_items(room_dict[currentRoom])
                    print(room_items, "\n")
                    choice = input(">").lower().capitalize()
                    if choice in room_items:
                        Room.grab_item(room_dict[currentRoom], choice)
                        user_inventory.append(choice)
                        print("\nYou grabbed the", choice.lower(), "from this room.\n")
                    else:
                        print("There is no item with that name in this room\n")

            elif userInput == "place":
                if len(user_inventory) == 0:
                    print("You have no items")
                else:
                    print("\nWhich item would you like to place?\n")
                    print(user_inventory, "\n")
                    choice = input(">").lower().capitalize()
                    if choice in user_inventory:
                        Room.place_item(room_dict[currentRoom], choice)
                        user_inventory.remove(choice)
                        print("\nYou have placed the", choice.lower(), "in this room.\n")
                    else: 
                        print("You do not have an item with that name.\n")

            elif userInput in special_actions:
                if room_exits[userInput.capitalize()]:
                    currentRoom = SpecialRoom.move_special_room(room_dict[currentRoom], userInput.capitalize())
                    SpecialRoom.display_room(room_dict[currentRoom], item_dict, monster_dict)
                else:
                    print("Cannot perform action here...\n")

            elif userInput in directions or abbr_directions:
                if userInput in abbr_directions:
                    userInput = Room.unabbr_input(userInput)
    
                if room_exits[userInput.capitalize()]:
                    currentRoom = Room.move_room(room_dict[currentRoom], userInput.capitalize())
                    Room.display_room(room_dict[currentRoom], item_dict, monster_dict)
                else:
                    print("There is no exit this way...\n")
            
            else:
                print("Enter a valid command\n")

        
class SpecialRoom(Room):
    def __init__(self, name, description, exits):
        super.__init__(name, description, exits)

    def move_special_room(self, special):
        if special in self.exits:
            return self.exits[special]

def make_rooms():
    room_dict = {}
    with open("C:/Users/Alex/inf308_2022_spring-newpowalex/programs/Final_Project/rooms2.tsv") as rooms:
        room_reader = csv.reader(rooms, delimiter="\t")
        next(room_reader)
        for row in room_reader:
            room = "%s" % row[0]
            room_dict[room] = {}
            room_exits = {}
            items = []
            monsters = []
            north = "%s" % row[2]
            room_exits["North"] = north
            east = "%s" % row[3]
            room_exits["East"] = east
            south = "%s" % row[4]
            room_exits["South"] = south
            west = "%s" % row[5]
            room_exits["West"] = west
            jump = "%s" % row[6]
            room_exits["Jump"] = jump
            crawl = "%s" % row[7]
            room_exits["Crawl"] = crawl
            room_item = row[8]
            if room_item != "":
                items.append(room_item)
            room_monster = row[9]
            if room_monster != "":
                monsters.append(room_monster)

            room_dict[room] = Room(room, row[1], room_exits, items, monsters)

    return room_dict

def make_items():
    item_dict = {}
    with open("C:/Users/Alex/inf308_2022_spring-newpowalex/programs/Track_Programs/Text-Based_RPG/items.tsv") as items:
        item_reader = csv.reader(items, delimiter="\t")
        next(item_reader)
        for row in item_reader:
            item = row[0]
            item_description = row[1]
            item_dict[item] = item_description
    
    return item_dict

def make_monsters():
    monster_dict = {}
    with open("C:/Users/Alex/inf308_2022_spring-newpowalex/programs/Final_Project/monsters.tsv") as monsters:
        monster_reader = csv.reader(monsters, delimiter="\t")
        next(monster_reader)
        for row in monster_reader:
            monster = row[0]
            monster_description = row[1]
            monster_dict[monster] = monster_description
    
    return monster_dict

def main():
    hasBegun = False
    while hasBegun == False:
        print("Hit 'ENTER' to start")
        answer = input(">").lower()
        if answer == "":
            dict_of_rooms = make_rooms()
            dict_of_items = make_items()
            dict_of_monsters = make_monsters()
            hasBegun = True
            print("\n(Game Started)\n")
            print("You have now entered The Haunted Mansion!\n\nIn order to calm the spirits in the mansion, you must find the three items scattered about and place them\nin the Foyer.\n")
            print("Actions:\n\t“Quit” - end the game\n\t“North” - move north\n\t“East” - move east\n\t“South” - move south\n\t“West” - move west\n\t“Look” - see the exits for that room\n\t“Locate” - display what room you are in\n\t“Grab” - pick up the item in that room\n\t“Place” - place an item from your inventory in that room\n")
            print("Monster Actions:\n\t'Run' - try and run away from monster\n\t'Fight' - try and fight the monster\n\t'Hide' - try and hide from the monster\n")
            print("Special Actions:\n\t“Jump” - access special rooms by trying this special action in certain rooms\n\t“Crawl” - access special rooms by trying this special action in certain rooms\n")
        else:
            continue

    Room.handle_input(dict_of_rooms, dict_of_items, dict_of_monsters)
                       
if __name__== "__main__" :
        main()
    
    


    
            

        

        

