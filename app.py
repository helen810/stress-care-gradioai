import gradio as gr
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

# Global history list for tracking assessments
assessment_history = []

quotes_pool = [
    "“The soul always knows what to do to heal itself. The challenge is to silence the mind.” — Caroline Myss",
    "“Surrender to what is. Let go of what was. Have faith in what will be.” — Sonia Ricotti",
    "“Your calm mind is the ultimate weapon against your challenges.” — Bryant McGill",
    "“Smile, breathe, and go slowly.” — Thich Nhat Hanh",
    "“In the middle of difficulty lies opportunity.” — Albert Einstein"
]

songs_data = {
    "High Stress": [
        "🎵 [Kun Faya Kun (Hindi) - Rockstar](https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp)",
        "🎵 [Pookkalae Sattru Oyivedungal (Tamil) - I](https://open.spotify.com/track/0X2X8z2wYV6PzL1N9K7x9C)",
        "🎵 [Weightless (English) - Marconi Union](https://open.spotify.com/track/21GzyENGSluDPGqD0qBjiK)"
    ],
    "Moderate Stress": [
        "🎵 [Safarnama (Hindi) - Tamasha](https://open.spotify.com/track/5QnU69o1W1Gg2QJ3)",
        "🎵 [Maruvaarthai (Tamil) - Enai Noki Paayum Thota](https://open.spotify.com/track/4P83gG1K9zX1t0J)",
        "🎵 [Vienna (English) - Billy Joel](https://open.spotify.com/track/285pFiAkaKXwd1z8NM3ofE)"
    ],
    "Low Stress": [
        "🎵 [Enjoy Enjaami (Tamil) - Dhee ft. Arivu](https://open.spotify.com/track/3ee8J1GIAbGOUmKGlBD4t8)",
        "🎵 [Kar Har Maidaan Fateh (Hindi) - Sanju](https://open.spotify.com/track/5QnU69o1W1Gg2QJ3)",
        "🎵 [Unstoppable (English) - Sia](https://open.spotify.com/track/3ee8J1GIAbGOUmKGlBD4t8)"
    ]
}

def analyze_stress(workload, sleep, exercise, caffeine, mood):
    mood_weights = {
        "Happy / Content": 0, "Neutral": 2,
        "Exhausted / Low Energy": 5, "Anxious / Overwhelmed": 7,
        "Stressed / Irritated": 8
    }
    mood_score = mood_weights.get(mood, 2)
    
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

    # Save to history log
    assessment_history.append({
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Sleep Hours": sleep,
        "Workload Hours": workload,
        "Mood": mood,
        "Stress Level": stress_level,
        "Stress Score (%)": stress_pct
    })

    df = pd.DataFrame(assessment_history)
    fig = px.line(
        df, x="Timestamp", y="Stress Score (%)", markers=True,
        color="Stress Level", title="Session Stress Score Trend",
        color_discrete_map={"High": "#FF5252", "Moderate": "#FFD700", "Low": "#00E676"}
    ) if not df.empty else None

    result_md = f"### {color_code} Predicted Stress Level: **{stress_level} ({stress_pct}%)**"
    recommendations_md = f"#### 💡 AI Recommendations\n- **Recommended Sleep:** {rec_sleep}\n- **Routine Advice:** {routine}"
    quote_md = f"🌟 **Quote:** {random.choice(quotes_pool)}"

    return result_md, recommendations_md, quote_md, df, fig

def get_music_recommendations(category):
    tracks = songs_data.get(category, [])
    return "\n\n".join(tracks)

# Build Gradio Application Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌱 Stress Care Free AI")
    gr.Markdown("### Personal Stress Assessment & Wellness Engine")
    
    with gr.Tabs():
        with gr.TabItem("📋 Assessment & AI Engine"):
            with gr.Row():
                with gr.Column():
                    workload = gr.Slider(label="Workload Hours (per day)", minimum=1, maximum=16, value=8, step=1)
                    sleep = gr.Slider(label="Sleeping Hours (per day)", minimum=1, maximum=14, value=7, step=0.5)
                    exercise = gr.Slider(label="Physical Activity / Exercise (minutes per day)", minimum=0, maximum=120, value=30, step=5)
                    caffeine = gr.Slider(label="Caffeine Intake (cups)", minimum=0, maximum=10, value=2, step=1)
                    mood = gr.Dropdown(
                        label="How is your mood today?",
                        choices=["Happy / Content", "Neutral", "Anxious / Overwhelmed", "Exhausted / Low Energy", "Stressed / Irritated"],
                        value="Stressed / Irritated"
                    )
                    submit_btn = gr.Button("🔍 Predict Stress & Generate Recommendations", variant="primary")
                    
                with gr.Column():
                    out_status = gr.Markdown("### Results will appear here after analysis.")
                    out_recs = gr.Markdown()
                    out_quote = gr.Markdown()

        with gr.TabItem("🧘 Breathing Exercise"):
            gr.Markdown("### Guided Box Breathing")
            gr.Markdown("Box Breathing consists of four equal phases to activate calm:")
            gr.Markdown("1. **Inhale** slowly through your nose (4 seconds)\n2. **Hold** your breath (4 seconds)\n3. **Exhale** slowly through your mouth (4 seconds)\n4. **Hold** your breath (4 seconds)")

        with gr.TabItem("🎧 Music Therapy"):
            gr.Markdown("### Multilingual Music Therapy")
            music_category = gr.Dropdown(label="Select Vibe / Mood Category", choices=["High Stress", "Moderate Stress", "Low Stress"], value="Moderate Stress")
            music_output = gr.Markdown(value=get_music_recommendations("Moderate Stress"))
            music_category.change(fn=get_music_recommendations, inputs=music_category, outputs=music_output)

        with gr.TabItem("📊 Stress Log & Trends"):
            gr.Markdown("### Session Stress Log & Analytics")
            log_df = gr.DataFrame(value=pd.DataFrame(columns=["Timestamp", "Sleep Hours", "Workload Hours", "Mood", "Stress Level", "Stress Score (%)"]))
            log_plot = gr.Plot()

    submit_btn.click(
        fn=analyze_stress,
        inputs=[workload, sleep, exercise, caffeine, mood],
        outputs=[out_status, out_recs, out_quote, log_df, log_plot]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
