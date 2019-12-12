# Python Implementation of the Peculiar Holidays Calendar
# (holiday generation algorithm only -- no UI)

from datetime import datetime,timedelta,date
from bitarray import bitarray
from icalendar import Calendar, Event
import pytz

# Note: Most of this code is canon & cannot be changed without disrupting the holidays.

R_SCALE = 2**32;
LEGEND_RATE = 0.0026 * R_SCALE;
RARE_RATE = 0.006 * R_SCALE;
SPEC_RATE = 0.04 * R_SCALE;
REG_RATE = 0.11 * R_SCALE;

types = [
    "* Day", "* Day", "* Dawn", "* Morning", "* Lunch", "* Evening", "* Night", "* Eve",
    "* Fest", "* Festival", "* Dance", "* Ball", "* Feast", "* Faire", "*'s Day",
    "*fest", "*ween", "*mas", "*sgiving", "*tide", "*morn", "*day", "*DOW", "*DOW",
    "Day", "Morning", "Brunch", "Lunch", "Evening", "Night",
    "Fest", "Festival", "Dance", "Ball", "Dinner", "Feast", "Faire", "Celebration",
];

topics = [
    # 0 - WATER ANIMALS
    "Fish", "Shark", "Whale", "Dolphin", "Seal", "Squid", "Octopus", "Eel",
    "Turtle", "Frog", "Penguin", "Otter", "Crayfish", "Lobster", "Crab", "Starfish",
    "Tadpole", "Jellyfish", "Carp", "Catfish", "Sunfish", "Swordfish", "*Tuna", "Seagull",
    "Koi", "Goldfish", "Serpent", "Minnow", "Trout", "Salmon", "Ray", "Oyster",
    # 1 - DOMESTIC ANIMALS
    "Dog", "Cat", "Cow", "Sheep", "Horse", "Goat", "Chicken", "Duck",
    "Goose", "Llama", "Rabbit", "Guinea Pig", "Pig", "Parrot", "Mouse", "Rat",
    "Bull", "Ox", "Ram", "Peacock", "Hen", "Rooster", "Pigeon", "Dove",
    "Dog Park", "Housecat", "Alley Cat", "Pup", "Puppy", "Kitten", "Hound", "*Fetching",
    # 2 - INSECTS / SMALL ANIMALS
    "Fly", "Butterfly", "Dragonfly", "Mosquito", "Spider", "Beetle", "Ant", "Wasp",
    "Bee", "Cicada", "Grasshopper", "Cricket", "Pillbug", "Snail", "Slug", "Scorpion",
    "Toad", "Lizard", "Salamander", "Centipede", "Mite", "Hedgehog", "Gnat", "Mole",
    "Moth", "Orb Weaver", "Jumping Spider", "Squirrel", "Raccoon", "Opossum", "Chipmunk", "Skunk",
    # 3 - WILD ANIMALS
    "Bird", "Sparrow", "Hawk", "Owl", "Crow", "Deer", "Bear", "Groundhog",
    "Elk", "Beaver", "Wolf", "Fox", "Boar", "Elephant", "Lion", "Tiger",
    "Bobcat", "Panda", "Monkey", "Ape", "Coyote", "Hippopotamus", "Alligator", "Buffalo",
    "Mammoth", "Dinosaur", "Velociraptor", "T-Rex", "Panther", "Jaguar", "Giraffe",
    # 4 - MYTHICAL CREATURES
    "Dragon", "Gryphon", "Centaur", "Unicorn", "Werewolf", "Vampire", "Jackalope", "Yeti",
    "Sasquatch", "Elf", "Dwarf", "Faerie", "Witch", "Wizard", "Hydra", "Kraken",
    "Minotaur", "Basilisk", "Golem", "Troll", "Ogre", "Giant", "Bigfoot", "Alien",
    "Serpent", "Wyrm", "Angel", "Demon", "Satyr", "Sprite", "Goblin", "Mummy",
    # 5 - HOUSEHOLD
    "Table", "Chair", "Bed", "Couch", "Spoon", "Knife", "Fork", "Mug",
    "Glass", "Mirror", "Door", "Window", "Stairs", "Attic", "Basement", "Computer",
    # 6 - MEDIA
    "Book", "Poem", "Zine", "Blog", "*Painting", "*Drawing", "Photo", "Sculpture",
    "Model", "Record", "Album", "Song", "*Design", "Font", "Logo", "Article",
    # 7 - GEOGRAPHY
    "Mountain", "Hill", "Glade", "Cliff", "Ocean", "Lake", "River", "Creek",
    "Prarie", "Desert", "Valley", "Tundra", "Forest", "Jungle", "Woods", "Swamp",
    "Grove", "Wetland", "Clearing", "Plain", "Canyon", "Wasteland", "City", "Farm",
    "Stream", "Coast", "Beach", "Island", "Rainforest", "Tropics", "Cavern", "Cave",
    # 8 - FLORA / WEATHER
    "Tree", "Root", "Bark", "Leaf", "Branch", "Twig", "Fern", "Flower",
    "Seed", "Mushroom", "Fruit", "Houseplant", "Berry", "Vine", "Shrub", "Sapling",
    "Storm", "Wind", "Rain", "Gale", "Lightning", "Thunder", "Mist", "Sunshine",
    # 9 - OCCUPATIONS
    "Builder", "Teacher", "Leader", "Clerk", "Servant", "Artist", "Writer", "Manager",
    "Repairer", "Farmer", "Driver", "Librarian", "Merchant", "Mender", "Officer", "Caretaker",
    "Baker", "Cook", "Assistant", "Doctor",
    # 10 - HOBBIES
    "*Knitting", "*Sewing", "*Storytelling", "*Singing", "*Dancing", "*Gaming", "*Science", "*Physics",
    "*Gardening", "*Mathematics", "*Traveling", "*Cooking", "*Puzzling", "*Collecting", "*Reading", "*Coding",
    # 11 - TOOLS / INSTRUMENTS
    "Shovel", "Rake", "Hammer", "Saw", "Plow", "Blade", "Bow", "Knife",
    "Guitar", "Piano", "Flute", "Violin", "Trumpet", "Bass", "Synth", "Drum",
    "Harp", "Horn", "Viola", "Cello", "Banjo", "Ukulele", "Shaker", "Cowbell",
    # 12 - COSMOS
    "Star", "Sun", "Moon", "Comet", "Meteor", "Galaxy", "Satellite", "Cloud",
    "Planet", "Void", "Abyss", "Nebula", "Vortex", "Dream", "Cosmos", "Light",
    # 13 - ACTIVITIES
    "*Troublemaking", "*Hugs", "*High-Fives", "*Snacks", "*Letters", "*Notes", "*Giving", "*Trading",
    "*Compliments", "*Friend-Making", "*Challenges", "*Competitions", "*Games", "*Contests", "*Sports", "*Jokes",
    # 14 - TRINKETS
    "Button", "Pin", "Hat", "Hair", "Mustache", "Glasses", "Notebook", "Ribbon",
    "Hankerchief", "Doll", "Ring", "Necklace", "Tattoo", "Memento", "Trinket", "Charm",
    # 15 - CREATIVE
    "*Nonsense", "*Improv", "*Play", "*Short-Stories", "*Doodling", "*Crayons", "*Rhymes", "*DIY-ing",
    "*Sketches", "*Daydreaming", "Journal", "Sketchbook", "*Tabletop Games", "*Crafting", "*Visiting", "*Exploring",
    # 16 - RELATIONSHIPS
    "Father", "Mother", "Sister", "Brother", "Grandfather", "Grandmother", "Aunt", "Uncle",
    "Niece", "Nephew", "Cousin", "Sibling", "Son", "Daughter", "Child", "Friend",
    # 17 - FOOD
    "Cereal", "Roll", "Cassarole", "Pasta", "Oatmeal", "Sandwich", "Burger", "Pizza",
    "Dessert", "Roast", "Salad", "Panini", "Taco", "Burrito", "Tofu", "Vegetables",
    "Omelette", "Chili", "Stir Fry", "Sauce", "Jerky", "Wrap", "Pie", "Pot Pie",
    "Beans", "Bread", "Muffins", "Cupcakes", "Cake", "Scones", "Peanut Butter", "Peanut",
    "Cashew", "Almond", "Smoothie", "Milkshake", "Soda", "Lemonade", "Wine", "Juice",
    # 18 - CLOTHES
    "Shirt", "Suit", "Pants", "Tie", "Dress", "Shoes", "Socks", "Hat",
    "Briefs", "Underwear", "Belt", "Suspenders", "Bowtie", "Cap", "T-Shirt", "Pocket",
    # 19 - BODY PARTS
    "Hand", "Foot", "Leg", "Nose", "Eye", "Ear", "Chin", "Arm",
    # 20 - Misc
    "Mischief", "Fool", "MONTH", "MONTH", "MONTH", "MONTH", "MONTH",
];

