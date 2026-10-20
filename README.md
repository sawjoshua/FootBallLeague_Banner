# Touchline Football Overlay

A lightweight football broadcast graphics controller and OBS-ready overlay for live match visuals. This project includes a browser-based control panel for managing scores, timers, player lower thirds, event banners, and a clean 16:9 overlay layout designed to be added to OBS as a browser source.

## Included files

- `touchline_football_overlay_v3.html` — main control panel and live preview UI
- `touchline_football_overlay_v3.css` — styling for the overlay and operator dashboard
- `touchline_server.py` — local Python HTTP server that serves the app and exposes the overlay on a local port

## Features

- Team names, short names, and score controls
- Home/away logo upload support
- Shirt color selection for each side
- Match clock with start, pause, and reset controls
- Half-time and full-time state management
- Player lower-third generator for event graphics
- Goal, yellow card, red card, substitution, walkout, lineup, and other match event banners
- OBS-friendly overlay mode with transparent or chroma-key background options
- Shared state sync between the control page and the overlay so both stay in sync

## Quick start

1. Open a terminal in the project folder.
2. Run:

```bash
python3 touchline_server.py
```

3. Open the controller in your browser:

```text
http://localhost:8080/
```

4. For the overlay view, open:

```text
http://localhost:8080/?overlay=1&bg=transparent
```

## OBS setup

Add a Browser Source in OBS and set the URL to:

```text
http://localhost:8080/?overlay=1&bg=transparent
```

Recommended settings:

- Width: `1920`
- Height: `1080`
- Custom CSS: leave blank unless you want extra styling overrides
- In OBS, keep the source visible and do not enable the "Shutdown source when not visible" option if you want the overlay to remain active during streaming

You can also use a green or blue chroma background by changing the URL parameter:

```text
http://localhost:8080/?overlay=1&bg=green
```

or

```text
http://localhost:8080/?overlay=1&bg=blue
```

## Notes

- The server binds to `127.0.0.1:8080` on your local machine.
- This is designed for local use and broadcasting workflow, not a production web app.
- The timer runs in the browser while the page is open; it is intended as a live graphics clock, not a wall-clock countdown.

## License

This project is provided as-is for personal or broadcast use. Add your own license if you want to distribute it more formally.
