from __future__ import annotations

from typing import Any
import random

from psychopy import logging


# Kirby et al. style 27-item Monetary Choice Questionnaire (MCQ-27)
# (as reported in Kaplan et al., 2016; table with small/medium/large sets)
MCQ27_ITEMS: list[dict[str, Any]] = [
    {"item_id": 1, "magnitude": "small", "ss_amount": 25, "ll_amount": 30, "delay_days": 14, "k_ref": 0.014286},
    {"item_id": 2, "magnitude": "small", "ss_amount": 35, "ll_amount": 35, "delay_days": 186, "k_ref": 0.016129},
    {"item_id": 3, "magnitude": "small", "ss_amount": 40, "ll_amount": 55, "delay_days": 62, "k_ref": 0.006048},
    {"item_id": 4, "magnitude": "small", "ss_amount": 30, "ll_amount": 35, "delay_days": 41, "k_ref": 0.004065},
    {"item_id": 5, "magnitude": "small", "ss_amount": 15, "ll_amount": 35, "delay_days": 13, "k_ref": 0.102564},
    {"item_id": 6, "magnitude": "small", "ss_amount": 25, "ll_amount": 60, "delay_days": 14, "k_ref": 0.100000},
    {"item_id": 7, "magnitude": "small", "ss_amount": 40, "ll_amount": 45, "delay_days": 62, "k_ref": 0.002016},
    {"item_id": 8, "magnitude": "small", "ss_amount": 25, "ll_amount": 55, "delay_days": 31, "k_ref": 0.038710},
    {"item_id": 9, "magnitude": "small", "ss_amount": 55, "ll_amount": 75, "delay_days": 61, "k_ref": 0.005962},
    {"item_id": 10, "magnitude": "medium", "ss_amount": 30, "ll_amount": 35, "delay_days": 186, "k_ref": 0.000896},
    {"item_id": 11, "magnitude": "medium", "ss_amount": 80, "ll_amount": 85, "delay_days": 157, "k_ref": 0.000398},
    {"item_id": 12, "magnitude": "medium", "ss_amount": 65, "ll_amount": 75, "delay_days": 119, "k_ref": 0.001293},
    {"item_id": 13, "magnitude": "medium", "ss_amount": 55, "ll_amount": 60, "delay_days": 117, "k_ref": 0.000777},
    {"item_id": 14, "magnitude": "medium", "ss_amount": 40, "ll_amount": 55, "delay_days": 62, "k_ref": 0.006048},
    {"item_id": 15, "magnitude": "medium", "ss_amount": 65, "ll_amount": 85, "delay_days": 35, "k_ref": 0.008791},
    {"item_id": 16, "magnitude": "medium", "ss_amount": 70, "ll_amount": 80, "delay_days": 162, "k_ref": 0.000882},
    {"item_id": 17, "magnitude": "medium", "ss_amount": 80, "ll_amount": 95, "delay_days": 157, "k_ref": 0.001195},
    {"item_id": 18, "magnitude": "medium", "ss_amount": 50, "ll_amount": 60, "delay_days": 89, "k_ref": 0.002247},
    {"item_id": 19, "magnitude": "large", "ss_amount": 35, "ll_amount": 85, "delay_days": 7, "k_ref": 0.204082},
    {"item_id": 20, "magnitude": "large", "ss_amount": 80, "ll_amount": 100, "delay_days": 30, "k_ref": 0.008333},
    {"item_id": 21, "magnitude": "large", "ss_amount": 65, "ll_amount": 85, "delay_days": 30, "k_ref": 0.010256},
    {"item_id": 22, "magnitude": "large", "ss_amount": 50, "ll_amount": 75, "delay_days": 14, "k_ref": 0.035714},
    {"item_id": 23, "magnitude": "large", "ss_amount": 65, "ll_amount": 75, "delay_days": 61, "k_ref": 0.002520},
    {"item_id": 24, "magnitude": "large", "ss_amount": 90, "ll_amount": 100, "delay_days": 30, "k_ref": 0.003704},
    {"item_id": 25, "magnitude": "large", "ss_amount": 45, "ll_amount": 60, "delay_days": 14, "k_ref": 0.023810},
    {"item_id": 26, "magnitude": "large", "ss_amount": 35, "ll_amount": 45, "delay_days": 20, "k_ref": 0.014286},
    {"item_id": 27, "magnitude": "large", "ss_amount": 60, "ll_amount": 80, "delay_days": 30, "k_ref": 0.011111},
]


VALID_MAGNITUDES = ("small", "medium", "large")


def normalize_magnitude(value: str) -> str:
    magnitude = str(value).strip().lower()
    if magnitude not in VALID_MAGNITUDES:
        raise ValueError(f"Unsupported delay-discounting magnitude: {value!r}")
    return magnitude