spring = [
    "Spring", "Mud", "Dirt", "Earth", "Daffodil", "Robin", "Petal", "Clover",
    "Morel", "*Mist", "Strawberry", "Blueberry", "*Rain", "Thunderstorm", "Grass", "Dandelion",
    "Tulip", "Crocus", "Lily", "*Green", "*Brown", "*Water", "Blossum", "Pear", "Bulb",
    "Rhubarb", "Potato", "*Fertility", "*Romance", "Wren", "*Flirtation", "*Life", "*Rebirth",
    "Jam", "Marmalade", "Greens", "Pollen", "Nest", "*Awakening", "Songbird", "Melody",
    "Tune", "*Harmony", "*Nature", "Sprout", "Sapling", "Baby", "Egghunt", "*Lace",
    "MONTH",
];

summer = [
    "Summer", "Heat", "Pool", "Daisy", "Black-Eyed Susan", "Marigold", "Hibiscus", "Sunflower",
    "Rose", "Apricot", "Cherry", "Raspberry", "Blackberry", "Plum", "Mango", "Beach",
    "Jam", "Drought", "Campfire", "*Yellow", "*Fire", "Sand", "Finch", "*Love",
    "*Friendship", "*Bread", "*Ice Cream", "Watermelon", "*Treats", "Egg", "Eggplant", "Avocado",
    "Skirt", "Shorts", "Sandals", "Sprinkler", "Pond", "Barbeque", "Grill", "Cookout",
    "*Hiking", "Deck", "Lawn", "Garden", "Fire Pit", "*Camping", "Camp", "Tent",
    "MONTH",
];

