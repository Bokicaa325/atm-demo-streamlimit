import streamlit as st

st.title("🏧 ATM Demo Aplikacija")

# ---- PODACI O KORISNICIMA ----
users = {
    "1234": {"name": "Marko", "balance": 2500},
    "4321": {"name": "Ana", "balance": 5000},
    "9999": {"name": "Ivan", "balance": 800},
}

WITHDRAW_LIMIT = 1000  # CHF
MAX_ATTEMPTS = 3

# ---- SESSION STATE ----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ---- LOGIN ----
if not st.session_state.logged_in:
    st.subheader("Prijava")

    pin_input = st.text_input("Unesite PIN", type="password")

    if st.button("Prijava"):
        if pin_input in users:
            st.session_state.logged_in = True
            st.session_state.current_user = pin_input
            st.session_state.attempts = 0
            st.success(f"Dobrodošao/la, {users[pin_input]['name']} 👋")
        else:
            st.session_state.attempts += 1
            remaining = MAX_ATTEMPTS - st.session_state.attempts
            st.error(f"Pogrešan PIN! Preostalo pokušaja: {remaining}")

            if st.session_state.attempts >= MAX_ATTEMPTS:
                st.error("Kartica je blokirana ❌")
                st.stop()

# ---- ATM MENI ----
else:
    user = users[st.session_state.current_user]

    st.subheader("ATM Meni")
    st.write(f"👤 Korisnik: **{user['name']}**")
    st.write(f"💰 Stanje: **{user['balance']} CHF**")
    st.write(f"⬆ Maksimalna isplata po transakciji: **{WITHDRAW_LIMIT} CHF**")

    amount = st.number_input("Unesite iznos (CHF)", min_value=0)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Uplata"):
            user["balance"] += amount
            st.success(f"Uplaćeno {amount} CHF")

    with col2:
        if st.button("Isplata"):
            if amount > WITHDRAW_LIMIT:
                st.error("Prekoračen maksimalni limit za isplatu")
            elif amount > user["balance"]:
                st.error("Nedovoljno sredstava")
            else:
                user["balance"] -= amount
                st.success(f"Podignuto {amount} CHF")

    if st.button("Odjava"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
