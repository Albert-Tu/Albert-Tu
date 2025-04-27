# 🌌 Neon Drift: Skybound Protocol

> *A high-speed hover racing game set in the clouds of a fractured Earth. Race rogue AI, explore neon skylines, and rewrite your destiny—one drift at a time.*

![Banner](./Assets/_Project/Art/UI/banner.png)

---

## 🚀 Overview

**Neon Drift: Skybound Protocol** is a futuristic racing and exploration game built with **Unity HDRP**, blending high-speed competitive hover racing with narrative-rich open-world discovery.  
Experience reactive weather, cloud-based leaderboards, and stunning neon-lit skylines powered by real-world data and dynamic APIs.

---

## ✨ Features

- 🏎️ **Hover Racing Mechanics** — Responsive, skill-based controls with drift boosts, aerial flips, and gravity modulation.
- 🌍 **Live World Events** — Real-time weather synced to actual cities via OpenWeatherMap API.
- 📡 **Firebase Cloud Integration** — Player stats, ghost racers, leaderboards, and save syncing.
- 🔊 **Dynamic Audio** — Reactive music system and layered sound design via FMOD.
- 🧠 **Adaptive AI** — AI opponents learn player behavior and shift racing strategy dynamically.
- 🎮 **Full Controller Support** — Input remapping, vibration feedback, and UI navigation.
- 🔓 **Open-World Exploration** — Between races, freely explore floating cities, hack terminals, and uncover the Skybound conspiracy.

---

## 🧩 Game Details

- **Engine:** Unity (2022.3+ HDRP)
- **Genre:** Racing | Open-World | Sci-Fi
- **Modes:** Single Player | Time Trials | Free Roam
- **Target Platforms:** PC, macOS *(optional: Steam Deck & Linux)*

---

## 🖼️ Screenshots

| Race Mode | Free Roam | UI |
|:---------:|:---------:|:--:|
| ![Race](./Assets/_Project/Screenshots/race1.png) | ![Explore](./Assets/_Project/Screenshots/explore1.png) | ![UI](./Assets/_Project/Screenshots/ui1.png) |

---

## 🛠️ Project Structure

```plaintext
Assets/
├── _Project/
│   ├── Art/
│   ├── Audio/
│   ├── Code/
│   │   ├── Core/
│   │   ├── Racing/
│   │   ├── API/
│   │   ├── AI/
│   │   ├── UI/
│   ├── Data/
│   ├── Prefabs/
│   ├── Scenes/
│   ├── Shaders/
```

---

## 🔧 Setup & Installation

### Requirements

- **Unity Editor**: 2022.3 LTS or newer (HDRP template)
- **Hardware**: Minimum 8GB RAM, GTX 1060 GPU
- **Compatibility**: .NET Standard 2.1

### Installation

```bash
git clone https://github.com/yourusername/NeonDriftSkybound.git
cd NeonDriftSkybound
```

- Open the folder in **Unity Hub**.
- Ensure **HDRP** is installed and set up.
- Open and play the `MainMenu` scene.

---

## 🌐 API Integration

| API             | Purpose                            |
|-----------------|------------------------------------|
| OpenWeatherMap  | Real-time weather & effects        |
| Firebase        | Leaderboards, stats, saves         |
| Steamworks      | Achievements, multiplayer support  |

### Environment Setup

Create a `.env` file in the project root:

```bash
# .env
OPENWEATHERMAP_KEY=your_key_here
FIREBASE_DB_URL=https://your-game.firebaseio.com/
STEAM_APP_ID=000000
```

---

## 🎮 Controls

| Action          | Keyboard             | Controller       |
|-----------------|-----------------------|------------------|
| Accelerate      | `W`                   | `RT (Trigger)`   |
| Brake / Drift   | `S` / `Left Shift`     | `LT` / `B`        |
| Turn            | `A` / `D`              | `Left Stick`      |
| Free Roam Mode  | `Tab`                  | `Select`          |
| Pause / Menu    | `Esc`                  | `Start`           |

---

## 🧱 Build & Deployment

From **Unity Editor**:

1. Go to `File > Build Settings`
2. Select the target platform (e.g., Windows)
3. Click **Build**
4. Output will appear in the `/Builds/` directory
---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for full details.

---

> *“In a city that floats above the clouds, truth rides faster than light.”*