autumn = [
    "Autumn", "Fall", "*Leaves", "*Orange", "*Red", "*Purple", "Bonfire", "Squash",
    "Pumpkin", "Tomato", "Mums", "Begonia", "Grackle", "Dead", "Ghost", "Skeleton",
    "*Witchcraft", "Cauldron", "Spell", "Harvest", "Turkey", "Gratitude", "Cider", "Apple",
    "Cinnamon", "Maple", "*Plaid", "*Flannel", "*Boots", "Scarecrow", "Raven", "*Tea",
    "Vest", "Jacket", "Hoodie", "Hayride", "*Soup", "Cardigan", "Scare", "Syrup",
    "Vision", "Nightmare", "Starling", "Coffin", "Graveyard", "Corn", "Tombstone", "Boot",
    "MONTH"
];

winter = [
    "Winter", "*Frost", "*Snow", "*Ice", "*Blue", "Blanket", "Fireplace", "Coat",
    "Scarf", "Mitten", "Junco", "Cardinal", "Sled", "*Bells", "*Carols", "*Death",
    "*Sleep", "*Silence", "*Presents", "*Cookies", "*Brownies", "Pancake", "*Nog", "*Cocoa",
    "*Chocolate", "*Spirits", "Snowman", "Snowball", "*Coffee", "*Fog", "*Sleet", "Nap",
    "Sweater", "Toy", "Tinsel", "Stew", "Chowder", "Waffle", "Sugar", "Candy",
    "Chimney", "Nutmeg", "Ginger", "Snowflake", "Popcorn", "Cookie", "*Hibernation", "Candle",
    "MONTH"
];

