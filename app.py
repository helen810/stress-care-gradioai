import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime
import time
import streamlit.components.v1 as components

# --- PAGE SETUP & MOBILE CONFIG ---
st.set_page_config(page_title="Stress Care Free AI", page_icon="🌱", layout="centered")

# --- CUSTOM DARK STYLING ---
custom_css = """
<style>
.stApp { background-color: #0E1117; color: #E0E0E0; }
h1, h2, h3, h4 { color: #00E676 !important; font-family: 'Segoe UI', Roboto, sans-serif; }
div[data-testid="stMarkdownContainer"] > blockquote {
    background-color: #1E2640; border-left: 4px solid #00E676; padding: 12px; border-radius: 8px;
}
div.stButton > button {
    background: linear-gradient(135deg, #00E676 0%, #00B0FF 100%);
    color: #000000 !important; font-weight: bold; border-radius: 12px;
    padding: 12px 24px; border: none; box-shadow: 0px 4px 15px rgba(0, 230, 118, 0.3);
    width: 100%; transition: all 0.3s ease;
}
label { color: #A0AAB0 !important; font-size: 1rem !important; }
.card-box {
    background-color: #161B22; border: 1px solid #30363D; border-radius: 12px; padding: 16px; margin-bottom: 15px;
}
.accent-box {
    background-color: #1A2332; border-left: 4px solid #00B0FF; padding: 10px 14px; border-radius: 6px; margin-top: 8px;
}
.avoid-box {
    background-color: #2D1517; border-left: 4px solid #FF5252; padding: 10px 14px; border-radius: 6px; margin-top: 8px;
}
.timer-display {
    background-color: #161B22; border: 2px solid #00E676; border-radius: 16px;
    padding: 20px; text-align: center; margin: 15px 0;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "history_list" not in st.session_state:
    st.session_state.history_list = []

# --- DATABASES ---
quotes_pool = [
    "“The soul always knows what to do to heal itself. The challenge is to silence the mind.” — Caroline Myss",
    "“Surrender to what is. Let go of what was. Have faith in what will be.” — Sonia Ricotti",
    "“Your calm mind is the ultimate weapon against your challenges.” — Bryant McGill",
    "“Smile, breathe, and go slowly.” — Thich Nhat Hanh",
    "“In the middle of difficulty lies opportunity.” — Albert Einstein"
]

songs_data = {
    "High Stress": [
        {"title": "Kun Faya Kun (Hindi) - Rockstar", "spotify_id": "3n3Ppam7vgaVa1iaRUc9Lp"},
        {"title": "Pookkalae Sattru Oyivedungal (Tamil) - I", "spotify_id": "0X2X8z2wYV6PzL1N9K7x9C"},
        {"title": "Azhagiye (Tamil) - Kaatru Veliyidai", "spotify_id": "4V2Ku57gK3dK5YvL5sJ6v8"},
        {"title": "Butta Bomma (Telugu) - Ala Vaikunthapurramuloo", "spotify_id": "1Vv1wV2pZ9x8c7v6b5n4m3"},
        {"title": "Malare (Malayalam) - Premam", "spotify_id": "3Z8X9c7v6b5n4m3l2k1j0h"},
        {"title": "Weightless (English) - Marconi Union", "spotify_id": "21GzyENGSluDPGqD0qBjiK"}
    ],
    "Moderate Stress": [
        {"title": "Safarnama (Hindi) - Tamasha", "spotify_id": "5QnU69o1W1Gg2QJ3"},
        {"title": "Maruvaarthai (Tamil) - Enai Noki Paayum Thota", "spotify_id": "4P83gG1K9zX1t0J"},
        {"title": "Samajavaragamana (Telugu) - Ala Vaikunthapurramuloo", "spotify_id": "5v6b5n4m3l2k1j0h3Z8X9c"},
        {"title": "Aaromale (Malayalam) - Vinnaithaandi Varuvaayaa", "spotify_id": "1N9K7x9C0X2X8z2wYV6PzL"},
        {"title": "Vienna (English) - Billy Joel", "spotify_id": "285pFiAkaKXwd1z8NM3ofE"}
    ],
    "Low Stress": [
        {"title": "Enjoy Enjaami (Tamil) - Dhee ft. Arivu", "spotify_id": "3ee8J1GIAbGOUmKGlBD4t8"},
        {"title": "Oo Antava Mava (Telugu) - Pushpa", "spotify_id": "7lQWRAjy9FA0yR22fqNC96"},
        {"title": "Jimikki Kammal (Malayalam) - Velipadinte Pusthakam", "spotify_id": "6kA1VwT2p2p9y15LhKq59r"},
        {"title": "Kar Har Maidaan Fateh (Hindi) - Sanju", "spotify_id": "5QnU69o1W1Gg2QJ3"},
        {"title": "Unstoppable (English) - Sia", "spotify_id": "3ee8J1GIAbGOUmKGlBD4t8"}
    ]
}

# --- HEADER TITLE ---
st.title("🌱 Stress Care Free AI")
st.subheader("Personal Stress Assessment & Wellness Engine")
st.markdown("---")

# --- ORGANIZING INTO TABS ---
tab_assessment, tab_breathing, tab_music, tab_analytics = st.tabs([
    "📋 Assessment & AI Engine", 
    "🧘 Breathing Exercise", 
    "🎧 Music Therapy", 
    "📊 Stress Log & Trends"
])

with tab_assessment:
    st.header("Daily Input Tracker")
    workload = st.slider("Workload Hours (per day)", 1, 16, 8, key="workload_slider")
    sleep = st.slider("Sleeping Hours (per day)", 1, 14, 7, key="sleep_slider")
    exercise = st.slider("Physical Activity / Exercise (minutes per day)", 0, 120, 30, step=5, key="exercise_slider")
    caffeine = st.slider("Caffeine Intake (cups)", 0, 10, 2, key="caffeine_slider")

    mood = st.selectbox(
        "How is your mood today?",
        ["Happy / Content", "Neutral", "Anxious / Overwhelmed", "Exhausted / Low Energy", "Stressed / Irritated"],
        key="mood_select"
    )

    if st.button("🔍 Predict Stress & Generate Recommendations"):
        mood_weights = {
            "Happy / Content": 0, "Neutral": 2,
            "Exhausted / Low Energy": 5, "Anxious / Overwhelmed": 7,
            "Stressed / Irritated": 8
        }
        mood_score = mood_weights[mood]
        
        workload_penalty = max(0, workload - 6) * 1.5
        sleep_deficit = max(0, 8 - sleep) * 2.0
        caffeine_penalty = max(0, caffeine - 2) * 1.0
        exercise_credit = min(exercise, 60) * 0.05
        
        raw_stress = (workload_penalty + sleep_deficit + mood_score + caffeine_penalty) - exercise_credit
        raw_stress = max(0, min(raw_stress, 20))
        stress_pct = round((raw_stress / 20) * 100, 1)
        
        if stress_pct >= 65:
            stress_level = "High"
            color_code = "🚨"
            rec_sleep = "8 to 9 Hours"
            routine = "Take an immediate 20-minute quiet break. Stop screen time after 8 PM."
        elif stress_pct >= 35:
            stress_level = "Moderate"
            color_code = "⚠️"
            rec_sleep = "7.5 to 8 Hours"
            routine = "Take 5-minute movement breaks every 90 minutes. Organize tasks using priority lists."
        else:
            stress_level = "Low"
            color_code = "✨"
            rec_sleep = "7 to 8 Hours"
            routine = "Maintain your current positive routine! Add outdoor active time or pursue a hobby."

        # Save to session state
        st.session_state.history_list.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Sleep Hours": sleep, "Workload Hours": workload,
            "Mood": mood, "Stress Level": stress_level, "Stress Score (%)": stress_pct
        })

        st.header(f"{color_code} Predicted Stress Level: {stress_level} ({stress_pct}%)")
        st.progress(int(stress_pct))
        
        st.markdown(f"""
        <div class="card-box">
            <h4>💡 AI Recommendations</h4>
            <p><strong>Recommended Sleep:</strong> {rec_sleep}</p>
            <p><strong>Routine Advice:</strong> {routine}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(f"🌟 **Quote:** {random.choice(quotes_pool)}")

