
from solver import bfs_solve


def run_tests():

    # Format: (Jug A, Jug B, Target, Expected solution)
    test_cases = [
        (4, 3, 2, True),    # Standard example
        (3, 5, 4, True),    # Another achievable target
        (4, 6, 3, False),   # Target not divisible by GCD
        (3, 5, 6, False),   # Target exceeds both capacities
        (4, 3, 0, True),    # Already solved
        (2, 3, 1, True),    # Small capacities
        (5, 7, 6, True),    # Larger capacities
    ]

    passed = 0

    print("\nWATER JUG SOLVER - TEST RESULTS")
    print("=" * 65)

    for capacity_a, capacity_b, target, expected in test_cases:

        result = bfs_solve(
            capacity_a,
            capacity_b,
            target
        )

        actual = result is not None
        status = "PASS" if actual == expected else "FAIL"

        print(
            f"{status} | A={capacity_a}, B={capacity_b}, "
            f"Target={target} | Expected={expected}, Actual={actual}"
        )

        if actual == expected:
            passed += 1

        # Validate the returned solution
        if result is not None:

            path = result["path"]

            # Number of operations must match the path length
            assert result["operations"] == len(path) - 1

            # The path must begin with both jugs empty
            assert path[0]["state"] == (0, 0)

            # The final state must contain the target
            final_a, final_b = path[-1]["state"]

            assert final_a == target or final_b == target

            # Every state must respect jug capacities
            for item in path:
                a, b = item["state"]

                assert 0 <= a <= capacity_a
                assert 0 <= b <= capacity_b

    print("=" * 65)
    print(f"Tests passed: {passed}/{len(test_cases)}")


if __name__ == "__main__":
    run_tests()
