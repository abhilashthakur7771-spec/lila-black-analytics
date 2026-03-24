# LILA BLACK: Architecture & System Design

## 🛠 Tech Stack & Rationale
* **Streamlit (Python):** Chosen for **Speed-to-Insight**. It allowed for a rapid move from raw telemetry to a functional UI, enabling immediate feedback loops for Level Designers.
* **Pandas & PyArrow:** Essential for handling **Parquet files** efficiently, allowing for fast column-based filtering without high memory overhead.
* **Pillow (PIL):** Used for low-latency image compositing. This allowed us to draw dynamic paths over static minimaps without degrading performance.

## 🔄 Data Flow: Parquet to Screen
1.  **Ingestion:** The app dynamically scans the `player_data` directory.
2.  **Processing:** Raw bytes in the `event` column are decoded to UTF-8. We then map the match timeline to a standardized "Step" index to ensure consistent playback.
3.  **Visualization:** Data is passed through our coordinate engine and rendered as a transparent `.png` overlay, which is then composited onto the base minimap image.

## 📐 The "Tricky Part": Coordinate Mapping
Mapping 3D world space to a 2D 1024x1024 image requires **Linear Normalization**. My approach was:
1.  **Origin Offset:** Subtract the `origin_x/z` to move the world (0,0) to the map's (0,0).
2.  **Scaling:** Divide by the map's `scale` to get a value between 0 and 1.
3.  **Pixel Projection:** Multiply by 1024 to find the exact pixel on the image.

**Formula:** $$px = \frac{x - origin\_x}{scale} \times 1024$$

## ⚖️ Major Trade-offs
| Decision | Trade-off | Rationale |
| :--- | :--- | :--- |
| **Sampling vs. Full Scan** | Analyzed first 100 matches for heatmap. | Prioritized **UI Latency**. A 2-second load time is better for a designer than 100% data exhaustiveness. |
| **Static vs. Dynamic Map** | Used fixed 1024px minimap images. | Simple, robust, and performs well on mobile/low-bandwidth devices. |
| **Step-based Playback** | Used event counts instead of wall-clock time. | Ensures the playback slider works even for matches with inconsistent telemetry heartbeat. |

## 🧠 Assumptions & Ambiguities
* **The "Void" Data:** I encountered significant coordinates outside the `-370 to +530` range. I assumed this was **Pre-match Lobby telemetry**. I handled this by creating a "User Warning" instead of filtering it out, providing designers transparency into "Dead Time" behavior.
* **Bot Identification:** I assumed that events with "BotKill" or perfectly linear pathing indicated AI. I handled this by creating separate visual logic to help differentiate them from high-entropy human paths.