adjs = [
    # 0 - EMOTION
    "Happy", "Friendly", "Grumpy", "Grouchy", "Sleepy", "Furious", "Giddy", "Playful",
    "Silly", "Sad", "Melancholy", "Frightened", "Thoughtful", "Caring", "Bubbly", "Lovesick",
    # 1 - TONE
    "Sanguine", "Serene", "Peaceful", "Spooky", "Haunted", "Somber", "Reflective", "Delighted",
    "Jubilant", "Serious", "Professional", "Comical", "Triumphant", "Dramatic", "Grandiloquent", "Fancy",
    # 2 - TEXTURE
    "Sandy", "Rough", "Smooth", "Sharp", "Dull", "Solid", "Squishy", "Spiky",
    "Scratchy", "Soft", "Hard", "Fuzzy", "Lumpy", "Velvet", "Slimy", "Clammy",
    # 3 - SIZE / FLAVOR
    "Little", "Big", "Tiny", "Miniature", "Gigantic", "Enormous", "Bulky", "Short",
    "Tall", "Long", "Wide", "Stout", "Sweet", "Bitter", "Sour", "Spicy",
    # 4 - BEHAVIOR
    "Dancing", "Leaping", "Jumping", "Sleeping", "Shouting", "Barking", "Chattering", "Hungry",
    "Singing", "Clapping", "Fighting", "Sneaky", "Disorganized", "Clean", "Sexy", "Disgruntled",
    "Troublesome", "Quarrelsome", "Itchy", "Clamboring", "Clumsy", "Pouting", "Obstinate", "Ironic",
    "Curious", "Disagreeable", "Obnoxious", "Seductive", "Alluring", "Rambling", "Blathering",
    # 5 - MATERIAL
    "Silver", "Golden", "Iron", "Copper", "Wooden", "Paper", "Stone", "Foam",
    "Ghostly", "Ethereal", "Fiery", "Icy", "Electric", "Clay", "Brass",
    "Bronze", "Tin", "Granite", "Marble", "Plastic", "Cardboard", "Glass", "Abstract",
    # 6 - APPEARANCE
    "Shiny", "Colorful", "Rainbow", "Beautiful", "Lovely", "Pretty", "Ugly", "Crisp",
    "Checkered", "Ornate", "Furry", "Hairy", "Jeweled", "Striped", "Spotted", "Plaid",
    # 7 - TIME
    "Early", "Late", "Immortal", "Ancient", "Youthful", "Young", "Fledgling", "Elder",
    "Vintage", "Prompt", "Retro", "Classic", "Midnight", "Endless", "Eternal", "Infinite",
    # 8 - QUALITY
    "Flawless", "Perfect", "Pristine", "Dirty", "Broken", "Scuffed", "Grimy", "Rare",
    "New", "Fashionable", "Damaged", "Recycled", "Indie", "Hipster", "Pop", "Punk",
    "Goth", "Emo", "Cool", "Stylish", "Secondhand", "Exquisite", "Custom", "DIY",
    "Uppity", "Elitist", "High-Class", "Trashy", "Muddy", "Bloody", "Gross", "Sticky",
    # 9 - CHARACTERISTICS
    "Toothless", "Delicious", "Sturdy", "Responsible", "Funky", "Formidable", "Charismatic", "Eccentric",
    "Eloquent", "Timid", "Quiet", "Noisy", "Independent", "Dizzy", "Hypnotic", "Melodic",
    "Obscure", "Loquacious", "Ominous", "Suspicious", "Blunt", "Befuddling", "Encrypted", "Obfuscated",
    "Confounding", "Darn", "Divine", "Omnipotent", "Clever", "Cunning", "Robotic", "Digital",
    # 10- PERSONALITY
    "Timid", "Ornery", "Bratty", "Chatty", "Lazy", "Kind", "Seedy", "Trustworthy",
    "Sly", "Mischevious", "Generous", "Compassionate", "Caring", "Emotional", "Lackadaisical", "Scatterbrained",
    "Focused", "Orderly", "Messy", "Social", "Long-Winded", "Rebel", "Anarchist", "Competitive",
    "Cantankerous", "Magnanimous", "Benevolent", "Bright", "Intelligent", "Personable", "Agreeable", "Merciful",
    # 11- ESSENCE
    "Spiritual", "Demonic", "Holy", "Unholy", "Tranquil", "Enlightened", "Astral", "Cosmic",
    "Radiant", "Hypothetical", "Metaphorical", "Mythological", "Legendary", "Soul", "Dark", "Light",
    # 12- VALUE
    "Expensive", "Cheap", "Luxury", "Worthless", "Designer", "Unique", "Authentic", "Discount",
    "Refurbished", "Priceless", "Irreplaceable", "Premium", "Lackluster", "Antique", "Imitation", "Counterfeit",
    "Critical", "Non-essential", "Essential", "Extra", "Superfluous", "Redundant", "Affordable", "Unreasonable",
    # 13- RELATIONAL
    "Affectionate", "Single", "Family", "Commanding", "Listening", "Lonely", "Lonesome", "Annoying",
    "Pestering", "Diplomatic", "Empathetic", "Popular", "Loyal", "Party", "Pretentious", "Judgemental",
    "Inconsiderate", "Rude", "Polite", "Gentle", "Tender", "Mild-Mannered", "Loud", "Rowdy",
    "Rambunctious", "Aloof", "Dedicated", "Mean", "Cruel", "Kindhearted", "Nurturing", "Wise",
    # 14- COLOR
    "Red", "Orange", "Yellow", "Green", "Blue", "Violet", "Pink", "White",
    "Black", "Gray", "Brown", "Tan", "Crystal", "Invisible", "Metallic", "Chromatic",
    # 15- MISC
    "Audio", "Video", "Cyber", "Futuristic", "Dangerous", "Burning", "Damp", "Smelly",
    "Petrified", "Literary", "Controversial", "Existential", "Metaphysical", "Philosophical", "Celebratory", "Wireless",
    "Baby", "Viral", "Internet", "Electronic", "Noble", "Mini", "Mega", "Harmonious", "Entrepreneurial", "Smokey",
    "Sprouting", "Snoozing", "Awakening",
];

