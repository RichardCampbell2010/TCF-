import streamlit as st

# Mobilvänlig layout och titel
st.set_page_config(page_title="TCF Analyzer", layout="centered")

st.title("🧬 The Campbell Formula (TCF)")
st.subheader("Matchanalys – Nacka IBK (Vita)")

st.markdown("---")

# FLIKAR FÖR ENKEL MOBILNAVIGERING
tab1, tab2, tab3 = st.tabs(["📊 Lagstats", "🏃‍♂️ Positionsstats", "📋 Färdig Rapport"])

with tab1:
    st.header("Lagets KPI:er (Bänken)")
    nacka_goals = st.number_input("Faktiska Mål (Nacka)", min_value=0, value=2, step=1)
    nacka_skott = st.number_input("Skott på mål (Nacka)", min_value=0, value=22, step=1)
    slot_completions = st.slider("Lyckade Slot Completions", 0, 40, 14)
    hdc_chances = st.slider("Antal HDC (Slottet/Royal Pass)", 0, 30, 11)
    
    st.markdown("---")
    st.header("🔵 Motståndarna")
    opp_goals = st.number_input("Faktiska Mål (Motståndare)", min_value=0, value=1, step=1)
    opp_skott = st.number_input("Skott på mål (Motståndare)", min_value=0, value=19, step=1)
    opp_slot_completions = st.slider("Motståndarnas Slot Completions", 0, 40, 22)

with tab2:
    st.header("Positionsdata (Nacka Vita)")
    st.caption("Fördela matchens händelser på dina fem positioner:")
    
    positions = ["Centrar", "Vänsterforwards", "Högerforwards", "Vänsterbackar", "Högerbackar"]
    pos_data = {}
    
    for pos in positions:
        st.markdown(f"### {pos}")
        p_mål = st.number_input(f"Mål - {pos}", min_value=0, value=0, key=f"{pos}_m")
        p_skott = st.number_input(f"Skott på mål - {pos}", min_value=0, value=0, key=f"{pos}_s")
        p_pass = st.number_input(f"Slottspass (A) - {pos}", min_value=0, value=0, key=f"{pos}_p")
        
        # TCF-logik för positioner baserat på skott och passningshot
        p_xG = round((p_mål * 0.40) + (p_skott * 0.08), 2)
        p_xA = round(p_pass * 0.15, 2)
        p_xT = round((p_skott * 0.03) + (p_pass * 0.05), 2)
        
        pos_data[pos] = {"Mål": p_mål, "xG": p_xG, "Assist": p_pass, "xA": p_xA, "xT": p_xT}

with tab3:
    st.header("📋 TCF Matchrapport till laget")
    
    # Beräkna TCF-värden live för lagstats
    nacka_xG = round((hdc_chances * 0.20) + ((nacka_skott - hdc_chances) * 0.035), 2)
    nacka_xA = round(slot_completions * 0.13, 2)
    nacka_xT = round((nacka_skott * 0.05) + (slot_completions * 0.06), 2)

    opp_xG = round((opp_slot_completions * 0.10) + (opp_skott * 0.02), 2)
    opp_xA = round(opp_slot_completions * 0.09, 2)
    opp_xT = round((opp_skott * 0.04) + (opp_slot_completions * 0.10), 2)

    # 1. LAG MOT LAG
    st.markdown("### 📊 1. STATISTISK JÄMFÖRELSE")
    st.table({
        "Lag": ["Nacka IBK (Vit)", "Motståndarna"],
        "Mål": [nacka_goals, opp_goals],
        "Totalt xG": [nacka_xG, opp_xG],
        "Totalt xA": [nacka_xA, opp_xA],
        "Totalt xT": [nacka_xT, opp_xT],
        "Skott": [nacka_skott, opp_skott]
    })

    # 2. POSITIONER
    st.markdown("### 🏃‍♂️ 2. POSITIONSPRESTATIONER (NACKA)")
    st.table(pos_data)

    # 3. VINSTFORMELN
    st.markdown("### 📐 3. UTVÄRDERING MOT VINSTFORMELN")
    if nacka_xG >= 5.0:
        st.success(f"🔥 **TCF Mål uppnått!** Vi nådde {nacka_xG} xG (Mål: 5.0+).")
    else:
        st.warning(f"⚠️ **TCF Analys:** Vi landade på {nacka_xG} xG (Mål: 5.0+).")

    st.write(f"• **Slot Completions:** {slot_completions} st (Mål: 20+).")
    st.write(f"• **High-Danger Chances (HDC):** {hdc_chances} st (Mål: 15+).")

    # 4. COA CHENS SLUTSATS
    st.markdown("### 🔥 Coachens slutsats till laget")
    if nacka_goals > opp_goals:
        st.info('"Tjejer, idag visar vi vilket enormt krigarhjärta det finns i det här gänget! Vi stängde slottet, tog heroiskt slit för varandra och tog hem vinsten. Sjukt stolt över laginsatsen – vi är vita maskinen!"')
    else:
        st.error('"Huvudet högt tjejer. TCF-datan visar exakt vad vi behöver skruva på till nästa träningsvecka. Vi kommer tillbaka starkare!"')
      
