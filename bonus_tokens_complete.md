# Zenith - Complete Bonus Tokens Information

## Source
Found in: `resources/boardgamearena.com/5/zenith.html` (line 2142)
The `bonus_ref` data structure contains the definitive list of all bonus tokens.

---

## Distribution of 16 Bonus Tokens

### Setup Distribution:
- **8 tokens placed on the board initially:**
  - 5 bonus tokens on the Planet board (one on each planet track)
  - 3 bonus tokens on the Technology board (one on each tech faction)
- **8 tokens in the supply/deck**

---

## The 16 Bonus Tokens (Complete List)

There are **8 different types** of bonus tokens with varying quantities:

### Type 1: Gain 3 Credits
- **Quantity:** 2 tokens
- **Effect:** Gain 3 Credits

### Type 2: Gain 4 Credits
- **Quantity:** 2 tokens
- **Effect:** Gain 4 Credits

### Type 3: Gain 1 Influence (Choice)
- **Quantity:** 4 tokens ⭐ (Most common)
- **Effect:** Gain 1 influence on a planet of your choice

### Type 4: Take the Leader Badge
- **Quantity:** 2 tokens
- **Effect:** Take the Leader badge

### Type 5: Gain 1 Zenithium
- **Quantity:** 3 tokens
- **Effect:** Gain 1 Zenithium

### Type 6: Mobilize 2 Cards
- **Quantity:** 1 token (Rare)
- **Effect:** Mobilize 2 cards

### Type 7: Exile 2 Cards
- **Quantity:** 1 token (Rare)
- **Effect:** Exile 2 cards

### Type 8: Transfer 1 Card
- **Quantity:** 1 token (Rare)
- **Effect:** Transfer 1 card

---

## Summary by Category

### Resource Bonuses (10 tokens total):
- **Credits:** 4 tokens (2× "3 Credits" + 2× "4 Credits")
- **Zenithium:** 3 tokens (all "1 Zenithium")

### Influence Bonuses (4 tokens total):
- **Influence:** 4 tokens (all "1 influence on planet of choice")

### Special Actions (2 tokens total):
- **Leadership:** 2 tokens (all "Take the Leader badge")

### Card Manipulation (3 tokens total):
- **Mobilize:** 1 token ("Mobilize 2 cards")
- **Exile:** 1 token ("Exile 2 cards")
- **Transfer:** 1 token ("Transfer 1 card")

---

## Token Distribution Statistics

**Total:** 2 + 2 + 4 + 2 + 3 + 1 + 1 + 1 = **16 tokens**

**Most Common:** Type 3 (Influence) with 4 tokens
**Rarest:** Types 6, 7, 8 (Card manipulation) with 1 token each

---

## Game Mechanics

1. **During Setup:** 8 tokens are randomly placed face-up (5 on planets, 3 on tech board)
2. **Supply:** Remaining 8 tokens stay in the supply deck (face-down)
3. **When Gained:** Effect is applied immediately, then token is discarded
4. **Reshuffle:** When supply is empty and a token needs to be drawn, discarded tokens are reshuffled into the supply
5. **Acquisition Methods:**
   - Gain a planet's influence disc → get that planet's bonus token
   - First to reach Level 2 on any tech track → draw bonus token from supply
   - Various card effects award bonus tokens

---

## Data Structure (from game code)

```json
"bonus_ref": {
  "1": {"num": 1, "nb": 2, "rule": "4,3", "desc": "Gain 3 Credits"},
  "2": {"num": 2, "nb": 2, "rule": "4,4", "desc": "Gain 4 Credits"},
  "3": {"num": 3, "nb": 4, "rule": "1,-7,1,1", "desc": "Gain 1 influence on a planet of your choice"},
  "4": {"num": 4, "nb": 2, "rule": "8,1", "desc": "Take the Leader badge"},
  "5": {"num": 5, "nb": 3, "rule": "3,1", "desc": "Gain 1 Zenithium"},
  "6": {"num": 6, "nb": 1, "rule": "51_17,2,1", "desc": "Mobilize 2 cards"},
  "7": {"num": 7, "nb": 1, "rule": "6,-1,1,1_6,-1,1,1", "desc": "Exile 2 cards"},
  "8": {"num": 8, "nb": 1, "rule": "14,1", "desc": "Transfer 1 card"}
}
```

**Field Explanation:**
- `num`: Token type number
- `nb`: Number of tokens of this type (quantity in the game)
- `rule`: Internal game rule code
- `desc`: Human-readable description of the effect