monthNames = ["January", "February", "March", "April",
                  "May", "June", "July", "August",
                  "September", "October", "November", "December"];

weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

class Dice:
    def __init__(self,date):
        self.rollA = 0
        self.rollB = 0
        self.initRolls(date)

    # Pesudorandom Number Generator (32-bit xorshift)
    def roll(self,state):
        ary = bitarray()
        for i in range(32):
            ary.append(state & 1)
            state = state >> 1
        ary2 = bitarray()
        for i in range(13):
            ary2.append(0)
        ary2.extend(ary[0:32-13])
        ary ^= ary2

        ary2 = ary[17:len(ary)]
        for i in range(17):
            ary2.append(0)

        ary ^= ary2

        ary2 = bitarray()
        for i in range(5):
            ary2.append(0)
        ary2.extend(ary[0:32-5])

        ary ^= ary2
        state = 0
        for i in range(32):
            if(i == 0 and ary[31] == 1):
                state = -1
            else:
                state = state + ary[31-i]
            if(i != 31):
                state = state << 1
        #state ^= state << 13
        #state ^= state >> 17
        #state ^= state << 5
        #print("STATE: " + str(state+(2**31-1)))
        return state+(2**31-1)

    def initRolls(self,date):
        seed = -1123581321345589
        self.rollA = self.roll(dateSum(date,True)+seed)
        self.rollB = self.roll(dateSum(date,False)+seed)

    def nextA(self):
        self.rollA = self.roll(self.rollA)
        self.rollB = self.roll(self.rollB)
        return self.rollA

    def nextB(self):
        self.rollA = self.roll(self.rollA)
        self.rollB = self.roll(self.rollB)
        return self.rollB

    
def divideYear(date):
    return int((date.year+yearOffset(date))/yearDivisor(date))

def yearDivisor(date):
    return 1 + (5-(date.day%6))

def yearOffset(date):
    return date.day%11

def legendYear(date):
    return (date.year+yearOffset(date))%yearDivisor(date) == 0

def dateSum(date, divYear):
    sm = 0
    if(divYear):
        sm = divideYear(date)
    else:
        sm = date.year

    sm *= 12
    sm += date.month-1
    sm *= 31
    sm += date.day-1
    return sm