with tab_breathing:
    st.header("🧘 Guided Box Breathing Timer")
    st.write("Box Breathing (4s Inhale ➔ 4s Hold ➔ 4s Exhale ➔ 4s Hold) activates calm.")
    
    timer_seconds = st.selectbox("Select Session Duration:", [60, 180, 300], format_func=lambda x: f"{x//60} Minute(s)")

    if st.button("▶️ Start Breathing Session"):
        timer_placeholder = st.empty()
        progress_bar = st.progress(0)
        box_phases = [
            ("🫁 Inhale slowly through your nose...", 4),
            ("⏸️ Hold your breath...", 4),
            ("💨 Exhale slowly through your mouth...", 4),
            ("⏸️ Hold your breath...", 4)
        ]
        
        start_time = time.time()
        elapsed = 0
        phase_idx = 0
        
        while elapsed < timer_seconds:
            current_phase, phase_duration = box_phases[phase_idx % 4]
            for p in range(phase_duration):
                if elapsed >= timer_seconds: break
                mins, secs = divmod(timer_seconds - int(elapsed), 60)
                time_str = f"{mins:02d}:{secs:02d}"
                
                timer_placeholder.markdown(f"""
                <div class="timer-display">
                    <h2 style="color: #00B0FF !important; margin: 0;">{current_phase}</h2>
                    <h1 style="font-size: 3rem; color: #00E676 !important; margin: 10px 0;">{time_str}</h1>
                    <p style="color: #A0AAB0; margin: 0;">Time Remaining</p>
                </div>
                """, unsafe_allow_html=True)
                
                progress_bar.progress(min(elapsed / timer_seconds, 1.0))
                time.sleep(1)
                elapsed = time.time() - start_time
            phase_idx += 1
            
        progress_bar.progress(1.0)
        timer_placeholder.success("🎉 Great job! Breathing session complete.")

