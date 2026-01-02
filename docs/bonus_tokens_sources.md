# Bonus Tokens - Source Information & Uncertainty

## Confirmed Information

### From PDF Rules (`resources/ZE_Rules_EN.pdf`):
- ✓ **16 total bonus tokens** exist in the game
- ✓ **8 tokens placed on board at setup** (5 on planet tracks + 3 on tech board)
- ✓ **8 tokens in supply**
- ✓ When gained, effects are applied immediately and then discarded
- ✓ First to reach Level 2 on any tech track gains a bonus token
- ✓ Bonus tokens are placed face-up during setup
- ✓ Discarded bonuses can be reshuffled when supply runs out

## Inferred Information (UNCERTAIN)

### From Language File (`resources/x.boardgamearena.net/data/themereleases/251222-1408/js/modules/nls/en/lang_zenith.js`):

The language file contains hundreds of text strings describing various game effects. I found many bonus-related effect strings including:
- "Develop a HUMAN Technology with a reduction of 1 Zenithium"
- "Gain 1 influence on each of the 5 planets"
- "Take 1 BONUS token from those in play"
- "The 2 players go up to 8 Credits"
- etc.

### ⚠️ IMPORTANT LIMITATION:

**I do NOT have a definitive data structure that maps "Bonus Token #1 = X, Bonus Token #2 = Y, etc."**

The 16 effects I listed in `bonus_tokens_info.md` are my educated guess based on:
- Their standalone nature (seemed like bonus rewards rather than card effects)
- Appropriate power level for bonus tokens
- Finding roughly 16 effects that fit this pattern

### What I Need to Find:

A data structure like:
```javascript
bonus_ref = {
  1: { desc: "Effect description", ... },
  2: { desc: "Effect description", ... },
  ...
  16: { desc: "Effect description", ... }
}
```

This would definitively tell us which 16 effects are the actual bonus tokens.

## Next Steps:

Need to search more thoroughly in:
- `resources/x.boardgamearena.net/data/themereleases/251222-1408/js/`
- The main zenith.js file
- Any game data/configuration files

Looking for:
- `bonus_ref` object definition
- Bonus token data structures
- Any arrays or objects with exactly 16 bonus entries
