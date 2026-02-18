from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List
import random

from psychopy import logging


# Kirby et al. style 27-item Monetary Choice Questionnaire (MCQ-27)
# (as reported in Kaplan et al., 2016; table with small/medium/large sets)
MCQ27_ITEMS: List[Dict[str, Any]] = [
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


@dataclass
class DelayDiscountingController:
    """Prepare and serve per-trial offer pairs for delay discounting."""

    randomize_order: bool = True
    counterbalance_sides: bool = True
    ll_left_prob: float = 0.5
    enable_logging: bool = True
    item_pool: List[Dict[str, Any]] = field(default_factory=lambda: [dict(x) for x in MCQ27_ITEMS])

    def __post_init__(self) -> None:
        self.ll_left_prob = max(0.0, min(1.0, float(self.ll_left_prob)))
        self.item_pool = [dict(x) for x in self.item_pool]
        self._queues: Dict[int, List[Dict[str, Any]]] = {}
        self._trial_counter: int = 0

    @classmethod
    def from_dict(cls, config: dict) -> "DelayDiscountingController":
        allowed = {
            "randomize_order": True,
            "counterbalance_sides": True,
            "ll_left_prob": 0.5,
            "enable_logging": True,
            "item_pool": [dict(x) for x in MCQ27_ITEMS],
        }
        extra = set(config.keys()) - set(allowed)
        if extra:
            raise ValueError(f"[DelayDiscountingController] Unsupported config keys: {extra}")
        final = {k: config.get(k, default) for k, default in allowed.items()}
        return cls(**final)

    def _build_plan(self, n_trials: int, seed: int | None) -> List[Dict[str, Any]]:
        if n_trials <= 0:
            return []

        rng = random.Random(seed)
        base_pool = [dict(x) for x in self.item_pool]
        planned: List[Dict[str, Any]] = []

        while len(planned) < n_trials:
            chunk = [dict(x) for x in base_pool]
            if self.randomize_order:
                rng.shuffle(chunk)
            planned.extend(chunk)

        planned = planned[:n_trials]

        if self.counterbalance_sides:
            n_left = n_trials // 2
            ll_sides = ["left"] * n_left + ["right"] * (n_trials - n_left)
            rng.shuffle(ll_sides)
        else:
            ll_sides = ["left" if rng.random() < self.ll_left_prob else "right" for _ in range(n_trials)]

        for i, trial in enumerate(planned, start=1):
            ll_side = ll_sides[i - 1]
            ss_side = "right" if ll_side == "left" else "left"
            left_is_ll = ll_side == "left"

            left_amount = trial["ll_amount"] if left_is_ll else trial["ss_amount"]
            right_amount = trial["ss_amount"] if left_is_ll else trial["ll_amount"]
            left_delay = trial["delay_days"] if left_is_ll else 0
            right_delay = 0 if left_is_ll else trial["delay_days"]

            trial.update(
                block_trial_index=i,
                ll_side=ll_side,
                ss_side=ss_side,
                left_amount=left_amount,
                right_amount=right_amount,
                left_delay_days=left_delay,
                right_delay_days=right_delay,
            )

        return planned

    def prepare_block(self, block_idx: int, n_trials: int, seed: int | None) -> List[str]:
        plan = self._build_plan(int(n_trials), seed)
        self._queues[int(block_idx)] = list(plan)

        if self.enable_logging:
            dist: Dict[str, int] = {}
            for t in plan:
                c = str(t.get("magnitude", "unknown"))
                dist[c] = dist.get(c, 0) + 1
            logging.data(
                f"[DelayDiscountingController] block={block_idx} n_trials={len(plan)} "
                f"seed={seed} dist={dist}"
            )

        return [str(t["magnitude"]) for t in plan]

    def next_trial(self, block_idx: int, expected_condition: str | None = None) -> Dict[str, Any]:
        queue = self._queues.get(int(block_idx), [])
        if not queue:
            raise RuntimeError(
                f"[DelayDiscountingController] No remaining planned trials for block_idx={block_idx}."
            )

        spec = dict(queue.pop(0))
        self._trial_counter += 1
        spec["global_trial_id"] = self._trial_counter

        if expected_condition and str(spec.get("magnitude")) != str(expected_condition):
            logging.warning(
                "[DelayDiscountingController] Condition mismatch: "
                f"expected={expected_condition} actual={spec.get('magnitude')}"
            )

        return spec
