# LILA BLACK: Product & Gameplay Insights

## 🚨 Insight 1: The "Deadly Entrance" (Level Design Flaw)
* **Observation:** A massive concentration of deaths (red clusters) consistently appears in the top-left sector of Ambrose Valley.
* **Evidence:** The **Global Death Heatmap** reveals a recurring "Kill Zone" at the road entrance across multiple dates (Feb 10-14).
* **Actionable Step:** Add defensive cover (rocks/trenching) or a secondary forest path to break this "Spawn Trap."
* **Affected Metrics:** **Early-Game Retention.** Preventing "instant deaths" keeps new players in the session longer.
* **Why a Level Designer cares:** This is a **Spatial Imbalance**. If one entry point has a 0% success rate, that portion of the map is "dead content" that players will eventually avoid entirely.

## 🗺️ Insight 2: The "Lobby Engagement Gap" (Monetization)
* **Observation:** 15-20% of all recorded telemetry events occur outside the playable minimap bounds.
* **Evidence:** The tool's **Off-Map Warning** identifies significant player activity in the top-left "Void," which represents the Pre-match Lobby.
* **Actionable Step:** Introduce **Lobby-specific monetization** (Emotes, temporary skins, or "Social Spaces") to fill the waiting time.
* **Affected Metrics:** **ARPU (Average Revenue Per User).** We are currently losing "attention time" that could be converted into engagement.
* **Why a Level Designer cares:** This is a **Flow Opportunity**. If players are spending 20% of their time here, the "Lobby" should be designed as a high-quality "Social Hub" rather than just an empty box in coordinate space.

## 🤖 Insight 3: Bot Predictability (Immersion)
* **Observation:** There is a stark visual difference in "Path Entropy" (randomness) between organic human paths and AI paths.
* **Evidence:** Using the **Playback Slider**, humans show "searching" behavior (circles, strafing), while bots move in highly linear waypoint-to-waypoint vectors.
* **Actionable Step:** Implement "Perlin Noise" or "Simulated Looting" stops into the AI Pathfinding logic. 
* **Affected Metrics:** **Player Immersion & Session Depth.** If players can't distinguish bots from humans, the "win" feels more rewarding.
* **Why a Level Designer cares:** This is about **NPC Believability**. Bots that walk through walls or move in perfect lines ruin the "Atmosphere" of the map that the designers worked hard to create.