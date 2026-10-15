import textwrap
import streamlit as st
import matplotlib.pyplot as plt

from solver import bfs_solve
from graph_visualizer import draw_state_graph, draw_solution_path


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Water Lab | BFS Explorer",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# HTML RENDERING HELPER
# =========================================================
def render_html(content):
    """Render HTML content correctly in Streamlit."""
    st.html(textwrap.dedent(content).strip())


# =========================================================
# CUSTOM CSS
# =========================================================
render_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #081321;
    --panel: #112238;
    --cyan: #51e5f2;
    --purple: #b8a0ff;
    --muted: #9bb0c5;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 0%, #12344a 0%, transparent 36%),
        radial-gradient(ellipse at 95% 15%, #28204a 0%, transparent 30%),
        var(--bg);
    color: #edf7ff;
    font-family: 'Manrope', sans-serif;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    color: #f1f8ff !important;
    letter-spacing: -0.7px;
}

p, label {
    color: #d3e1ee;
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #142a40, #101c30);
    border: 1px solid #29445b;
    border-radius: 16px;
    padding: 20px;
}

div[data-testid="stMetricLabel"] {
    color: #9bb0c5;
}

div[data-testid="stMetricValue"] {
    color: #51e5f2;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 11px;
    min-height: 44px;
    font-weight: 700;
    border: 1px solid #3a657c;
    transition: all .2s ease;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #51dce9, #8a9dff);
    color: #081321;
    border: none;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #51e5f2;
    transform: translateY(-1px);
}

div[data-testid="stNumberInput"] input {
    background: #0d1a2b;
    color: white;
    border-radius: 10px;
}

div[data-testid="stExpander"] {
    border: 1px solid #29445b;
    border-radius: 14px;
    background: #0d1b2b;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #29445b;
}

.eyebrow {
    color: #51e5f2;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    letter-spacing: 3px;
}

.hero {
    padding: 32px 0 24px 0;
}

.hero-title {
    font-size: clamp(42px, 6vw, 76px);
    line-height: 1.03;
    font-weight: 800;
    letter-spacing: -3px;
    margin: 18px 0;
    color: #f1f8ff;
}

