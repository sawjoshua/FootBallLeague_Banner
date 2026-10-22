# Touchline Studio v4

1. Run `python3 touchline_server.py` and leave it open.
2. Controller: http://localhost:8080/
3. OBS Browser Source (1920 × 1080): http://localhost:8080/?overlay=1  (use **Copy OBS link** for chroma options)

Optional: put a font file at `fonts/overlay.woff2` and the overlay and controller will use it. Without it they fall back to Inter if installed, then Segoe UI or Arial.

Match state is saved to `state.json`, and logos to `logo_home.png` and `logo_away.png`, so a server restart keeps the match.

To show the starting lineup graphic, enter each team's formation and players in the controller, then select **Starting lineups** under Graphics. Add one player per line; use `shirt number | player name` (for example, `9 | Alex Morgan`). Shirt numbers are optional.
