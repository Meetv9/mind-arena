# -*- coding: utf-8 -*-
"""
content.py — The full content library for MIND ARENA.

Everything the game draws from lives here:
  * 200+ speaking prompts / topics / props / "images" (emoji visual props)
  * A large brain-teaser bank (riddles, lateral, logic, quick-math, patterns)
  * The four+ progressive "boss" challenge generators
  * A speaking-coach teaching section (confidence, sounding excellent, voice
    exercises, breathing, tongue twisters)

Nothing here needs the internet. It is pure data + a few random generators so
the game always works offline.
"""

import random
import string

# ---------------------------------------------------------------------------
# 1) SPEAKING PROMPTS  (200 of them)
#    Each item is (emoji_prop, prompt_text).  The emoji acts as the "random
#    picture / prop" the user must weave into the mini-speech.
# ---------------------------------------------------------------------------

SPEECH_PROMPTS = [
    ("🕰️", "If you could freeze time for everyone but yourself, what is the first thing you would do?"),
    ("🌋", "Describe a volcano to someone who has never seen one — make them feel the heat."),
    ("📻", "Sell an old radio to a teenager who has only ever used streaming apps."),
    ("🪐", "You are the first tour guide of Saturn's rings. Give the opening speech."),
    ("🧦", "Deliver a heartfelt eulogy for a single lost sock."),
    ("🔑", "This key opens one door in the world. Convince us which door it should be."),
    ("🦑", "Explain the daily life of a deep-sea squid as if narrating a nature film."),
    ("🎈", "A balloon can carry one message across the sky. What does it say and why?"),
    ("🧭", "You found a compass that points to what you want most. Describe the journey."),
    ("🪞", "Talk to your reflection from ten years ago for sixty seconds."),
    ("🌩️", "Persuade a village that a coming storm is actually good news."),
    ("🧩", "Argue that life is more like a jigsaw puzzle than a race."),
    ("🐢", "Defend the tortoise's strategy in a world obsessed with speed."),
    ("🎷", "Describe the sound of a saxophone to someone who has never heard music."),
    ("🕯️", "Give a toast at a dinner lit only by a single candle."),
    ("🚂", "You are a train that has decided to stop following the tracks. Explain."),
    ("🌵", "Teach a survival lesson using only what a cactus knows."),
    ("📮", "Write and deliver the last letter ever sent by post."),
    ("🎭", "Convince us that wearing a mask reveals more than it hides."),
    ("🧠", "Give a pep talk to your own brain before an important exam."),
    ("🪁", "Explain freedom using only the idea of a kite and its string."),
    ("🐝", "Pitch the bee's case for being the most important worker on Earth."),
    ("🌊", "Describe the ocean to a desert dweller in a way that makes them cry."),
    ("🔦", "You control the only flashlight in a blackout. Address the crowd."),
    ("🎨", "Defend a painting that everyone else calls ugly."),
    ("⏳", "Argue that patience is a superpower, not a weakness."),
    ("🌙", "Speak on behalf of the Moon, tired of always being second to the Sun."),
    ("🧊", "Sell ice to someone living at the North Pole — and win."),
    ("📚", "Give a passionate speech about the smell of an old library."),
    ("🚀", "Announce the launch of humanity's first mission to nowhere in particular."),
    ("🦉", "Explain why the wise owl chose to stay awake all night."),
    ("🎂", "Deliver a birthday toast for someone turning 100."),
    ("🌉", "Describe a bridge that connects two people who have never met."),
    ("🧵", "Argue that a single thread can change the whole fabric of a life."),
    ("🐙", "You are an octopus applying for a human office job. Ace the interview."),
    ("🕳️", "Explain what you would find at the bottom of an endless hole."),
    ("🎯", "Convince us that missing the target taught you more than hitting it."),
    ("🌱", "Give the opening words a seed would say before becoming a tree."),
    ("🔔", "Ring an imaginary bell and announce the most important news of the century."),
    ("🧳", "You may pack only three ideas for the rest of your life. Defend them."),
    ("🐉", "Introduce a dragon as the new mayor of your city."),
    ("🍄", "Explain the secret social network of mushrooms beneath the forest."),
    ("⚓", "Argue that staying anchored can be braver than sailing away."),
    ("🎁", "Describe the best gift that costs absolutely nothing."),
    ("🌪️", "You are the calm eye of a tornado. Reassure everyone around you."),
    ("🪙", "Flip a coin's perspective: speak as the side that always loses."),
    ("🦇", "Defend the bat against centuries of bad reputation."),
    ("📷", "Describe the one photograph you would save from a burning house."),
    ("🧭", "Give directions to happiness as if it were a real place on a map."),
    ("🎺", "Rally an army using only the courage of a single trumpet note."),
    ("🌰", "Explain how something small and hard can hold an entire forest."),
    ("🚦", "Argue that the yellow light is the most misunderstood one."),
    ("🐧", "You are a penguin who dreams of the desert. Make your case."),
    ("🕊️", "Deliver a two-minute plea for one day of worldwide silence."),
    ("🔥", "Describe fire to someone who has only ever known cold."),
    ("🪀", "Explain the philosophy of a yo-yo that keeps coming back."),
    ("🎢", "Argue that the drop is the best part of any roller coaster — and of life."),
    ("🧲", "You are a magnet. Explain what and who you are drawn to and why."),
    ("🌻", "Give a motivational talk from the point of view of a sunflower."),
    ("📡", "Announce first contact with an alien civilization to planet Earth."),
    ("🕶️", "Defend the idea that sometimes we see clearest through a shaded lens."),
    ("🧱", "Argue that walls, not bridges, are what some moments need."),
    ("🐛", "Narrate the exact moment a caterpillar decides to change."),
    ("🎻", "Describe heartbreak using only the language of a violin."),
    ("🌈", "Explain a rainbow to someone who cannot see color."),
    ("🪤", "Warn a friend about the most tempting trap you can imagine."),
    ("🧥", "This coat was worn by someone remarkable. Tell their story."),
    ("🛎️", "You are the concierge of dreams. Welcome a new guest for the night."),
    ("🌾", "Give a speech honoring the invisible farmers behind every meal."),
    ("🔮", "You can see one day into everyone's future. Should you tell them?"),
    ("🐺", "Defend the lone wolf's choice to leave the pack."),
    ("🎪", "Announce the greatest show that has never happened."),
    ("🧴", "Sell a bottle of 'bottled courage' — describe its effects."),
    ("🌡️", "Argue that discomfort is the body's way of asking us to grow."),
    ("🪐", "Describe what silence sounds like in outer space."),
    ("🎤", "You have one line before the microphone is cut. Make it count."),
    ("🐦", "Teach us to sing using only what a morning bird knows."),
    ("🧊", "Explain how the coldest moment of your life warmed your heart."),
    ("🚁", "You can hover over any place on Earth for one hour. Describe it."),
    ("📖", "Argue that the best stories are the ones we never finish."),
    ("🌵", "Give a love letter from a cactus to the rain."),
    ("🎩", "Pull one impossible idea out of a hat and defend it seriously."),
    ("🐘", "Explain memory using everything an elephant would tell you."),
    ("🕹️", "Argue that life should have a pause button — and what you'd do with it."),
    ("🌊", "You are the last wave before the tide goes out. Say goodbye."),
    ("🔗", "Describe the strongest chain in the world and its weakest link."),
    ("🎨", "Convince us that the empty part of the canvas is the real art."),
    ("🐌", "Defend slowness in a culture addicted to fast."),
    ("🌟", "You are a star that just went out. Tell us what you shone on."),
    ("🧯", "Give calm instructions during an imaginary emergency."),
    ("📅", "Argue that we should celebrate ordinary Tuesdays."),
    ("🦋", "Explain transformation without using the word 'change'."),
    ("🎬", "Direct the opening scene of the movie of your life."),
    ("🏔️", "Describe the view from a mountain no one has ever climbed."),
    ("🔋", "You are running on 1% battery. What is worth the last of your energy?"),
    ("🌵", "Teach resilience using three lessons from the desert."),
    ("🧭", "You are a compass that has fallen in love with going in circles."),
    ("🐳", "Deliver the whale's message to humanity from the deep ocean."),
    ("🎇", "Describe fireworks to someone who thinks the sky should stay quiet."),
    ("🪶", "Explain how something as light as a feather can tip a decision."),
    ("🚪", "There are two doors: certainty and adventure. Convince us to open one."),
    ("🧬", "Give a speech to your future descendants a hundred years from now."),
    ("🌵", "Argue that thorns are just a plant's way of loving carefully."),
    ("🎲", "Defend the role of luck in a story everyone credits to skill."),
    ("🕰️", "You are the last minute of the year. What do you say to everyone?"),
    ("🐜", "Explain teamwork using nothing but an ant colony."),
    ("🌤️", "Describe the exact feeling of the first warm day after winter."),
    ("🔑", "You lost the key to a room you can never re-enter. Reflect."),
    ("🎈", "Argue that letting go can be the bravest thing you ever do."),
    ("🦁", "Give a courage lesson from a lion who was once afraid."),
    ("📞", "You get one phone call to anyone, living or dead. Explain the call."),
    ("🌵", "Sell 'doing nothing' as the most productive activity of all."),
    ("🧭", "Describe getting wonderfully, usefully lost."),
    ("🐝", "Argue that busyness and productivity are not the same thing."),
    ("🌋", "You are pressure building underground. Explain what you will become."),
    ("🎺", "Announce the return of something everyone thought was gone forever."),
    ("🪞", "Convince a stranger they are stronger than they think."),
    ("🌊", "Describe the difference between drowning and learning to float."),
    ("🔥", "Give a campfire speech that everyone will remember tomorrow."),
    ("🧊", "Argue that keeping your cool is an underrated act of courage."),
    ("🎨", "You can repaint one memory. Describe the new colors."),
    ("🐢", "Teach us how to carry our home on our back, wherever we go."),
    ("🌙", "Comfort someone who is awake at 3 a.m. and cannot sleep."),
    ("📚", "Argue that one book changed the entire course of human history."),
    ("🚀", "You have fuel for one launch. Where does humanity go?"),
    ("🕯️", "Describe hope using only a single flame in complete darkness."),
    ("🐉", "Explain that the dragon we fear is usually one we invented."),
    ("🌱", "Give a graduation speech to a class of tiny seedlings."),
    ("🎯", "Argue that the goal you missed pointed you to a better one."),
    ("🧵", "You are the last thread holding something together. Speak up."),
    ("🌵", "Convince a raindrop it matters, even in an ocean."),
    ("🐙", "Explain how to keep your head when everything grabs at you at once."),
    ("🎪", "Introduce the strangest, most wonderful act under the big top."),
    ("🔦", "Describe finding light in a place everyone said was hopeless."),
    ("🌊", "You are a message in a bottle. Reach whoever finds you."),
    ("🧭", "Argue that the best maps are the ones we draw ourselves."),
    ("🐦", "Teach an old bird to sing a brand-new song."),
    ("🌡️", "Describe the exact temperature of a perfect memory."),
    ("🎁", "You must give away your greatest talent. To whom, and why?"),
    ("🪐", "Speak as gravity, tired of always being taken for granted."),
    ("🔔", "Announce a small victory as if it were the biggest news in the world."),
    ("🌵", "Argue that being 'too much' is exactly enough for the right people."),
    ("🐺", "Give the speech that finally brings the lone wolf back home."),
    ("🎬", "Narrate the plot twist no one in your life saw coming."),
    ("🏔️", "Convince someone the climb is worth it before they've taken a step."),
    ("🔋", "Describe what recharges you when nothing else works."),
    ("🌟", "You get to name a brand-new constellation. Tell its story."),
    ("🧯", "Talk a friend down from a decision they'll regret."),
    ("📅", "Argue that today, right now, is the youngest you'll ever be."),
    ("🦋", "Describe the ugly, uncomfortable middle of becoming who you are."),
    ("🎤", "You are opening for the greatest speaker alive. Warm up the crowd."),
    ("🐳", "Explain loneliness and largeness using the biggest creature alive."),
    ("🎇", "Give the toast that ends the party and starts the memory."),
    ("🪶", "Argue that gentleness is a form of strength most people miss."),
    ("🚪", "Describe the feeling of closing one chapter to open another."),
    ("🧬", "You carry the stories of everyone before you. Introduce them."),
    ("🌵", "Teach patience using a plant that blooms once in a lifetime."),
    ("🎲", "Convince a gambler that the surest bet is on himself."),
    ("🕰️", "You have exactly one minute left. Say what actually matters."),
    ("🐜", "Argue that the smallest consistent effort beats the biggest burst."),
    ("🌤️", "Describe optimism to someone who has forgotten how it feels."),
    ("🔑", "You found the key to a locked part of yourself. Open it out loud."),
    ("🎈", "Give the speech a child needs to hear before their first big fear."),
    ("🦁", "Explain that real courage is being scared and showing up anyway."),
    ("📞", "You have thirty seconds on the line before it drops. Say it now."),
    ("🌊", "Describe standing at the shore of a decision you can't un-make."),
    ("🧭", "Argue that 'lost' and 'exploring' are the same thing seen differently."),
    ("🐝", "Give a speech thanking the small, unseen people who kept you going."),
    ("🌋", "You have held something in for years. Let it out — carefully."),
    ("🎺", "Sound the call that wakes a sleeping town to its own potential."),
    ("🪞", "Tell the truth to someone who only wants to hear a comforting lie."),
    ("🌊", "Describe the calm that comes right after the hardest storm."),
    ("🔥", "Reignite the passion of someone who has stopped trying."),
    ("🧊", "Argue that stillness can move people more than noise."),
    ("🎨", "You are the color no one picks. Make your case to be chosen."),
    ("🐢", "Explain how being last taught you to enjoy the whole road."),
    ("🌙", "Give the goodnight speech the whole world secretly needs."),
    ("📚", "You are the final page of a great book. Say goodbye to the reader."),
    ("🚀", "Describe the feeling of leaving everything familiar behind."),
    ("🕯️", "Teach someone to be their own light when the room goes dark."),
    ("🐉", "Convince a hero that the real dragon was fear all along."),
    ("🌱", "Give the speech a comeback deserves after a long, hard winter."),
    ("🎯", "Argue that aiming at nothing is the surest way to hit it."),
    ("🧵", "Describe how one small kindness unraveled into something huge."),
    ("🌵", "Teach us to bloom exactly where we were planted."),
    ("🐙", "Explain doing many things at once without losing yourself in any."),
    ("🎪", "Take a final bow and thank the audience of your life."),
    ("🔦", "Point your light at the one thing everyone keeps ignoring."),
    ("🌊", "Ride the last big wave and tell us what the ocean taught you."),
    ("🧭", "Deliver the speech that finally sends you in the right direction."),
    ("🐦", "You are free of the cage at last. Describe your first flight."),
    ("🌟", "This is the last star before dawn. Give the world one final wish."),
    ("🎤", "The lights are on you. You have earned this moment. Begin."),
    ("🧩", "You are the missing piece that just found where it belongs. Speak."),
    ("🕊️", "Give the shortest, most powerful speech about peace you can."),
    ("🌍", "You have sixty seconds to address the entire human race. Go."),
    ("☂️", "Convince someone that dancing in the rain beats waiting for it to stop."),
    ("🧭", "You are a road that has never been travelled. Invite the first walker."),
    ("🪁", "Explain ambition using a kite that wants to cut its own string."),
    ("🍵", "Give a two-minute meditation on the ritual of a single cup of tea."),
    ("🛠️", "Argue that the thing most worth building is a better version of yourself."),
    ("🌒", "Describe the courage it takes to keep glowing while only half-seen."),
    ("🎢", "You are the fear at the top of the first drop. Talk yourself over the edge."),
    ("📀", "Explain nostalgia to someone who has never lost anything yet."),
    ("🧗", "Give the last words of encouragement before someone's biggest leap."),
    ("🔭", "You found a new star. Convince the world it's worth looking up for."),
]

