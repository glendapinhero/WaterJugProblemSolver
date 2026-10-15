
from collections import deque
from math import gcd


def get_next_states(state, capacity_a, capacity_b):
    """
    Generate all valid next states from the current state.

    State format: (amount_a, amount_b)
    """

    a, b = state

    next_states = []

    # 1. Fill Jug A
    next_states.append(
        ((capacity_a, b), "Fill Jug A")
    )

    # 2. Fill Jug B
    next_states.append(
        ((a, capacity_b), "Fill Jug B")
    )

    # 3. Empty Jug A
    next_states.append(
        ((0, b), "Empty Jug A")
    )

    # 4. Empty Jug B
    next_states.append(
        ((a, 0), "Empty Jug B")
    )

    # 5. Pour water from Jug A into Jug B
    transfer = min(a, capacity_b - b)

    next_states.append(
        (
            (a - transfer, b + transfer),
            "Pour A into B"
        )
    )

    # 6. Pour water from Jug B into Jug A
    transfer = min(b, capacity_a - a)

    next_states.append(
        (
            (a + transfer, b - transfer),
            "Pour B into A"
        )
    )

    # Remove unchanged and duplicate states
    unique_states = []
    seen = set()

    for next_state, operation in next_states:
        if next_state != state and next_state not in seen:
            unique_states.append((next_state, operation))
            seen.add(next_state)

    return unique_states


def is_target_possible(capacity_a, capacity_b, target):
    """
    Check whether the target is mathematically achievable.
    Assumes integer capacities and target.
    """

    if target == 0:
        return True

    if target > max(capacity_a, capacity_b):
        return False

    return target % gcd(capacity_a, capacity_b) == 0


def bfs_solve(capacity_a, capacity_b, target):
    """
    Solve the Water Jug Problem using Breadth-First Search.

    Returns:
        Solution path
        Minimum number of operations
        Number of states explored

    Returns None if no solution exists.
    """

    # Validate input
    if capacity_a <= 0 or capacity_b <= 0:
        raise ValueError("Jug capacities must be positive.")

    if target < 0:
        raise ValueError("Target cannot be negative.")

    # Check feasibility before searching
    if not is_target_possible(
        capacity_a, capacity_b, target
    ):
        return None

    # Initial state
    start = (0, 0)

    # BFS queue
    queue = deque([start])

    # Store visited states
    visited = {start}

    # Store the parent state and operation
    parent = {start: None}

    # Count states removed from the queue
    states_explored = 0

    while queue:

        # Explore the oldest state first
        current = queue.popleft()
        states_explored += 1

        a, b = current

        # Check whether the target is reached
        if a == target or b == target:

            # Reconstruct the path
            path = []
            state = current

            while state is not None:

                previous = parent[state]

                if previous is None:
                    path.append({
                        "state": state,
                        "operation": "Start"
                    })

                    state = None

                else:
                    previous_state, operation = previous

                    path.append({
                        "state": state,
                        "operation": operation
                    })

                    state = previous_state

            # Reverse to get start-to-goal order
            path.reverse()

            return {
                "path": path,
                "operations": len(path) - 1,
                "states_explored": states_explored
            }

        # Generate all possible next states
        for next_state, operation in get_next_states(
            current,
            capacity_a,
            capacity_b
        ):

            # Visit each state only once
            if next_state not in visited:

                visited.add(next_state)

                # Record how this state was reached
                parent[next_state] = (current, operation)

                # Add it to the BFS queue
                queue.append(next_state)

    # No solution found
    return None


def display_result(capacity_a, capacity_b, target):
    """
    Run BFS and display the complete solution.
    """

    print("\n" + "=" * 45)
    print("       WATER JUG PROBLEM SOLVER")
    print("=" * 45)

    print(f"Jug A capacity : {capacity_a} litres")
    print(f"Jug B capacity : {capacity_b} litres")
    print(f"Target amount  : {target} litres")

    try:
        result = bfs_solve(
            capacity_a,
            capacity_b,
            target
        )

    except ValueError as error:
        print("\nInvalid input:", error)
        return

    if result is None:
        print("\nNo solution exists for this target.")
        return

    print("\nSOLUTION PATH")
    print("-" * 45)

    for step, item in enumerate(result["path"]):
        state = item["state"]
        operation = item["operation"]

        print(
            f"Step {step}: {operation:<20} "
            f"State = {state}"
        )

    print("\nRESULT SUMMARY")
    print("-" * 45)

    print(
        "Minimum operations :",
        result["operations"]
    )

    print(
        "States explored    :",
        result["states_explored"]
    )

    print("\nTarget achieved successfully!")


if __name__ == "__main__":

    # Example test case
    capacity_a = 4
    capacity_b = 3
    target = 2

    display_result(
        capacity_a,
        capacity_b,
        target
    )