def normalize_item_pool(item_pool: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    pool = list(item_pool) if item_pool is not None else [dict(x) for x in MCQ27_ITEMS]
    normalized: list[dict[str, Any]] = []
    for raw in pool:
        item = dict(raw)
        normalized.append(
            {
                "item_id": int(item["item_id"]),
                "magnitude": normalize_magnitude(str(item["magnitude"])),
                "ss_amount": float(item["ss_amount"]),
                "ll_amount": float(item["ll_amount"]),
                "delay_days": int(item["delay_days"]),
                "k_ref": float(item["k_ref"]),
            }
        )
    if not normalized:
        raise ValueError("Delay-discounting item pool cannot be empty.")
    return normalized


def _filter_item_pool_by_conditions(
    item_pool: list[dict[str, Any]],
    condition_labels: list[Any] | None,
) -> list[dict[str, Any]]:
    if not condition_labels:
        return [dict(x) for x in item_pool]

    allowed = {normalize_magnitude(str(label)) for label in condition_labels}
    filtered = [dict(item) for item in item_pool if normalize_magnitude(str(item["magnitude"])) in allowed]
    if not filtered:
        raise ValueError(
            "No delay-discounting items remain after filtering by condition labels "
            f"{list(condition_labels)!r}."
        )
    return filtered


def build_block_plan(
    n_trials: int,
    *,
    seed: int | None,
    condition_labels: list[Any] | None = None,
    item_pool: list[dict[str, Any]] | None = None,
    randomize_order: bool = True,
    counterbalance_sides: bool = True,
    ll_left_prob: float = 0.5,
) -> list[dict[str, Any]]:
    """Build one deterministic MCQ trial plan for a block."""
    n_trials = int(n_trials)
    if n_trials <= 0:
        return []

    ll_left_prob = max(0.0, min(1.0, float(ll_left_prob)))
    rng = random.Random(seed)
    base_pool = _filter_item_pool_by_conditions(normalize_item_pool(item_pool), condition_labels)

    planned: list[dict[str, Any]] = []
    while len(planned) < n_trials:
        chunk = [dict(x) for x in base_pool]
        if bool(randomize_order):
            rng.shuffle(chunk)
        planned.extend(chunk)
    planned = planned[:n_trials]

    if bool(counterbalance_sides):
        n_left = n_trials // 2
        ll_sides = ["left"] * n_left + ["right"] * (n_trials - n_left)
        rng.shuffle(ll_sides)
    else:
        ll_sides = ["left" if rng.random() < ll_left_prob else "right" for _ in range(n_trials)]

    for idx, trial in enumerate(planned, start=1):
        ll_side = ll_sides[idx - 1]
        ss_side = "right" if ll_side == "left" else "left"
        left_is_ll = ll_side == "left"

        left_amount = float(trial["ll_amount"]) if left_is_ll else float(trial["ss_amount"])
        right_amount = float(trial["ss_amount"]) if left_is_ll else float(trial["ll_amount"])
        left_delay = int(trial["delay_days"]) if left_is_ll else 0
        right_delay = 0 if left_is_ll else int(trial["delay_days"])

        trial.update(
            block_trial_index=idx,
            ll_side=ll_side,
            ss_side=ss_side,
            left_amount=left_amount,
            right_amount=right_amount,
            left_delay_days=left_delay,
            right_delay_days=right_delay,
            condition_id=f"{trial['magnitude']}|item{int(trial['item_id'])}|ll_{ll_side}",
        )

    return planned


def build_block_conditions(
    n_trials: int,
    condition_labels: list[Any] | None = None,
    *,
    seed: int | None = None,
    enable_logging: bool = True,
    item_pool: list[dict[str, Any]] | None = None,
    randomize_order: bool = True,
    counterbalance_sides: bool = True,
    ll_left_prob: float = 0.5,
    **_: Any,
) -> list[str]:
    """BlockUnit custom generator that outputs readable magnitude labels."""
    plan = build_block_plan(
        int(n_trials),
        seed=seed,
        condition_labels=condition_labels,
        item_pool=item_pool,
        randomize_order=bool(randomize_order),
        counterbalance_sides=bool(counterbalance_sides),
        ll_left_prob=float(ll_left_prob),
    )

    if enable_logging:
        dist: dict[str, int] = {}
        for trial in plan:
            magnitude = str(trial["magnitude"])
            dist[magnitude] = dist.get(magnitude, 0) + 1
        logging.data(
            "[DelayDiscountingConditionBuilder] "
            f"n_trials={len(plan)} seed={seed} dist={dist} "
            f"randomize_order={bool(randomize_order)} counterbalance_sides={bool(counterbalance_sides)}"
        )

    return [str(trial["magnitude"]) for trial in plan]


def get_block_trial_spec(
    *,
    block_idx: int,
    block_trial_index: int,
    n_trials: int,
    seed: int | None,
    condition_labels: list[Any] | None = None,
    item_pool: list[dict[str, Any]] | None = None,
    randomize_order: bool = True,
    counterbalance_sides: bool = True,
    ll_left_prob: float = 0.5,
    expected_condition: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Reconstruct one planned trial spec deterministically for the given block position."""
    plan = build_block_plan(
        int(n_trials),
        seed=seed,
        condition_labels=condition_labels,
        item_pool=item_pool,
        randomize_order=bool(randomize_order),
        counterbalance_sides=bool(counterbalance_sides),
        ll_left_prob=float(ll_left_prob),
    )
    idx = int(block_trial_index)
    if idx < 1 or idx > len(plan):
        raise IndexError(
            f"Block trial index out of range: block_trial_index={idx}, n_planned={len(plan)}"
        )

    spec = dict(plan[idx - 1])
    spec["block_idx"] = int(block_idx)

    if expected_condition is not None:
        expected = normalize_magnitude(str(expected_condition))
        actual = normalize_magnitude(str(spec["magnitude"]))
        if expected != actual:
            raise ValueError(
                "Delay-discounting condition mismatch between BlockUnit condition label and "
                f"deterministic plan: expected={expected!r}, actual={actual!r}"
            )

    return spec