# ---------------------------------------------------------------------------
# 2) BRAIN TEASERS  (riddles, lateral, logic, quick math, patterns)
#    Each: {"q": question, "a": answer, "type": category, "hint": optional}
# ---------------------------------------------------------------------------

BRAIN_TEASERS = [
    {"type": "Riddle", "q": "The more you take, the more you leave behind. What am I?", "a": "Footsteps."},
    {"type": "Riddle", "q": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "a": "An echo."},
    {"type": "Riddle", "q": "What has keys but opens no locks, space but no room, and you can enter but not go in?", "a": "A keyboard."},
    {"type": "Riddle", "q": "I'm tall when I'm young and short when I'm old. What am I?", "a": "A candle."},
    {"type": "Riddle", "q": "What has a head, a tail, is brown, and has no legs?", "a": "A penny."},
    {"type": "Riddle", "q": "What can travel around the world while staying in a corner?", "a": "A stamp."},
    {"type": "Riddle", "q": "What has hands but cannot clap?", "a": "A clock."},
    {"type": "Riddle", "q": "The person who makes it sells it. The person who buys it never uses it. The person who uses it never knows it. What is it?", "a": "A coffin."},
    {"type": "Riddle", "q": "What gets wetter the more it dries?", "a": "A towel."},
    {"type": "Riddle", "q": "What has many teeth but cannot bite?", "a": "A comb (or a zipper)."},
    {"type": "Riddle", "q": "What has one eye but cannot see?", "a": "A needle."},
    {"type": "Riddle", "q": "What has a neck but no head?", "a": "A bottle."},
    {"type": "Riddle", "q": "What runs but never walks, has a bed but never sleeps?", "a": "A river."},
    {"type": "Riddle", "q": "What can you catch but not throw?", "a": "A cold."},
    {"type": "Riddle", "q": "What has cities but no houses, forests but no trees, and water but no fish?", "a": "A map."},
    {"type": "Lateral", "q": "A man lives on the 10th floor. Every morning he takes the elevator down. Coming back, he rides to the 7th floor and walks the rest — except on rainy days, when he rides all the way up. Why?", "a": "He's short and can only reach the 7th-floor button; on rainy days he has an umbrella to reach higher."},
    {"type": "Lateral", "q": "A woman shoots her husband, holds him underwater for five minutes, then hangs him. Minutes later they enjoy dinner together. How?", "a": "She's a photographer: shoots a photo, develops it underwater, hangs it to dry."},
    {"type": "Lateral", "q": "Two fathers and two sons go fishing. Each catches one fish, yet only three fish are caught. How?", "a": "They are grandfather, father, and son — three people, two of whom are fathers and two are sons."},
    {"type": "Lateral", "q": "A man pushes his car to a hotel and instantly knows he's bankrupt. Why?", "a": "He's playing Monopoly."},
    {"type": "Lateral", "q": "What can fill a room but takes up no space?", "a": "Light (or sound)."},
    {"type": "Lateral", "q": "Forward I'm heavy, backward I'm not. What am I?", "a": "The word 'ton'."},
    {"type": "Lateral", "q": "A cowboy rides into town on Friday, stays three days, and leaves on Friday. How?", "a": "His horse is named Friday."},
    {"type": "Logic", "q": "Some months have 31 days, some have 30. How many have 28 days?", "a": "All 12 of them."},
    {"type": "Logic", "q": "If a doctor gives you 3 pills and says take one every 30 minutes, how long until they're gone?", "a": "One hour (0, 30, 60 minutes)."},
    {"type": "Logic", "q": "A farmer has 17 sheep and all but 9 die. How many are left?", "a": "Nine."},
    {"type": "Logic", "q": "You enter a dark room with a match, a lamp, a candle, and a fireplace. What do you light first?", "a": "The match."},
    {"type": "Logic", "q": "How many times can you subtract 10 from 100?", "a": "Once — after that you're subtracting from 90."},
    {"type": "Logic", "q": "A rooster lays an egg on the peak of a slanted roof. Which way does it roll?", "a": "Neither — roosters don't lay eggs."},
    {"type": "Logic", "q": "Which is heavier: a kilogram of feathers or a kilogram of steel?", "a": "They weigh the same — one kilogram each."},
    {"type": "Logic", "q": "A man builds a house with all four walls facing south. A bear walks by. What color is it?", "a": "White — the house is at the North Pole, so it's a polar bear."},
    {"type": "Logic", "q": "Before Mount Everest was discovered, what was the tallest mountain on Earth?", "a": "Mount Everest — it existed before it was discovered."},
    {"type": "Logic", "q": "If two's company and three's a crowd, what are four and five?", "a": "Nine."},
    {"type": "Math", "q": "I am an odd number. Take away one letter and I become even. What number am I?", "a": "Seven (remove the 's' → 'even')."},
    {"type": "Math", "q": "A bat and a ball cost 1.10 together. The bat costs 1.00 more than the ball. How much is the ball?", "a": "5 cents (the bat is 1.05)."},
    {"type": "Math", "q": "If it takes 5 machines 5 minutes to make 5 widgets, how long for 100 machines to make 100 widgets?", "a": "5 minutes."},
    {"type": "Math", "q": "A lily pad doubles in size every day and covers the lake in 48 days. On what day was it half-covered?", "a": "Day 47."},
    {"type": "Math", "q": "There are 100 pairs of dogs. Two dogs have puppies. Each has litters... Actually, how many legs total for 100 dogs?", "a": "400 legs."},
    {"type": "Math", "q": "Divide 30 by half and add 10. What do you get?", "a": "70 (30 ÷ 0.5 = 60, + 10)."},
    {"type": "Math", "q": "What three positive numbers give the same result when added and multiplied?", "a": "1, 2, and 3 (1+2+3 = 1×2×3 = 6)."},
    {"type": "Math", "q": "Count the number of times the digit 9 appears from 1 to 100.", "a": "Twenty times."},
    {"type": "Math", "q": "A clock strikes 6 in 5 seconds. How long to strike 12?", "a": "11 seconds (11 intervals of 1 second)."},
    {"type": "Pattern", "q": "What comes next: 1, 1, 2, 3, 5, 8, 13, ?", "a": "21 (Fibonacci — sum of the previous two)."},
    {"type": "Pattern", "q": "What comes next: 2, 6, 12, 20, 30, ?", "a": "42 (differences increase by 2: n×(n+1))."},
    {"type": "Pattern", "q": "What comes next: O, T, T, F, F, S, S, ?", "a": "E (first letters of One, Two, Three... → Eight)."},
    {"type": "Pattern", "q": "What comes next: 1, 4, 9, 16, 25, ?", "a": "36 (perfect squares)."},
    {"type": "Pattern", "q": "What comes next: 3, 6, 11, 18, 27, ?", "a": "38 (differences 3,5,7,9,11)."},
    {"type": "Pattern", "q": "Decode: J, F, M, A, M, J, J, ?", "a": "A (first letters of the months → August)."},
    {"type": "Pattern", "q": "What comes next: 1, 2, 4, 8, 16, ?", "a": "32 (doubling)."},
    {"type": "Pattern", "q": "What comes next: 100, 96, 88, 76, 60, ?", "a": "40 (subtract 4, 8, 12, 16, 20)."},
    {"type": "Wordplay", "q": "What word becomes shorter when you add two letters to it?", "a": "'Short' → 'shorter'."},
    {"type": "Wordplay", "q": "What five-letter word becomes shorter when you add two letters?", "a": "'Short'."},
    {"type": "Wordplay", "q": "What English word has three consecutive double letters?", "a": "'Bookkeeper' (oo-kk-ee)."},
    {"type": "Wordplay", "q": "Name a word that is spelled the same forwards and backwards and means 'noon'.", "a": "'Noon' itself — a palindrome."},
    {"type": "Wordplay", "q": "What starts with 'e', ends with 'e', but contains only one letter?", "a": "An envelope."},
    {"type": "Wordplay", "q": "What word is always spelled incorrectly?", "a": "'Incorrectly'."},
    {"type": "Wordplay", "q": "What 7-letter word contains dozens of letters?", "a": "'Mailbox'."},
    {"type": "Lateral", "q": "A girl kicks a ball. It goes 10 feet, then comes right back to her. How?", "a": "She kicked it straight up."},
    {"type": "Lateral", "q": "What can you hold in your right hand but never in your left?", "a": "Your left elbow."},
    {"type": "Lateral", "q": "What goes up but never comes down?", "a": "Your age."},
    {"type": "Lateral", "q": "A man walks into a bar and asks for water. The bartender pulls a gun. The man says 'thank you' and leaves. Why?", "a": "He had hiccups; the scare cured them."},
    {"type": "Riddle", "q": "What breaks yet never falls, and what falls yet never breaks?", "a": "Day breaks and night falls."},
    {"type": "Riddle", "q": "What has 13 hearts but no other organs?", "a": "A deck of cards."},
    {"type": "Riddle", "q": "What invention lets you look right through a wall?", "a": "A window."},
    {"type": "Riddle", "q": "What has a bottom at the top?", "a": "Your legs."},
    {"type": "Riddle", "q": "What building has the most stories?", "a": "A library."},
]

