"""
Abenteuer in der Wildnis - Streamlit GUI

Start:
    pip install -r requirements.txt
    streamlit run streamlit_app.py

Diese Datei nutzt die Spiellogik aus wildnis_core.py.
"""

from __future__ import annotations

import os
import base64
from datetime import datetime
from pathlib import Path
from typing import Callable

import streamlit as st

from wildnis_core import AbenteuerSpiel


# --------------------------------------------------
# Design-Konstanten
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"

APP_BG = "#07140f"
CARD_BG = "#101f19"
CARD_BG_2 = "#0b1a14"
BTN_BG = "#173622"
BTN_HOVER = "#245536"
BTN_ACTIVE = "#2d6b3f"
ACCENT = "#83e66f"
ACCENT_DARK = "#264d2c"
TEXT = "#f2f5ee"
MUTED = "#a7b5aa"
WARN = "#ff6767"
BLUE = "#4aa3ff"
GOLD = "#d7a83f"
PANEL_BORDER = "#2c4234"
LIGHT_CARD = "#f1eddc"
LIGHT_TEXT = "#111111"


# --------------------------------------------------
# Streamlit Setup
# --------------------------------------------------

st.set_page_config(
    page_title="Abenteuer in der Wildnis",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Damit die Bestenliste wie in der Desktop-Version im Projektordner liegt.
os.chdir(BASE_DIR)


st.markdown(
    f"""
    <style>
        .stApp {{
            background: {APP_BG};
            color: {TEXT};
        }}

        [data-testid="stHeader"] {{
            background: rgba(7, 20, 15, 0.88);
        }}

        .block-container {{
            padding-top: 4.2rem;
            padding-bottom: 2rem;
            max-width: 1680px;
        }}

        h1, h2, h3, p, label, span, div {{
            color: {TEXT};
        }}

        [data-testid="stVerticalBlockBorderWrapper"] {{
            background: {CARD_BG};
            border: 1px solid {PANEL_BORDER};
            border-radius: 18px;
            padding: 1rem 1rem 1.15rem 1rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.18);
        }}

        .title-row {{
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 8px;
        }}

        .app-title {{
            font-family: Georgia, serif;
            font-size: 34px;
            font-weight: 800;
            color: {TEXT};
            line-height: 1.1;
            margin: 0;
        }}

        .start-shell {{
            max-width: 720px;
            margin: 4.25rem auto 0 auto;
        }}

        .start-title-row {{
            display: flex;
            align-items: center;
            gap: 38px;
            margin-bottom: 0.75rem;
        }}

        .start-tree {{
            font-size: 76px;
            line-height: 1;
            flex: 0 0 auto;
        }}

        .start-app-title {{
            font-family: Georgia, serif;
            font-size: 58px;
            font-weight: 800;
            color: {TEXT};
            line-height: 1.02;
            margin: 0;
        }}

        .start-subtitle {{
            color: {MUTED};
            font-size: 16px;
            margin: 0 0 1rem 0;
        }}

        .menu-title {{
            font-family: "Segoe UI", sans-serif;
            font-size: 1.9rem;
            font-weight: 800;
            line-height: 1.15;
            margin: 0 0 0.75rem 0;
        }}

        .small-label {{
            color: {MUTED};
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: .04em;
        }}

        .round-badge {{
            width: 64px;
            height: 64px;
            border-radius: 999px;
            background: {CARD_BG};
            display: flex;
            align-items: center;
            justify-content: center;
            color: {ACCENT};
            font-size: 24px;
            font-weight: 800;
            border: 1px solid {PANEL_BORDER};
            margin: 0 auto;
        }}

        .status-line {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 6px 0;
            color: {TEXT};
            font-weight: 700;
        }}

        .log-box {{
            background: {CARD_BG_2};
            border: 1px solid #16291f;
            border-radius: 14px;
            padding: 16px;
            min-height: 490px;
            max-height: 590px;
            overflow-y: auto;
            white-space: pre-wrap;
            font-family: Consolas, Monaco, monospace;
            font-size: 15px;
            color: {TEXT};
        }}

        .log-time {{
            color: {MUTED};
            font-weight: 700;
        }}

        .warning {{
            color: {WARN};
            font-weight: 700;
        }}

        .good {{
            color: {ACCENT};
            font-weight: 700;
        }}

        .blue {{
            color: {BLUE};
            font-weight: 700;
        }}

        .leaderboard-card {{
            background: {LIGHT_CARD};
            border-radius: 16px;
            padding: 16px;
            margin-top: 1.1rem;
            margin-bottom: 1rem;
        }}

        .leaderboard-card * {{
            color: {LIGHT_TEXT} !important;
        }}

        .inventory-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 8px;
        }}

        .inventory-tile {{
            background: #14231b;
            border: 1px solid {PANEL_BORDER};
            border-radius: 12px;
            padding: 10px 6px;
            text-align: center;
            min-height: 92px;
        }}

        .tile-icon {{
            font-size: 26px;
            line-height: 1.2;
        }}

        .tile-amount {{
            font-weight: 800;
            font-size: 14px;
        }}

        .tile-name {{
            font-size: 12px;
            color: {TEXT};
        }}

        .hint-warning {{
            background: #351d22;
            border: 1px solid #71333d;
            border-radius: 16px;
            padding: 16px;
        }}

        .subtle-divider {{
            border: 0;
            border-top: 1px solid {PANEL_BORDER};
            margin: 0.6rem 0 0.2rem 0;
            opacity: 0.8;
        }}

        .banner img {{
            border-radius: 16px;
            border: 1px solid {PANEL_BORDER};
        }}

        .avatar-center {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            min-height: 104px;
        }}

        .avatar-center img {{
            display: block;
            margin: 0 auto;
        }}

        .avatar-fallback {{
            width: 96px;
            height: 96px;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0 auto;
            font-size: 52px;
        }}

        .stButton > button {{
            width: 100%;
            min-height: 46px;
            border-radius: 12px;
            border: 0;
            background: {BTN_BG};
            color: {TEXT};
            font-weight: 700;
            white-space: normal;
            line-height: 1.2;
            text-align: center;
            padding: 0.5rem 0.65rem;
        }}

        .stButton > button:hover {{
            background: {BTN_HOVER};
            color: {TEXT};
            border: 0;
        }}

        .stTextInput > div > div > input,
        .stNumberInput input {{
            background: {CARD_BG_2};
            color: {TEXT};
            border: 1px solid {ACCENT_DARK};
            border-radius: 12px;
        }}

        div[data-testid="stProgress"] > div > div > div > div {{
            background-color: {ACCENT};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Hilfsfunktionen
# --------------------------------------------------

def asset_path(filename: str) -> Path:
    return ASSET_DIR / filename


def render_centered_asset_image(filename: str, width: int = 96, fallback: str = "🧑") -> None:
    """Rendert Avatar-Bilder mittig in ihrer Spalte.

    st.image richtet kleine Bilder je nach Streamlit-Version linksbündig aus.
    Das HTML-Rendering sorgt dafür, dass die Figuren sauber mittig stehen.
    """
    path = asset_path(filename)
    if path.exists():
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        st.markdown(
            f"<div class='avatar-center'><img src='data:image/png;base64,{encoded}' width='{width}'></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f"<div class='avatar-fallback'>{fallback}</div>", unsafe_allow_html=True)


def shorten(text: str, max_len: int = 18) -> str:
    return text if len(text) <= max_len else text[: max_len - 1] + "…"


def material_amount(spiel: AbenteuerSpiel, name: str) -> int:
    item = spiel.spieler.inventar.suchen(name)
    return 0 if item is None else item.menge


def ensure_state() -> None:
    if "spiel" not in st.session_state:
        st.session_state.spiel = None
    if "spielername" not in st.session_state:
        st.session_state.spielername = "Lesley"
    if "menu_mode" not in st.session_state:
        st.session_state.menu_mode = "main"
    if "log_entries" not in st.session_state:
        st.session_state.log_entries = []
    if "start_error" not in st.session_state:
        st.session_state.start_error = ""


def add_log(text: str, clear: bool = False) -> None:
    if clear:
        st.session_state.log_entries = []
    if text:
        st.session_state.log_entries.append(
            {
                "time": datetime.now().strftime("%H:%M"),
                "text": text,
            }
        )


def clear_log() -> None:
    st.session_state.log_entries = []


def start_game(name: str) -> None:
    name = name.strip()
    if not name:
        st.session_state.start_error = "Bitte gib zuerst einen Spielernamen ein."
        return

    st.session_state.spielername = name
    st.session_state.spiel = AbenteuerSpiel(name)
    st.session_state.menu_mode = "main"
    st.session_state.start_error = ""
    add_log(st.session_state.spiel.intro_text(), clear=True)


def restart_game() -> None:
    st.session_state.spiel = AbenteuerSpiel(st.session_state.spielername)
    st.session_state.menu_mode = "main"
    add_log(st.session_state.spiel.intro_text(), clear=True)


def run_action(action_func: Callable[[], str]) -> None:
    spiel = st.session_state.spiel
    if spiel is None:
        return
    if spiel.beendet:
        add_log("Das Spiel ist bereits beendet. Starte ein neues Spiel.")
        return
    message = action_func()
    add_log(message)


def do_trade() -> None:
    spiel = st.session_state.spiel
    if spiel is None:
        return
    if spiel.beendet:
        add_log("Das Spiel ist bereits beendet. Starte ein neues Spiel.")
        return

    name_spieler = st.session_state.get("trade_player_item", "").strip()
    menge_spieler = str(st.session_state.get("trade_player_amount", "")).strip()
    name_tesla = st.session_state.get("trade_tesla_item", "").strip()
    menge_tesla = str(st.session_state.get("trade_tesla_amount", "")).strip()

    if not name_spieler or not menge_spieler or not name_tesla or not menge_tesla:
        add_log("WARNUNG: Bitte fülle alle Handelsfelder aus.")
        return

    message = spiel.handel_mit_tesla(name_spieler, menge_spieler, name_tesla, menge_tesla)
    add_log(message)


def log_html() -> str:
    if not st.session_state.log_entries:
        return "<span class='log-time'>Noch keine Ereignisse.</span>"

    parts: list[str] = []
    for entry in st.session_state.log_entries:
        parts.append(f"<span class='log-time'>[{entry['time']}]</span>")
        for raw_line in entry["text"].split("\n"):
            line = raw_line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            upper = line.upper()
            css_class = ""
            if any(word in upper for word in ["WARNUNG", "GAME OVER", "ERSCHÖPFT", "NICHT GENUG"]):
                css_class = "warning"
            elif any(word in upper for word in ["GEWONNEN", "GERETTET", "ERFOLGREICH"]):
                css_class = "good"
            elif "ENERGIE" in upper:
                css_class = "blue"

            if css_class:
                parts.append(f"<span class='{css_class}'>{line}</span>")
            else:
                parts.append(line)
        parts.append("")
    return "\n".join(parts)


# --------------------------------------------------
# Startscreen
# --------------------------------------------------

def render_start_screen() -> None:
    left, center, right = st.columns([0.8, 1.55, 0.8])
    with center:
        st.markdown(
            f"""
            <div class='start-shell'>
                <div class='start-title-row'>
                    <div class='start-tree'>🌲</div>
                    <div class='start-app-title'>Abenteuer in der Wildnis</div>
                </div>
                <p class='start-subtitle'>Überlebe, sammle Ressourcen, handle mit Tesla und baue dein Signalfeuer.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        name = st.text_input("Spielername", value=st.session_state.spielername, placeholder="z. B. Lesley")
        if st.session_state.get("start_error"):
            st.error(st.session_state.start_error)
        if st.button("Spiel starten ➜", type="primary", use_container_width=False):
            start_game(name)
            st.rerun()


# --------------------------------------------------
# Linkes Menü
# --------------------------------------------------

def set_menu(mode: str) -> None:
    st.session_state.menu_mode = mode


def render_left_menu() -> None:
    spiel = st.session_state.spiel
    mode = st.session_state.menu_mode

    title_by_mode = {
        "main": "Hauptmenü",
        "actions": "Aktionen / Überleben",
        "food": "Etwas essen",
        "trade": "Handel mit Tesla",
    }

    with st.container(border=True):
        st.markdown(f"<div class='menu-title'>{title_by_mode.get(mode, 'Hauptmenü')}</div>", unsafe_allow_html=True)

        if mode == "main":
            if st.button("🤝 Handel mit Tesla", use_container_width=True):
                set_menu("trade")
                st.rerun()
            if st.button("🛠️ Aktionen / Überleben", use_container_width=True):
                set_menu("actions")
                st.rerun()
            if st.button("🌙 Schlafen gehen", use_container_width=True):
                run_action(spiel.schlafen)
                st.rerun()
            if st.button("🎒 Status / Inventar", use_container_width=True):
                add_log(spiel.status_text() + "\n\n" + spiel.inventar_text())
                st.rerun()
            if st.button("🔥 Signalfeuer bauen", use_container_width=True):
                run_action(spiel.signalfeuer)
                st.rerun()
            if st.button("🏆 Bestenliste", use_container_width=True):
                add_log(spiel.bestenliste_text())
                st.rerun()
            if st.button("🚪 Spiel beenden", use_container_width=True):
                add_log(spiel.spiel_beenden())
                st.rerun()

        elif mode == "actions":
            actions = [
                ("1 🌲 Holz sammeln", spiel.holz_sammeln),
                ("2 ⛰️ Steine sammeln", spiel.steine_sammeln),
                ("3 🐟 Angeln gehen", spiel.angeln_gehen),
                ("4 🌊 Fluss überqueren", spiel.fluss_ueberqueren),
                ("5 🍓 Beeren sammeln", spiel.beeren_sammeln),
                ("6 🥜 Nüsse sammeln", spiel.nuesse_sammeln),
                ("7 🌿 Kräuter suchen", spiel.kraeuter_suchen),
            ]
            for label, func in actions:
                if st.button(label, use_container_width=True):
                    run_action(func)
                    st.rerun()
            if st.button("8 🍲 Etwas essen", use_container_width=True):
                set_menu("food")
                st.rerun()
            if st.button("← Zurück zum Hauptmenü", use_container_width=True):
                set_menu("main")
                st.rerun()

        elif mode == "food":
            for food, icon in [("Beeren", "🍓"), ("Fisch", "🐟"), ("Nüsse", "🥜"), ("Kräuter", "🌿")]:
                label = f"{icon} {food} essen" if food != "Kräuter" else "🌿 Kräuter nutzen"
                if st.button(label, use_container_width=True):
                    run_action(lambda f=food: spiel.essen(f))
                    st.rerun()
            if st.button("← Zurück zu Aktionen", use_container_width=True):
                set_menu("actions")
                st.rerun()

        elif mode == "trade":
            st.markdown(
                f"<p style='color:{MUTED};'>Tesla besitzt Harz, Feuerstein, Stoff, Nüsse und Kräuter.<br>Beispiel: Du gibst Holz / 20 und Tesla gibt Harz / 2.</p>",
                unsafe_allow_html=True,
            )
            st.text_input("Du gibst", value="Holz", key="trade_player_item")
            st.number_input("Menge", min_value=1, max_value=200, value=20, key="trade_player_amount")
            st.text_input("Tesla gibt", value="Harz", key="trade_tesla_item")
            st.number_input("Menge ", min_value=1, max_value=200, value=2, key="trade_tesla_amount")
            if st.button("✅ Handel ausführen", use_container_width=True):
                do_trade()
                st.rerun()
            if st.button("📦 Tesla-Inventar anzeigen", use_container_width=True):
                add_log(spiel.tesla.inventar_anzeigen())
                st.rerun()
            if st.button("← Zurück zum Hauptmenü", use_container_width=True):
                set_menu("main")
                st.rerun()

    render_leaderboard_preview()

    if spiel.beendet:
        if st.button("↻ Neues Spiel starten", use_container_width=True):
            restart_game()
            st.rerun()



def render_leaderboard_preview() -> None:
    spiel = st.session_state.spiel
    entries = [] if spiel is None else spiel.bestenliste.laden()
    entries = sorted(entries, key=lambda x: x.get("punkte", 0), reverse=True)[:3]

    st.markdown("<div class='leaderboard-card'><h3>🏆 Bestenliste</h3>", unsafe_allow_html=True)
    if not entries:
        st.markdown("<p>Noch keine Einträge.</p>", unsafe_allow_html=True)
    else:
        medals = ["🥇", "🥈", "🥉"]
        for index, entry in enumerate(entries):
            status = "Sieg" if entry.get("gewonnen") else "Beendet"
            st.markdown(
                f"<p><b>{medals[index]} Platz {index + 1}: {entry.get('name', '-')}</b><br>"
                f"{entry.get('punkte', 0)} Punkte · {entry.get('runden', 0)} Runden · {status}</p>",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)


# --------------------------------------------------
# Mitte
# --------------------------------------------------

def render_center() -> None:
    with st.container(border=True):
        top_left, top_right = st.columns([1, 0.28])
        with top_left:
            st.markdown("<h2 style='margin:0 0 0.3rem 0;'>📜 Ereignisse</h2>", unsafe_allow_html=True)
        with top_right:
            if st.button("🗑 Verlauf löschen", use_container_width=True):
                clear_log()
                st.rerun()

        banner = asset_path("forest_banner.png")
        if banner.exists():
            st.markdown("<div class='banner'>", unsafe_allow_html=True)
            st.image(str(banner), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("🌲 Nebliger Wald · Lagerfeuer · Überleben")

        st.markdown(f"<div class='log-box'>{log_html()}</div>", unsafe_allow_html=True)


# --------------------------------------------------
# Rechte Sidebar
# --------------------------------------------------

def render_progress(label: str, value: int, icon: str, color: str) -> None:
    st.markdown(
        f"<div class='status-line'><span style='font-size:24px;color:{color};'>{icon}</span><span>{label}</span><span style='margin-left:auto;'>{value} / 100</span></div>",
        unsafe_allow_html=True,
    )
    st.progress(value / 100)


def render_player_card() -> None:
    spiel = st.session_state.spiel
    hp = spiel.spieler.status.gesundheit
    en = spiel.spieler.status.energie

    with st.container(border=True):
        img_col, text_col = st.columns([0.32, 0.68])
        with img_col:
            render_centered_asset_image("player_avatar.png", width=96, fallback="🧑")
        with text_col:
            st.markdown(f"<div class='small-label'>Spieler</div><h2 style='margin:0;'>{spiel.spielername}</h2>", unsafe_allow_html=True)
        render_progress(" Gesundheit", hp, "♥", ACCENT)
        render_progress(" Energie", en, "⚡", BLUE)


def render_inventory_card() -> None:
    spiel = st.session_state.spiel
    total = spiel.spieler.inventar.gesamtmenge()
    limit = spiel.spieler.inventar.obergrenze

    with st.container(border=True):
        st.markdown(
            f"<div style='display:flex; align-items:center; justify-content:space-between; gap:12px;'>"
            f"<h3 style='margin:0;'>🎒 Inventar</h3>"
            f"<span style='background:#18281e;color:{ACCENT};border-radius:8px;padding:4px 10px;font-weight:800;white-space:nowrap;'>{total} / {limit}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        items = spiel.spieler.inventar.als_liste()[:4]
        icons = {
            "Holz": "🌲",
            "Stein": "⛰️",
            "Beeren": "🍓",
            "Fisch": "🐟",
            "Nüsse": "🥜",
            "Kräuter": "🌿",
            "Harz": "🟤",
            "Feuerstein": "⚫",
            "Stoff": "🧵",
        }
        while len(items) < 4:
            items.append(("Platz", "+"))

        html_tiles = ["<div class='inventory-grid'>"]
        for name, amount in items:
            if name == "Platz":
                icon = "+"
                amount_text = ""
            else:
                icon = icons.get(name, "📦")
                amount_text = str(amount)
            html_tiles.append(
                f"<div class='inventory-tile'><div class='tile-icon'>{icon}</div>"
                f"<div class='tile-amount'>{amount_text}</div>"
                f"<div class='tile-name'>{shorten(name, 9)}</div></div>"
            )
        html_tiles.append("</div>")
        st.markdown("".join(html_tiles), unsafe_allow_html=True)


def render_quick_food_card() -> None:
    spiel = st.session_state.spiel
    with st.container(border=True):
        st.markdown("<h3 style='margin-top:0;'>🌿 Schnellaktionen (Nahrung)</h3>", unsafe_allow_html=True)
        rows = [
            [("Beeren", "🍓"), ("Fisch", "🐟")],
            [("Nüsse", "🥜"), ("Kräuter", "🌿")],
        ]
        for pair in rows:
            cols = st.columns(2)
            for col, (food, icon) in zip(cols, pair):
                with col:
                    if st.button(f"{icon} {food}", use_container_width=True):
                        run_action(lambda f=food: spiel.essen(f))
                        st.rerun()


def render_tesla_card() -> None:
    with st.container(border=True):
        st.markdown("<h3 style='margin-top:0;'>Tesla – Handel mit seltenen Gütern</h3>", unsafe_allow_html=True)
        img_col, text_col = st.columns([0.32, 0.68])
        with img_col:
            render_centered_asset_image("tesla_avatar.png", width=96, fallback="🧙‍♀️")
        with text_col:
            st.markdown(
                f"<p style='color:{MUTED}; margin-top:0;'>Tesla hat wertvolle Waren.<br>Handle mit ihr, um seltene Materialien für dein Signalfeuer zu bekommen.</p>",
                unsafe_allow_html=True,
            )
        if st.button("Zu Tesla gehen »", use_container_width=True):
            set_menu("trade")
            st.rerun()


def render_hint_card() -> None:
    spiel = st.session_state.spiel
    warnung = spiel.spieler.warnung_pruefen()

    with st.container(border=True):
        if warnung:
            st.markdown(
                f"<div class='hint-warning'><h3 style='color:{ACCENT}; margin-top:0;'>💡 Hinweis</h3><p class='warning'>{warnung}</p></div>",
                unsafe_allow_html=True,
            )
            return

        needs = [("Holz", 100), ("Stein", 30), ("Fisch", 5), ("Harz", 3), ("Feuerstein", 1), ("Stoff", 2)]
        lines = ["Für das Signalfeuer brauchst du:"]
        for name, need in needs:
            have = material_amount(spiel, name)
            marker = "✓" if have >= need else "✕"
            missing = max(need - have, 0)
            if missing == 0:
                lines.append(f"{marker} {name}: {have}/{need}")
            else:
                lines.append(f"{marker} {name}: {have}/{need} | fehlt: {missing}")
        lines.append("")
        lines.append("Seltene Materialien bekommst du bei Tesla.")

        st.markdown(f"<h3 style='color:{ACCENT}; margin-top:0;'>💡 Hinweis</h3>", unsafe_allow_html=True)
        st.markdown(
            "<pre style='white-space:pre-wrap; font-family: Segoe UI, sans-serif; margin-bottom:0;'>" + "\n".join(lines) + "</pre>",
            unsafe_allow_html=True,
        )


def render_right_sidebar() -> None:
    render_player_card()
    render_inventory_card()
    render_quick_food_card()
    render_tesla_card()
    st.markdown("<hr class='subtle-divider'>", unsafe_allow_html=True)
    render_hint_card()


# --------------------------------------------------
# Game Screen
# --------------------------------------------------

def render_topbar() -> None:
    spiel = st.session_state.spiel
    hp = spiel.spieler.status.gesundheit
    en = spiel.spieler.status.energie

    title_col, round_col, status_col = st.columns([0.50, 0.14, 0.36], vertical_alignment="center")
    with title_col:
        st.markdown(
            "<div class='title-row'><span style='font-size:34px;'>🌲</span><span class='app-title'>Abenteuer in der Wildnis</span></div>",
            unsafe_allow_html=True,
        )
    with round_col:
        st.markdown("<div class='small-label' style='text-align:center;'>Runde</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='round-badge'>{spiel.runden}</div>", unsafe_allow_html=True)
    with status_col:
        render_progress("Gesundheit", hp, "♥", ACCENT)
        render_progress("Energie", en, "⚡", BLUE)


def render_game_screen() -> None:
    render_topbar()
    st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)
    left, center, right = st.columns([0.23, 0.49, 0.28], gap="large")
    with left:
        render_left_menu()
    with center:
        render_center()
    with right:
        render_right_sidebar()


# --------------------------------------------------
# App Start
# --------------------------------------------------

ensure_state()

if st.session_state.spiel is None:
    render_start_screen()
else:
    render_game_screen()