# converts Python weekdays (0 = Monday) to JavaScript weekdays (0 = Sunday)
def wdConvert(weekday):
    return (weekday+1)%7

def buildHoliday(quality, htype, topic, seasonal, adj, tone, date):
    base = ""
    spec = ""
    if(htype == None or (topic == None and seasonal == None)):
        return ""

    if(topic == "MONTH"):
        topic = monthNames[date.month-1]
    
    if(seasonal == "MONTH"):
        seasonal = monthNames[date.month-1]
    
    if(htype[0] == '*'):
        base = htype[1:len(htype)]
        if(base == "DOW"):
           base = " " + weekdays[wdConvert(date.weekday())]
        
        if(tone != None):
            spec = tone
        
        if(adj != None):
            if(spec != ""):
                spec += " "
            spec += adj
        
        if(seasonal != None):
            if(seasonal[0] == '*'):
                seasonal = seasonal[1:len(seasonal)]

            if(spec != ""):
                spec += " "
            spec += seasonal
        
        if(topic != None):
            if(topic[0] == '*'):
               topic = topic[1:len(topic)]

            if(spec != ""):
                spec += " "
            spec += topic
        
        base = (spec + base).strip()
    else:
        base = htype + " of"

        if(tone != None):
            base = tone + " " + base

        needsThe = True

        if(adj != None):
            spec = adj
        
        if(seasonal != None):
            if(seasonal[0] == '*'):
                needsThe = False
                seasonal = seasonal[1:len(seasonal)]

            if(spec != ""):
                spec += " "
            spec += seasonal
        
        if(topic != None):
            if(topic[0] == '*'):
                needsThe = False
                topic = topic[1:len(topic)]
            else:
                needsThe = True

            if(spec != ""):
                spec += " "
            spec += topic
        
        if(needsThe):
            base = base + " the"
        
        base = (base + " " + spec).strip()

    return base

def getHolidayForDate(date, include_pips=False, include_quality=False):
    # get a pair of dice, seeded from this date
    # the first value is based on a divided year (for repetition)
    # the second value is based on an unaltered year
    # different elements use different dice, depending on whether they should repeat
    dice = Dice(date)

    season = None
    if(date.month < 3 or date.month == 12):
        season = winter
    elif(date.month < 6):
        season = spring
    elif(date.month < 9):
        season = summer
    else:
        season = autumn
    
    htype = None
    topic = None
    seasonal = None
    adj = None
    tone = None

    qRoll = dice.nextA()
        
    if(qRoll < LEGEND_RATE and legendYear(date)): # A LEGENDARY HOLIDAY ??
        htype = types[dice.nextB()%len(types)]
        topic = topics[dice.nextB()%len(topics)]
        seasonal = season[dice.nextB()%len(season)]
        adj = adjs[dice.nextB()%len(adjs)]
        tone = adjs[dice.nextB()%len(adjs)]
        hday = buildHoliday("legend", htype, topic, seasonal, adj, tone, date)
        if(include_pips):
            hday = "~!~ " + hday + " ~!~"
        if(include_quality):
            return (hday,"Legendary")
        else:
            return hday
    elif(qRoll < RARE_RATE): # Ooh, a rare holiday!
        htype = types[dice.nextA()%len(types)]
        mixRoll = dice.nextB()%4

        if(mixRoll == 0): # ADJ+SEAS+TOPIC+TYPE
            topic = topics[dice.nextA()%len(topics)]
            seasonal = season[dice.nextA()%len(season)]
            adj = adjs[dice.nextB()%len(adjs)]
        elif(mixRoll == 1): # TONE+SEAS+TOPIC+TYPE
            topic = topics[dice.nextA()%len(topics)]
            seasonal = season[dice.nextA()%len(season)]
            tone = adjs[dice.nextB()%len(adjs)]
        elif(mixRoll == 2): # TONE+ADJ+TOPIC+TYPE
            topic = topics[dice.nextA()%len(topics)]
            adj = adjs[dice.nextB()%len(adjs)]
            tone = adjs[dice.nextB()%len(adjs)]
        else: # TONE+ADJ+SEAS+TYPE
            seasonal = season[dice.nextA()%len(season)]
            adj = adjs[dice.nextB()%len(adjs)]
            tone = adjs[dice.nextB()%len(adjs)]

        hday = buildHoliday("rare", htype, topic, seasonal, adj, tone, date)
        if(include_pips):
            hday = "** " + hday + " **"
        if(include_quality):
            return (hday,"Rare")
        else:
            return hday
        
    elif(qRoll < SPEC_RATE): # A special holiday
        htype = types[dice.nextA()%len(types)]
        mixRoll = dice.nextA()%5

        if(mixRoll == 0): # SEAS+TOPIC+TYPE
            topic = topics[dice.nextA()%len(topics)]
            seasonal = season[dice.nextA()%len(season)]
        elif(mixRoll == 1): # ADJ+TOPIC+TYPE
            topic = topics[dice.nextA()%len(topics)]
            adj = adjs[dice.nextA()%len(adjs)]
        elif(mixRoll == 2): # ADJ+SEAS+TYPE
            seasonal = season[dice.nextA()%len(season)]
            adj = adjs[dice.nextA()%len(adjs)]
        elif(mixRoll == 3): # TONE+TOPIC+TYPE
            topic = topics[dice.nextA()%len(topics)]
            tone = adjs[dice.nextA()%len(adjs)]
        else: # TONE+SEASON+TYPE
            seasonal = season[dice.nextA()%len(season)]
            tone = adjs[dice.nextA()%len(adjs)]

        hday =  buildHoliday("special", htype, topic, seasonal, adj, tone, date)
        if(include_pips):
            hday = "+ " + hday + " +"
        if(include_quality):
            return (hday,"Special")
        else:
            return hday
        
    elif(qRoll < REG_RATE): # A regular holiday
        htype = types[dice.nextA()%len(types)]
        if(dice.nextA()%2==0):
            topic = topics[dice.nextA()%len(topics)]
        else:
            seasonal = season[dice.nextA()%len(season)]

        hday = buildHoliday("regular", htype, topic, seasonal, adj, tone, date)
        if(include_quality):
            return (hday,"Regular")
        else:
            return hday
    else:
        # No holiday on this date.
        if(include_quality):
            return ("","None")
        return ""