# ---------------------------------------------------------------------------
# 3) PROGRESSIVE "BOSS" CHALLENGES  (the final escalating round)
#    Each generator returns a dict describing a fresh, randomized challenge.
# ---------------------------------------------------------------------------

_FICTIONAL_JOBS = [
    "Underwater Rug Weaver", "Gravitational Boot Repairman", "Professional Cloud Shepherd",
    "Retired Time-Zone Inspector", "Certified Echo Tuner", "Volcano Barista",
    "Shadow Cartographer", "Moonlight Electrician", "Dream Traffic Controller",
    "Antique Silence Restorer", "Left-Handed Compass Whisperer", "Emotional Weather Forecaster",
    "Sneeze Choreographer", "Professional Nap Auditor", "Rainbow Quality Inspector",
    "Ghost Landlord", "Gravity Salesman", "Freelance Genie Consultant",
    "Municipal Yawn Coordinator", "Deep-Space Librarian",
]

_CHARACTERS = [
    "Sherlock Holmes", "Cleopatra", "a medieval knight", "a Viking explorer",
    "Albert Einstein", "a pirate captain", "Julius Caesar", "a Victorian butler",
    "a 1920s radio announcer", "Marie Curie", "a samurai warrior", "a cave-dweller",
    "a Shakespearean actor", "a robot from the year 3000", "a wild-west cowboy",
    "a French philosopher", "a superhero on their day off", "a wizard from a fantasy realm",
]