.gradient-text {
    background: linear-gradient(90deg, #51e5f2, #b8a0ff);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtle {
    color: #9bb0c5;
    line-height: 1.8;
}

.section-tag {
    color: #51e5f2;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.pill {
    display: inline-block;
    border: 1px solid #3b6078;
    border-radius: 30px;
    padding: 7px 12px;
    color: #b8d4e8;
    font-size: 11px;
    margin: 4px 4px 4px 0;
    letter-spacing: .5px;
}

.jug {
    position: relative;
    height: 210px;
    width: 130px;
    border: 3px solid #638da5;
    border-top: 0;
    border-radius: 8px 8px 27px 27px;
    overflow: hidden;
    background: #11263a;
    margin: 18px auto 10px auto;
    display: flex;
    align-items: center;
    justify-content: center;
}

.water {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(180deg, #48dce8cc, #2787e5dd);
    border-top: 2px solid #8ff7ff;
    transition: height .5s ease;
}

.jug-number {
    z-index: 2;
    color: white;
    font-size: 28px;
    font-weight: 800;
    text-shadow: 0 2px 10px #081321;
}

.jug-caption {
    text-align: center;
    color: #9bb0c5;
    font-size: 13px;
}

.jug-capacity {
    text-align: center;
    font-weight: 700;
    color: #eaf7ff;
    margin-top: 5px;
}

.step-card {
    border: 1px solid #31526b;
    background: linear-gradient(135deg, #132b40, #101d31);
    border-radius: 15px;
    padding: 20px;
    margin: 12px 0;
}

.step-number {
    color: #51e5f2;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    letter-spacing: 2px;
}

.step-state {
    font-size: 30px;
    font-weight: 800;
    margin: 8px 0;
    color: #f1f8ff;
}

.trace-card {
    border: 1px solid #29445b;
    background: #101f32;
    border-radius: 14px;
    padding: 18px 20px;
    margin: 10px 0;
}

.trace-card.goal {
    border-color: #e7c75c;
    background: linear-gradient(110deg, #282b35, #172337);
}

.trace-title {
    color: #eaf7ff;
    font-weight: 700;
    margin: 8px 0;
}

.trace-state {
    color: #51e5f2;
    font-family: 'DM Mono', monospace;
    font-size: 17px;
}

.footer {
    text-align: center;
    color: #718ca4;
    font-size: 12px;
    padding: 32px 0 10px 0;
}

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #51e5f2, #8a9dff);
}
</style>
""")


# =========================================================
# HELPER FUNCTIONS
# =========================================================
def render_jug(name, amount, capacity):
    percentage = min(100, amount / capacity * 100) if capacity else 0

    render_html(f"""
    <div>
        <div class="jug-caption">{name}</div>
        <div class="jug-capacity">{capacity} litre capacity</div>
        <div class="jug">
            <div class="water" style="height:{percentage:.2f}%"></div>
            <div class="jug-number">
                {amount}<span style="font-size:14px"> L</span>
            </div>
        </div>
        <div class="jug-caption">{percentage:.0f}% filled</div>
    </div>
    """)


def normalise_solver_result(result):
    """Extract the solution path and explored-state count."""

    explored = 0
    path = result

    if isinstance(result, dict):
        path = result.get("path", result.get("solution", []))
        explored = result.get(
            "states_explored",
            result.get("explored", result.get("visited_count", 0)),
        )

    elif isinstance(result, tuple):
        if len(result) >= 2 and isinstance(result[0], (list, tuple)):
            path = result[0]
            if isinstance(result[1], (int, float)):
                explored = int(result[1])

    if path is None:
        return [], explored

    path = list(path)

    if path and not (
        isinstance(path[0], dict)
        and "state" in path[0]
        and "operation" in path[0]
    ):
        raise ValueError(
            "Expected each path item to contain 'state' and 'operation'. "
            "Check the return format of bfs_solve() in solver.py."
        )

    return path, explored


def make_report(path, capacity_a, capacity_b, target, explored):
    lines = [
        "WATER LAB - WATER JUG SOLVER",
        "MFC Project P009",
        "=" * 44,
        f"Jug A capacity: {capacity_a} litres",
        f"Jug B capacity: {capacity_b} litres",
        f"Target: {target} litres",
        f"Minimum operations: {max(0, len(path) - 1)}",
        f"States explored: {explored}",
        "",
        "SOLUTION PATH",
    ]

    for step_number, item in enumerate(path):
        lines.append(
            f"Step {step_number}: {item['operation']} -> {item['state']}"
        )

    return "\n".join(lines)


def section_heading(number, label):
    render_html(
        f'<div class="section-tag">{number} / {label}</div>'
    )


# =========================================================
# HERO SECTION
# =========================================================
render_html("""
<div class="hero">
    <div class="eyebrow">
        MFC PROJECT P009 · GRAPH THEORY LAB
    </div>

    <div class="hero-title">
        Every drop<br>
        has a <span class="gradient-text">path.</span>
    </div>

    <p class="subtle">
        Explore the classic Water Jug Problem through graph search.
        Configure your jugs, discover the shortest solution, and watch
        Breadth-First Search turn possibilities into a path.
    </p>

    <span class="pill">BREADTH-FIRST SEARCH</span>
    <span class="pill">STATE-SPACE EXPLORER</span>
    <span class="pill">INTERACTIVE LAB</span>
</div>
""")

st.divider()


# =========================================================
# CONFIGURATION
# =========================================================
section_heading("01", "CONFIGURE YOUR EXPERIMENT")
st.subheader("Set up your jugs")

with st.form("water_lab_form"):
    col_a, col_b, col_target = st.columns(3)

    with col_a:
        capacity_a = st.number_input(
            "Jug A capacity (litres)",
            min_value=1,
            max_value=30,
            value=4,
            step=1,
        )

    with col_b:
        capacity_b = st.number_input(
            "Jug B capacity (litres)",
            min_value=1,
            max_value=30,
            value=3,
            step=1,
        )

    with col_target:
        target = st.number_input(
            "Target quantity (litres)",
            min_value=0,
            max_value=30,
            value=2,
            step=1,
        )

    submitted = st.form_submit_button(
        "Find the shortest path  →",
        type="primary",
        width="stretch",
    )


if submitted:
    st.session_state["water_lab_config"] = (
        int(capacity_a),
        int(capacity_b),
        int(target),
    )
    st.session_state.pop("water_lab_result", None)

    # Reset the slider for the new problem.
    st.session_state["water_lab_slider"] = 0


if "water_lab_config" not in st.session_state:
    st.session_state["water_lab_config"] = (4, 3, 2)

a, b, target_value = st.session_state["water_lab_config"]


# =========================================================
# BFS SOLUTION
# =========================================================
if "water_lab_result" not in st.session_state:
    st.session_state["water_lab_result"] = bfs_solve(a, b, target_value)

try:
    path, explored = normalise_solver_result(
        st.session_state["water_lab_result"]
    )
except (ValueError, TypeError, KeyError) as error:
    st.error(f"Could not interpret the BFS result: {error}")
    st.stop()


# =========================================================
# SOLUTION OVERVIEW
# =========================================================
if not path:
    st.warning(
        "No solution path was returned. Try another target or check "
        "the return format of bfs_solve() in solver.py."
    )
    st.stop()

states = [item["state"] for item in path]
total_steps = max(0, len(path) - 1)

st.divider()
section_heading("02", "SOLUTION OVERVIEW")
st.subheader("Your shortest path is ready.")

metric_a, metric_b, metric_c = st.columns(3)
metric_a.metric("Minimum operations", total_steps)
metric_b.metric("States in solution", len(path))
metric_c.metric("Target quantity", f"{target_value} L")

if explored:
    st.caption(f"BFS explored {explored} states while searching.")


# =========================================================
# INTERACTIVE WATER SIMULATION
# =========================================================
section_heading("03", "LIVE WATER SIMULATION")
st.subheader("Watch each state come to life")

# Use one session-state key for both buttons and slider.
if "water_lab_slider" not in st.session_state:
    st.session_state["water_lab_slider"] = 0

# Keep the selected step within the available solution range.
current_step = max(
    0,
    min(int(st.session_state["water_lab_slider"]), total_steps),
)


def go_to_previous_step():
    """Move one step backward before Streamlit reruns the app."""
    st.session_state["water_lab_slider"] = max(
        0,
        int(st.session_state["water_lab_slider"]) - 1,
    )


def go_to_next_step():
    """Move one step forward before Streamlit reruns the app."""
    st.session_state["water_lab_slider"] = min(
        total_steps,
        int(st.session_state["water_lab_slider"]) + 1,
    )


state_a, state_b = states[current_step]

left, middle, right = st.columns([1, 1.2, 1])

with left:
    render_jug("JUG A", state_a, a)

with middle:
    render_html(f"""
    <div class="step-card">
        <div class="step-number">
            STEP {current_step:02d} / {total_steps:02d}
        </div>
        <div class="step-state">({state_a}, {state_b})</div>
        <p class="subtle">Current state · (Jug A, Jug B)</p>
        <span class="pill">A: {state_a}/{a} L</span>
        <span class="pill">B: {state_b}/{b} L</span>
    </div>
    """)

    progress = current_step / total_steps if total_steps else 1.0
    st.progress(progress, text="Solution progress")

with right:
    render_jug("JUG B", state_b, b)

st.markdown(f"**Operation:** {path[current_step]['operation']}")

previous_col, slider_col, next_col = st.columns([1, 2, 1])

with previous_col:
    st.button(
        "← Previous",
        disabled=current_step == 0,
        width="stretch",
        on_click=go_to_previous_step,
    )

with slider_col:
    st.slider(
        "Explore solution step",
        min_value=0,
        max_value=total_steps,
        key="water_lab_slider",
    )

with next_col:
    st.button(
        "Next →",
        disabled=current_step >= total_steps,
        type="primary",
        width="stretch",
        on_click=go_to_next_step,
    )


# =========================================================
# GRAPH VISUALIZATIONS
# =========================================================
st.divider()
section_heading("04", "THE SEARCH SPACE")
st.subheader("Explore the graph")

st.caption(
    "Every node represents a reachable state. Directed edges represent "
    "valid water-jug operations. Highlighted nodes belong to the solution."
)

with st.expander("View the complete state-space graph", expanded=True):
    figure = draw_state_graph(a, b, target_value, path)
    st.pyplot(figure, width="stretch")
    plt.close(figure)

with st.expander("View the shortest solution-path graph", expanded=True):
    figure = draw_solution_path(path, a, b, target_value)
    st.pyplot(figure, width="stretch")
    plt.close(figure)


# =========================================================
# SOLUTION TRACE
# =========================================================
st.divider()
section_heading("05", "SOLUTION TRACE")
st.subheader("Every operation, accounted for")

st.caption(
    "Follow each state from the empty starting jugs to the target quantity."
)

for step_number, item in enumerate(path):
    sx, sy = item["state"]
    is_goal = sx == target_value or sy == target_value
    card_class = "trace-card goal" if is_goal else "trace-card"

    render_html(f"""
    <div class="{card_class}">
        <div class="step-number">STEP {step_number:02d}</div>
        <div class="trace-title">{item['operation']}</div>
        <div class="trace-state">({sx}, {sy})</div>
        <div class="subtle">
            Jug A: {sx} L &nbsp; · &nbsp; Jug B: {sy} L
        </div>
    </div>
    """)


# =========================================================
# DOWNLOADABLE REPORT
# =========================================================
st.download_button(
    label="Download solution report",
    data=make_report(path, a, b, target_value, explored),
    file_name="water_jug_solution.txt",
    mime="text/plain",
    width="stretch",
)


# =========================================================
# LEARNING ZONE
# =========================================================
st.divider()
section_heading("06", "UNDERSTAND THE ALGORITHM")
st.subheader("Behind every drop is a search strategy.")

with st.expander("How does Breadth-First Search work?"):
    st.markdown("""
    **Breadth-First Search (BFS)** explores the state space level by level.

    1. Start with `(0, 0)`.
    2. Generate valid states using fill, empty, and pour operations.
    3. Track visited states to prevent repeated exploration.
    4. Store parent information to reconstruct the solution path.
    5. Stop when a state contains the target quantity.

    Since each operation has equal cost, BFS finds a solution using
    the minimum number of operations.
    """)

with st.expander("What does a state such as (3, 0) mean?"):
    st.markdown("""
    A state is represented as **`(x, y)`**:

    - `x` is the quantity of water in Jug A.
    - `y` is the quantity of water in Jug B.

    For example, `(3, 0)` means Jug A contains 3 litres and Jug B is empty.

    Valid states must satisfy `0 ≤ x ≤ capacity A` and
    `0 ≤ y ≤ capacity B`.
    """)

with st.expander("The six permitted operations"):
    st.markdown("""
    - Fill Jug A completely.
    - Fill Jug B completely.
    - Empty Jug A.
    - Empty Jug B.
    - Pour water from Jug A into Jug B until A is empty or B is full.
    - Pour water from Jug B into Jug A until B is empty or A is full.
    """)

with st.expander("What makes this a graph theory problem?"):
    st.markdown("""
    - **Vertices:** reachable water-jug states.
    - **Directed edges:** valid operations between states.
    - **Initial vertex:** `(0, 0)`.
    - **Goal vertex:** a state where one jug contains the target.
    - **Path:** a sequence of operations from the start to a goal.
    - **Shortest path:** a path containing the fewest operations.
    """)

with st.expander("About this project"):
    st.markdown("""
    **MFC Project P009 — Water Jug Problem Solver**

    Built with Python, Streamlit, NetworkX, and Matplotlib.

    The project demonstrates state-space modelling, graph traversal,
    shortest-path reconstruction, and interactive algorithm visualization.
    """)


# =========================================================
# FOOTER
# =========================================================
render_html("""
<div class="footer">
    WATER LAB · MFC PROJECT P009 · POWERED BY BREADTH-FIRST SEARCH
</div>
""")
