"""5G downlink MAC scheduler comparison: RR, PF, and Max-C/I."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SimulationConfig:
    users: int = 20
    slots: int = 5_000
    bandwidth_hz: float = 20e6
    noise_power: float = 1e-10
    seed: int = 42


def jains_fairness(values: np.ndarray) -> float:
    """Return Jain's fairness index for non-negative user throughputs."""
    denominator = len(values) * np.square(values).sum()
    return float(np.square(values.sum()) / denominator) if denominator else 0.0


def spectral_efficiency(snr_linear: np.ndarray) -> np.ndarray:
    """Use a capped Shannon-style spectral-efficiency model (bit/s/Hz)."""
    return np.minimum(np.log2(1.0 + snr_linear), 7.4)


def generate_channels(config: SimulationConfig) -> tuple[np.ndarray, np.ndarray]:
    """Generate path loss and independent small-scale fading for all slots."""
    rng = np.random.default_rng(config.seed)
    # A small group near the cell edge makes the fairness trade-off visible.
    distances_m = np.linspace(80, 950, config.users)
    large_scale_gain = np.power(distances_m / 80, -3.3)
    fading_power = rng.exponential(scale=1.0, size=(config.slots, config.users))
    return large_scale_gain, fading_power


def choose_user(name: str, slot: int, rates: np.ndarray, average_rates: np.ndarray) -> int:
    if name == "Round-Robin":
        return slot % len(rates)
    if name == "Max-C/I":
        return int(np.argmax(rates))
    # Proportional Fair balances a high instantaneous rate with past service.
    return int(np.argmax(rates / np.maximum(average_rates, 1e-12)))


def simulate(name: str, config: SimulationConfig, gains: np.ndarray, fading: np.ndarray) -> dict[str, float]:
    delivered_bits = np.zeros(config.users)
    average_rates = np.full(config.users, 1e-9)
    slot_duration_s = 1e-3

    for slot in range(config.slots):
        snr = gains * fading[slot] / config.noise_power
        rates = spectral_efficiency(snr) * config.bandwidth_hz
        selected = choose_user(name, slot, rates, average_rates)
        served_rate = rates[selected]
        delivered_bits[selected] += served_rate * slot_duration_s

        instantaneous = np.zeros(config.users)
        instantaneous[selected] = served_rate
        average_rates = 0.99 * average_rates + 0.01 * instantaneous

    user_throughput_mbps = delivered_bits / (config.slots * slot_duration_s) / 1e6
    edge_count = max(1, int(np.ceil(config.users * 0.2)))
    return {
        "Scheduler": name,
        "Cell Throughput (Mbps)": float(user_throughput_mbps.sum()),
        "Jain Fairness Index": jains_fairness(user_throughput_mbps),
        "Cell-Edge Throughput (Mbps)": float(np.mean(user_throughput_mbps[-edge_count:])),
    }


def save_chart(results: pd.DataFrame, output_dir: Path) -> None:
    metrics = ["Cell Throughput (Mbps)", "Jain Fairness Index", "Cell-Edge Throughput (Mbps)"]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    colors = ["#0F6CBD", "#1A7F37", "#8250DF"]
    for axis, metric in zip(axes, metrics):
        axis.bar(results["Scheduler"], results[metric], color=colors)
        axis.set_title(metric)
        axis.tick_params(axis="x", rotation=25)
        axis.grid(axis="y", alpha=0.25)
    fig.suptitle("5G MAC Scheduler Comparison", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_dir / "scheduler_comparison.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare 5G downlink MAC scheduling algorithms.")
    parser.add_argument("--users", type=int, default=20, help="Number of UEs to simulate.")
    parser.add_argument("--slots", type=int, default=5_000, help="Number of 1 ms scheduling slots.")
    parser.add_argument("--output-dir", default="results", help="Directory for CSV and chart outputs.")
    args = parser.parse_args()

    config = SimulationConfig(users=args.users, slots=args.slots)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    gains, fading = generate_channels(config)
    results = pd.DataFrame(
        [simulate(name, config, gains, fading) for name in ("Round-Robin", "Proportional Fair", "Max-C/I")]
    )
    results.to_csv(output_dir / "scheduler_metrics.csv", index=False)
    save_chart(results, output_dir)
    print(results.to_string(index=False))
    print(f"\nSaved results to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()