_MUNDANE_ACTIVITIES = [
    "ordering fast food", "fixing the Wi-Fi", "assembling flat-pack furniture",
    "waiting in a long queue", "unclogging a sink", "charging a phone",
    "finding a parking spot", "returning an online purchase", "making instant noodles",
    "arguing with a self-checkout machine", "untangling a pair of earphones",
    "reading the terms and conditions", "waiting for a software update",
]

_TABOO_TOPICS = [
    ("Cooking", ["food", "kitchen", "eat"]),
    ("Football", ["ball", "goal", "team"]),
    ("The Ocean", ["water", "fish", "wave"]),
    ("Music", ["sound", "song", "listen"]),
    ("School", ["teacher", "student", "learn"]),
    ("Winter", ["cold", "snow", "ice"]),
    ("A Birthday", ["cake", "gift", "party"]),
    ("Money", ["cash", "buy", "pay"]),
    ("Sleep", ["bed", "dream", "tired"]),
    ("The Internet", ["online", "website", "click"]),
    ("Travel", ["trip", "plane", "hotel"]),
    ("Coffee", ["cup", "drink", "morning"]),
]

_EMOTIONS = [
    "furious", "overjoyed", "terrified", "hopelessly in love", "deeply suspicious",
    "unbearably bored", "wildly excited", "melancholic", "smug and superior", "panicked",
]

