# %% Libraries

import streamlit as st
import time

# %% Parameters for Streamlit

st.set_page_config(page_title="Pomodoro", page_icon="🍅", layout="wide")
st.title("🍅 Pomodoro")
st.sidebar.image("./images/logo.png")

# %% Functions
def apply_styles():
    st.markdown(
        """
        <style>
        .time {
            font-size: 100px !important;
            font-weight: 700 !important;
            color: #000000 !important;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def initialize_state():
    state = st.session_state
    if 'TS' not in state:
        state.TS = 0
    if 'STARTED' not in state:
        state.STARTED = False
    if 'STOPPED' not in state:
        state.STOPPED = True
    if 'PAUSED' not in state:
        state.PAUSED = False
    if 'COUNTDOWN' not in state:
        state.COUNTDOWN = '--:--'
    if 'INFO' not in state:
        state.INFO = None
    if 'POMODORO_COUNT' not in state:
        state.POMODORO_COUNT = 0
    if 'PHASE' not in state:
        state.PHASE = 'Pomodoro'  # Possible values: 'Pomodoro', 'Short Break', 'Long Break'
    if 'CYCLE_COUNT' not in state:
        state.CYCLE_COUNT = 0  # Count of Pomodoro cycles (sets of 4 Pomodoros)

def set_states(started=False, stopped=True, paused=False):
    state.STARTED = started
    state.STOPPED = stopped
    state.PAUSED = paused

def _stop_cb():
    state.TS = 0
    state.COUNTDOWN = '--:--'
    state.INFO = (st.error, 'Stopped')
    set_states(started=False, stopped=True, paused=False)
    state.PHASE = 'Pomodoro'

def _start_cb(ts, phase):
    if not state.PAUSED:
        state.TS = ts
    state.INFO = (st.info, f'Started {phase}')
    set_states(started=True, stopped=False, paused=False)
    state.PHASE = phase

def _pause_cb():
    state.INFO = (st.warning, 'Paused')
    set_states(started=False, stopped=False, paused=True)

def display_countdown(countdown, st_deltagen=None):
    if not st_deltagen:
        st_deltagen = st.empty()
    return st_deltagen.markdown(
        f"""<p class="time">{countdown}</p>""",
        unsafe_allow_html=True
    )

def count_down():
    while True:
        mins, secs = divmod(state.TS, 60)
        state.COUNTDOWN = '{:02d}:{:02d}'.format(mins, secs)
        display_countdown(state.COUNTDOWN, countdown_widget)
        time.sleep(1)
        state.TS -= 1
        if state.TS < 0 or state.STOPPED:
            break
    if state.STARTED:
        set_states(started=False, stopped=True, paused=False)
        if state.PHASE == 'Pomodoro':
            state.CYCLE_COUNT += 1
            if state.CYCLE_COUNT % 4 == 0:
                state.POMODORO_COUNT += 1
        next_phase = get_next_phase(state.PHASE)
        state.INFO = (st.success, f'Time Up! Starting {next_phase}')
        _start_cb(get_phase_duration(next_phase), next_phase)
        st.experimental_rerun()

def get_next_phase(current_phase):
    if current_phase == 'Pomodoro':
        return 'Short Break' if state.CYCLE_COUNT % 4 != 0 else 'Long Break'
    return 'Pomodoro'

def get_phase_duration(phase):
    if phase == 'Pomodoro':
        return state.POMODORO_TIME
    elif phase == 'Short Break':
        return state.SHORT_BREAK
    elif phase == 'Long Break':
        return state.LONG_BREAK

def main():
    apply_styles()
    initialize_state()
    global state
    state = st.session_state
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pomodoro Configuration")
        state.POMODORO_TIME = int(st.number_input('Enter Pomodoro time in minutes', min_value=0.1, value=25.0) * 60)
        state.SHORT_BREAK = int(st.number_input('Enter short break time in minutes', min_value=0.1, value=5.0) * 60)
        state.LONG_BREAK = int(st.number_input('Enter long break time in minutes', min_value=0.1, value=10.0) * 60)

        info = state.INFO[0](f'# {state.PHASE} {state.INFO[1]}') if state.INFO != None else st.subheader('Pomodoro')
        global countdown_widget
        countdown_widget = display_countdown(state.COUNTDOWN)
    
        button_col1, button_col2, button_col3 = st.columns(3)
        with button_col1:
            if st.button('Start', type='primary', on_click=_start_cb, args=(state.POMODORO_TIME, 'Pomodoro'), disabled=state.STARTED, use_container_width=True):
                st.rerun()
        with button_col2:
            if st.button('Stop', on_click=_stop_cb, disabled=state.STOPPED, use_container_width=True):
                state.INFO = None
                st.rerun()
        with button_col3:
            if st.button('Pause', on_click=_pause_cb, disabled=state.PAUSED or state.STOPPED, use_container_width=True):
                st.rerun()
        
        if state.STARTED and not state.PAUSED:
            count_down()
    
    with col2:
        st.subheader("Completed Pomodoros")
        st.write(f"Total Pomodoros: {state.POMODORO_COUNT}")

# %% Main
if __name__ == '__main__':
    main()
