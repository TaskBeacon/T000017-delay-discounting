from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Any
import random as _py_random

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Delay-discounting sampler responder.

    Choice model:
    - Subjective value (hyperbolic): SV_LL = A / (1 + k * D)
    - Soft choice: P(choose LL) = sigmoid(beta * (SV_LL - SV_SS))
    - Lapse mixes toward 0.5 random choice.
    """

    continue_key: str = "space"
    discount_k: float = 0.015
    inverse_temp: float = 0.25
    lapse_rate: float = 0.03
    rt_mean_s: float = 0.85
    rt_sd_s: float = 0.18
    rt_min_s: float = 0.20

    def __post_init__(self) -> None:
        self._rng: Any = None
        self.discount_k = max(1e-8, float(self.discount_k))
        self.inverse_temp = max(1e-8, float(self.inverse_temp))
        self.lapse_rate = max(0.0, min(1.0, float(self.lapse_rate)))
        self.rt_mean_s = max(1e-3, float(self.rt_mean_s))
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _sample_normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        return float(rng.gauss(mean, sd))

    def _sample_random(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return float(_py_random.random())

    def _sigmoid(self, x: float) -> float:
        if x >= 0:
            z = exp(-x)
            return 1.0 / (1.0 + z)
        z = exp(x)
        return z / (1.0 + z)

    def act(self, obs: Observation) -> Action:
        valid_keys = list(obs.valid_keys or [])
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "delay_sampler", "reason": "no_valid_keys"})

        if self._rng is None:
            return Action(key=None, rt_s=None, meta={"source": "delay_sampler", "reason": "rng_missing"})

        phase = str(obs.phase or "")
        if phase not in ("choice", "target"):
            if self.continue_key in valid_keys:
                rt = max(self.rt_min_s, self._sample_normal(self.rt_mean_s, self.rt_sd_s))
                return Action(
                    key=self.continue_key,
                    rt_s=rt,
                    meta={"source": "delay_sampler", "phase": phase, "outcome": "continue"},
                )
            if len(valid_keys) == 1:
                rt = max(self.rt_min_s, self._sample_normal(self.rt_mean_s, self.rt_sd_s))
                return Action(
                    key=str(valid_keys[0]),
                    rt_s=rt,
                    meta={"source": "delay_sampler", "phase": phase, "outcome": "continue_single"},
                )
            return Action(key=None, rt_s=None, meta={"source": "delay_sampler", "phase": phase})

        factors = dict(obs.task_factors or {})

        try:
            ss_amount = float(factors.get("ss_amount"))
            ll_amount = float(factors.get("ll_amount"))
            delay_days = float(factors.get("delay_days"))
        except Exception:
            return Action(key=None, rt_s=None, meta={"source": "delay_sampler", "reason": "missing_values"})

        ss_key = str(factors.get("ss_key", "")).strip()
        ll_key = str(factors.get("ll_key", "")).strip()

        if ss_key not in valid_keys or ll_key not in valid_keys:
            return Action(
                key=None,
                rt_s=None,
                meta={
                    "source": "delay_sampler",
                    "reason": "missing_choice_keys",
                    "ss_key": ss_key,
                    "ll_key": ll_key,
                },
            )

        sv_ss = ss_amount
        sv_ll = ll_amount / (1.0 + self.discount_k * max(0.0, delay_days))
        p_ll_base = self._sigmoid(self.inverse_temp * (sv_ll - sv_ss))
        p_ll = (1.0 - self.lapse_rate) * p_ll_base + self.lapse_rate * 0.5

        choose_ll = self._sample_random() < p_ll
        key = ll_key if choose_ll else ss_key

        rt = max(self.rt_min_s, self._sample_normal(self.rt_mean_s, self.rt_sd_s))

        return Action(
            key=key,
            rt_s=rt,
            meta={
                "source": "delay_sampler",
                "outcome": "ll" if choose_ll else "ss",
                "sv_ss": sv_ss,
                "sv_ll": sv_ll,
                "p_ll": p_ll,
                "discount_k": self.discount_k,
                "inverse_temp": self.inverse_temp,
            },
        )