_RANDOM_TOPICS_SIMPLE = [
    "your morning routine", "the last meal you ate", "how to tie your shoes",
    "your favourite season", "why the sky is blue", "the perfect weekend",
    "your commute to work", "how a pencil works", "the best film you've seen",
    "what makes a good friend",
]


def challenge_accidental_expert():
    job = random.choice(_FICTIONAL_JOBS)
    return {
        "name": "The Accidental Expert",
        "icon": "🎓",
        "brief": f"You are the world's leading **{job}**.",
        "task": f"Speak for 60 seconds explaining the *history* and *daily routine* of being a {job}, as if it is completely real and you are the top authority alive.",
        "trains": "Rapid lateral thinking, confidence, and creative storytelling under pressure.",
        "difficulty": 1,
    }


def challenge_alphabet_sprint():
    start = random.choice(string.ascii_uppercase[:20])  # avoid ending near Z
    seq = []
    c = start
    for _ in range(6):
        seq.append(c)
        c = chr(ord(c) + 1)
    return {
        "name": "Alphabet Soup Sprint",
        "icon": "🔤",
        "brief": f"Start your monologue with a sentence beginning with **'{start}'**.",
        "task": f"Every new sentence must begin with the next letter of the alphabet: {' → '.join(seq)} … and keep going. Stay coherent the whole time.",
        "trains": "Planning sentence structure ahead while keeping your current thought coherent.",
        "difficulty": 2,
    }


