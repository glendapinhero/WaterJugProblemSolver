
import streamlit as st
import matplotlib.pyplot as plt

from solver import bfs_solve
from graph_visualizer import (
    draw_state_graph,
    draw_solution_path
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Water Jug Problem Solver",
    page_icon="💧",
    layout="wide"
)


# --------------------------------------------------
# SIMULATION CONTROLS
# --------------------------------------------------

def previous_step():
    st.session_state["step_slider"] = max(
        0, st.session_state["step_slider"] - 1
    )


def next_step():
    st.session_state["step_slider"] = min(
        st.session_state["total_steps"],
        st.session_state["step_slider"] + 1
    )


def reset_step():
    st.session_state["step_slider"] = 0


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("💧 Water Jug Problem Solver")

st.caption(
    "MFC Project P009 | Graph Theory | "
    "Breadth-First Search (BFS)"
)

st.write(
    "Find the minimum number of operations required "
    "to measure a target quantity of water using two jugs."
)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.header("1. Enter Problem Details")

with st.form("water_jug_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        capacity_a = st.number_input(
            "Jug A capacity (litres)",
            min_value=1,
            max_value=100,
            value=4,
            step=1
        )

    with col2:
        capacity_b = st.number_input(
            "Jug B capacity (litres)",
            min_value=1,
            max_value=100,
            value=3,
            step=1
        )

    with col3:
        target = st.number_input(
            "Target quantity (litres)",
            min_value=0,
            max_value=100,
            value=2,
            step=1
        )

    solve_button = st.form_submit_button(
        "🔍 Solve Water Jug Problem",
        width="stretch"
    )


# --------------------------------------------------
# RUN BFS
# --------------------------------------------------

if solve_button:

    capacity_a = int(capacity_a)
    capacity_b = int(capacity_b)
    target = int(target)

    result = bfs_solve(
        capacity_a,
        capacity_b,
        target
    )

    st.session_state["result"] = result
    st.session_state["capacity_a"] = capacity_a
    st.session_state["capacity_b"] = capacity_b
    st.session_state["target"] = target

    st.session_state["step_slider"] = 0
    st.session_state["total_steps"] = (
        len(result["path"]) - 1 if result else 0
    )


# --------------------------------------------------
# DISPLAY SOLUTION
# --------------------------------------------------