# Generate the calendar!
syear = 2019
eyear = 2060

# counts holidays so we don't put too many on the calendar (>1000 is iffy in Google Cal)
ecount = 0

cal = Calendar()
cal.add('prodid','-//Peculiar Holidays//www.nashhigh.com//')
cal.add('version','1.0')

for y in range(syear,eyear):
    print("YEAR: " + str(y) + " of " + str(eyear))
    for m in range(1,13):
        for d in range(1,32):
            if(ecount < 1000):
                #if(y == syear):
                #    print("DATE: " + str(y)+"/"+str(m)+"/"+str(d))
                try:
                    #dt = datetime(y,m,d,tzinfo=pytz.utc)
                    dt = date(y,m,d)
                except:
                    dt = None
                if(dt != None):
                    hday = getHolidayForDate(dt,include_pips=True,include_quality=True)
             
                    if(hday[0] != ""):
                        #print(hday)
                        ecount += 1
                        evt = Event()
                        evt.add('summary',hday[0])
                        evt.add('description',hday[1]+" Holiday")
                        evt.add('dtstart',dt)
                        #evt.add('dtend',date+timedelta(days=1))
                        evt.add('dtend',dt+timedelta(days=1))
                        evt.add('dtstamp',dt)
                        cal.add_component(evt)
                        if(ecount == 1000):
                            print("1000 HOLIDAYS REACHED")

fl = open("PeculiarHolidays.ics","wb")
fl.write(cal.to_ical())
fl.close()

#nog = []

#for y in range(2019,2039):
#    for m in range(12):
#        for d in range(31):
#            try:
#                nog.append(datetime.date(y,m+1,d+1))
#            except:
#                pass

#for n in nog:
#    hday = getHolidayForDate(n)
#    if(hday != ""):
#        print(str(n.year)+"/"+str(n.month)+"/"+str(n.day)+" " + getHolidayForDate(n,include_pips=True))