def challenge_reverse_interview():
    char = random.choice(_CHARACTERS)
    act = random.choice(_MUNDANE_ACTIVITIES)
    return {
        "name": "The Reverse Interview",
        "icon": "🎭",
        "brief": f"Become **{char}**.",
        "task": f"For 60 seconds, describe the utterly modern, mundane task of **{act}** — but entirely from {char}'s perspective, vocabulary, and worldview.",
        "trains": "Perspective-shifting, empathy mapping, and rapid vocabulary adaptation.",
        "difficulty": 2,
    }


def challenge_taboo_twist():
    topic, banned = random.choice(_TABOO_TOPICS)
    return {
        "name": "Taboo Topic Twist",
        "icon": "🚫",
        "brief": f"Talk about **{topic}**.",
        "task": f"Speak about {topic} for 60 seconds without ever saying: **{', '.join(banned)}**. If you slip, acknowledge it and push on.",
        "trains": "Escaping linguistic autopilot and triggering deep vocabulary retrieval.",
        "difficulty": 3,
    }


def challenge_emotion_rollercoaster():
    e1, e2, e3 = random.sample(_EMOTIONS, 3)
    topic = random.choice(_RANDOM_TOPICS_SIMPLE)
    return {
        "name": "Emotion Rollercoaster",
        "icon": "🎢",
        "brief": f"Topic: **{topic}**.",
        "task": f"Describe {topic} for 60 seconds, switching your emotional delivery every ~20 seconds: start **{e1}**, become **{e2}**, then finish **{e3}**. Make each shift obvious in your voice.",
        "trains": "Vocal range, emotional control, and tonal agility.",
        "difficulty": 3,
    }