with tab_music:
    st.header("🎧 Multilingual Music Therapy")
    st.write("Listen to calming tracks curated across Tamil, Telugu, Malayalam, Hindi, and English.")
    
    selected_category = st.selectbox("Select Vibe / Mood Category:", ["Moderate Stress", "High Stress", "Low Stress"])
    
    for song in songs_data[selected_category]:
        spotify_url = f"https://open.spotify.com/track/{song['spotify_id']}"
        st.markdown(f"👉 **[{song['title']}]({spotify_url})**")
        embed_code = f"""
        <iframe src="https://open.spotify.com/embed/track/{song['spotify_id']}?utm_source=generator&theme=0" 
                width="100%" height="80" frameborder="0" allowfullscreen="" 
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy">
        </iframe>
        """
        components.html(embed_code, height=90)

with tab_analytics:
    st.header("📊 Current Session Stress Log")
    if st.session_state.history_list:
        df_session = pd.DataFrame(st.session_state.history_list)
        fig_line = px.line(
            df_session, x="Timestamp", y="Stress Score (%)", markers=True,
            color="Stress Level", title="Session Stress Score Trend", template="plotly_dark",
            color_discrete_map={"High": "#FF5252", "Moderate": "#FFD700", "Low": "#00E676"}
        )
        fig_line.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#161B22")
        st.plotly_chart(fig_line, use_container_width=True)
        st.dataframe(df_session, use_container_width=True)
    else:
        st.info("No assessment history yet. Run a prediction in the **Assessment** tab to log data!")