if "result" in st.session_state:

    result = st.session_state["result"]
    capacity_a = st.session_state["capacity_a"]
    capacity_b = st.session_state["capacity_b"]
    target = st.session_state["target"]

    st.divider()
    st.header("2. Solution")

    if result is None:

        st.error(
            "No solution exists for these capacities "
            "and target under the standard water-jug rules."
        )

        st.info(
            "For positive integer capacities, a positive "
            "target must not exceed the larger jug's capacity "
            "and must be divisible by the greatest common "
            "divisor (GCD) of the capacities."
        )

    else:

        path = result["path"]
        total_steps = len(path) - 1

        st.success("A solution was found!")

        # ------------------------------------------
        # SUMMARY METRICS
        # ------------------------------------------

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(
            "Minimum operations",
            result["operations"]
        )

        metric2.metric(
            "States explored",
            result["states_explored"]
        )

        metric3.metric(
            "States in solution",
            len(path)
        )

        # ------------------------------------------
        # INTERACTIVE SIMULATION
        # ------------------------------------------

        st.divider()
        st.subheader("3. Interactive Jug Simulation")

        selected_step = st.slider(
            "Move through the solution",
            min_value=0,
            max_value=total_steps,
            key="step_slider"
        )

        current_item = path[selected_step]
        amount_a, amount_b = current_item["state"]

        st.caption(
            f"Step {selected_step} of {total_steps}"
        )

        st.info(
            f"Operation: **{current_item['operation']}**"
        )

        jug1, jug2 = st.columns(2)

        with jug1:

            st.subheader("🔵 Jug A")
            st.write(f"Capacity: {capacity_a} litres")

            st.metric(
                "Current water",
                f"{amount_a} L"
            )

            st.progress(
                amount_a / capacity_a,
                text=f"{amount_a} / {capacity_a} litres"
            )

        with jug2:

            st.subheader("🟢 Jug B")
            st.write(f"Capacity: {capacity_b} litres")

            st.metric(
                "Current water",
                f"{amount_b} L"
            )

            st.progress(
                amount_b / capacity_b,
                text=f"{amount_b} / {capacity_b} litres"
            )

        # Goal status
        if amount_a == target or amount_b == target:

            st.success(
                f"Target achieved: {target} litre(s)!"
            )

        else:

            st.warning(
                f"Target of {target} litre(s) "
                "has not been reached at this step."
            )

        # Navigation buttons
        prev_col, reset_col, next_col = st.columns(3)

        with prev_col:
            st.button(
                "⬅ Previous",
                on_click=previous_step,
                disabled=(selected_step == 0),
                width="stretch"
            )

        with reset_col:
            st.button(
                "↺ Reset",
                on_click=reset_step,
                width="stretch"
            )

        with next_col:
            st.button(
                "Next ➡",
                on_click=next_step,
                disabled=(selected_step == total_steps),
                width="stretch"
            )

        # ------------------------------------------
        # COMPLETE STATE-SPACE GRAPH
        # ------------------------------------------

        st.divider()
        st.header("4. Complete State-Space Graph")

        st.write(
            "Every node represents a reachable state. "
            "Directed edges represent valid water-jug "
            "operations. The colors identify the initial "
            "state, target states, solution states, and "
            "other reachable states."
        )

        full_graph_fig = draw_state_graph(
            capacity_a,
            capacity_b,
            target,
            path
        )

        st.pyplot(full_graph_fig)
        plt.close(full_graph_fig)

        st.caption(
            "Green: Initial state | Gold: Target state | "
            "Blue: BFS solution path | Grey: Other states"
        )

        # ------------------------------------------
        # BFS SHORTEST-PATH GRAPH
        # ------------------------------------------

        st.divider()
        st.header("5. BFS Shortest Solution Path")

        st.write(
            "This graph shows only the states in the "
            "shortest solution found by BFS. Each arrow "
            "is labelled with the operation performed."
        )

        path_fig = draw_solution_path(
            path,
            capacity_a,
            capacity_b,
            target
        )

        st.pyplot(path_fig)
        plt.close(path_fig)

        # ------------------------------------------
        # SOLUTION TABLE
        # ------------------------------------------

        st.divider()
        st.header("6. Complete Solution Path")

        solution_table = []

        for step_number, item in enumerate(path):

            a, b = item["state"]

            solution_table.append({
                "Step": step_number,
                "Operation": item["operation"],
                "Jug A (L)": a,
                "Jug B (L)": b
            })

        st.dataframe(
            solution_table,
            width="stretch",
            hide_index=True
        )

        # ------------------------------------------
        # DOWNLOAD REPORT
        # ------------------------------------------

        st.divider()
        st.header("7. Download Solution Report")

        report_lines = [
            "WATER JUG PROBLEM SOLUTION",
            "MFC Project P009",
            "",
            f"Jug A capacity: {capacity_a} litres",
            f"Jug B capacity: {capacity_b} litres",
            f"Target: {target} litres",
            f"Minimum operations: {result['operations']}",
            f"States explored: {result['states_explored']}",
            "",
            "SOLUTION PATH"
        ]

        for step_number, item in enumerate(path):

            report_lines.append(
                f"Step {step_number}: "
                f"{item['operation']} -> {item['state']}"
            )

        st.download_button(
            label="📥 Download Solution Report",
            data="\n".join(report_lines),
            file_name="water_jug_solution.txt",
            mime="text/plain",
            width="stretch"
        )


# --------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------

with st.expander("About this project"):

    st.write(
        "The Water Jug Problem is modelled as a "
        "state-space graph. Each state (x, y) represents "
        "the amount of water in Jug A and Jug B."
    )

    st.write(
        "Breadth-First Search (BFS) explores reachable "
        "states using a queue. Since every operation has "
        "equal cost, BFS finds a solution with the minimum "
        "number of operations."
    )

    st.write(
        "The six permitted operations are filling either "
        "jug, emptying either jug, and pouring water "
        "from one jug into the other."
    )
