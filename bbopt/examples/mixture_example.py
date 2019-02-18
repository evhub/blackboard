"""
Example using a mixture distribution over many different possible algorithms.

To run this example, just run:
    > bbopt ./mixture_example.py
"""

# BBopt setup:
from bbopt import BlackBoxOptimizer
bb = BlackBoxOptimizer(file=__file__, use_json=True)
if __name__ == "__main__":
    bb.run_backend("mixture", [
        ("gaussian_process", 1),
        ("random_forest", 1),
        ("extra_trees", 1),
        ("gradient_boosted_regression_trees", 1),
        ("tree_structured_parzen_estimator", 1),
        ("annealing", 1),
    ])


# If we're not serving, store which algorithm the
#  mixture backend has selected.
from bbopt.backends.mixture import MixtureBackend
if isinstance(bb.backend, MixtureBackend):
    bb.remember({
        "alg": bb.backend.selected_alg,
    })


# Set up a parameter from a random sample.
xs = bb.sample("xs", range(10), 5)


# Set the goal to be the sum.
y = sum(xs)
bb.minimize(y)


# Finally, we'll print out the value we used for debugging purposes.
if __name__ == "__main__":
    print(repr(y))