def challenge_one_breath_ideas():
    topic = random.choice(_RANDOM_TOPICS_SIMPLE)
    return {
        "name": "The Rapid-Fire Reframe",
        "icon": "⚡",
        "brief": f"Topic: **{topic}**.",
        "task": f"Give as many *distinct* one-sentence angles on {topic} as you can in 60 seconds — no repeats, no 'um'. Every sentence must start with a different word than the last.",
        "trains": "Idea fluency, filler-word suppression, and quick reframing.",
        "difficulty": 3,
    }


# All boss challenges, roughly ordered by difficulty.
BOSS_CHALLENGES = [
    challenge_accidental_expert,
    challenge_alphabet_sprint,
    challenge_reverse_interview,
    challenge_taboo_twist,
    challenge_emotion_rollercoaster,
    challenge_one_breath_ideas,
]


def pick_boss_challenge(level: int):
    """Higher level → bias toward harder challenges for progressive difficulty."""
    if level <= 2:
        pool = BOSS_CHALLENGES[:3]
    elif level <= 5:
        pool = BOSS_CHALLENGES[1:5]
    else:
        pool = BOSS_CHALLENGES[2:]
    return random.choice(pool)()


# ---------------------------------------------------------------------------
# 4) SPEAKING COACH — the teaching section
# ---------------------------------------------------------------------------

TONGUE_TWISTERS = [
    "Red leather, yellow leather, red leather, yellow leather.",
    "She sells seashells by the seashore.",
    "Peter Piper picked a peck of pickled peppers.",
    "Unique New York, unique New York, you know you need unique New York.",
    "The lips, the teeth, the tip of the tongue.",
    "A proper copper coffee pot.",
    "Six sticky skeletons sat and swayed.",
    "Toy boat, toy boat, toy boat.",
    "Which witch wished which wicked wish?",
    "Betty bought a bit of better butter.",
    "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
    "Fresh fried fish, fish fresh fried.",
]

VOICE_WARMUPS = [
    ("🌬️ Diaphragm breathing (30s)", "Sit tall. Inhale through the nose for 4 counts so your belly — not your chest — expands. Hold 2. Exhale slowly through pursed lips for 6. Repeat. This is the engine of a strong, steady voice."),
    ("🎵 The Siren (20s)", "On an 'ooo' sound, glide your pitch smoothly from your lowest note up to your highest and back down, like a slow siren. It stretches your full vocal range and warms the cords gently."),
    ("💆 Lip trills / 'brrr' (20s)", "Let your lips flutter as you hum a tune (like blowing a raspberry with sound). Releases tension in the lips and jaw and evens out airflow — a singer's secret."),
    ("🗣️ Over-articulate (30s)", "Read a tongue twister three times: first ridiculously slow and exaggerated, then medium, then fast but still crisp. Precision first, speed second."),
    ("😮 Big yawn-sigh (10s)", "Yawn wide, then sigh out on an open 'ahh'. Opens the throat and drops the larynx for a warmer, rounder tone."),
    ("💪 Neck & jaw roll (15s)", "Slowly roll your neck, then gently massage the jaw hinge and drop your jaw open-shut. Tension in the jaw chokes your resonance."),
]

COACH_CONFIDENCE = [
    "**Own the pause.** Silence feels long to you, powerful to them. When you finish a key point, stop for a full second. Pauses signal control, not uncertainty.",
    "**Kill the up-talk.** Ending sentences with a rising, question-like pitch makes statements sound unsure. Land your sentences with a firm, downward tone.",
    "**Plant your feet, open your chest.** Posture feeds your voice and your brain. Stand tall, shoulders back — you'll literally breathe better and sound more certain.",
    "**Slow down 20%.** Nervous speakers rush. Deliberate pace signals authority and gives your brain time to choose better words. Aim for ~130–150 words per minute.",
    "**Replace fillers with silence.** 'Um', 'uh', 'like', 'you know' are just pauses with noise. Train yourself to simply close your mouth and pause instead.",
    "**Speak in three-beat chunks.** Group ideas in threes ('faster, sharper, clearer'). The brain loves triads and they sound rehearsed and confident.",
]

COACH_EXCELLENCE = [
    "**Vary your pitch (prosody).** A monotone loses people in seconds. Consciously go higher on excitement, lower on gravity. Range = interest.",
    "**Use vocal dynamics.** Change volume too — drop to near-whisper to pull people in, rise to punch a point. Contrast is what the ear remembers.",
    "**Paint pictures, not lists.** 'A rusty red bicycle leaning on a cracked wall' beats 'an old bike.' Concrete, sensory nouns make you sound vivid and prepared.",
    "**Emphasise the operative word.** In every sentence one word carries the meaning. Hit it a touch harder and slower. 'I never *said* she stole it' changes meaning by stress alone.",
    "**Breathe at the punctuation, not mid-thought.** Plan your breaths at commas and full stops so ideas stay whole and you never sound out of air.",
    "**End on a line, not a fade.** Great speakers land a final, deliberate sentence and stop. Don't trail off — button it and be silent.",
]

COACH_VOICE_HEALTH = [
    "**Hydrate, don't clear.** Throat-clearing slams the vocal cords together. Instead, sip water or do a gentle 'hmm' hum to reset.",
    "**Warm up before you push.** Never launch into loud speaking cold — do the siren and lip-trills first. Cold cords strain and crack (the 'harsh voice' feeling).",
    "**Support from the belly, not the throat.** If your voice feels rough or tired, you're probably pushing from the throat. Power comes from breath support underneath.",
    "**Steam and rest for roughness.** For a genuinely harsh/hoarse voice, inhale steam from a bowl of hot water, avoid whispering (it strains more than normal talk), and rest the voice.",
    "**Open the throat with the 'yawn-sigh'.** If your tone is tight or grating, yawn to drop the larynx and speak on that open, relaxed space.",
    "**Avoid the vocal-fry crutch.** That low, creaky register at the end of sentences drains authority and tires the cords. Keep breath support up through the last word.",
]

SPEECH_STRUCTURE_TIP = (
    "**A reliable 3-part skeleton for any impromptu speech (P-E-P):**\n\n"
    "1. **Point** — State your one main idea in a single clear sentence.\n"
    "2. **Example / Explain** — Give one story, reason, or vivid picture that proves it.\n"
    "3. **Point again** — Restate the idea as a punchy, memorable closing line.\n\n"
    "When in doubt, answer three questions out loud: *What is it? Why does it matter? What should we do?*"
)
