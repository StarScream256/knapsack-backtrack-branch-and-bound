from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any

import pandas as pd
import plotly.graph_objects as go  # type: ignore
import streamlit as st

from model.models import Item


def items_to_dataframe(items: Sequence[Item]) -> pd.DataFrame:
    return pd.DataFrame([
        {
            "Price (Juta Rupiah)": item.price,
            "Processor": item.processor,
            "Memory": item.memory,
            "Storage": item.storage,
            "Skor Performa (Profit)": item.profit,
            "Ratio (Profit/Price)": item.ratio,
        }
        for item in items
    ])


def clear_session_keys(keys: Iterable[str]) -> None:
    for key in keys:
        st.session_state.pop(key, None)


def render_metric_summary(profit: float, nodes: int, elapsed_time: float, possible_combinations: int) -> None:
    st.success(f"**Skor Performa Total (Profit)**: {profit:.2f}")
    st.write(f"**Node dikunjungi**: {nodes:,} dari {possible_combinations:,} kemungkinan kombinasi")
    st.write(f"**Waktu**: {elapsed_time:.8f} seconds")


def bar_chart(labels: list[str], values: list[float], title: str, text_format: str, colors: list[str]) -> go.Figure:
    fig: Any = go.Figure()
    fig.add_trace(go.Bar(  # type: ignore[arg-type]
        x=labels,
        y=values,
        text=[text_format.format(value) for value in values],
        textposition="outside",
        marker_color=colors,
        textfont=dict(size=14, color="black", family="Arial Black"),
    ))
    fig.update_layout(  # type: ignore[call-arg]
        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(size=16),
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=50, t=50, b=50),
        height=450,
    )
    return fig


def line_chart(x_values: list[int], series: dict[str, list[float]], title: str, y_title: str) -> go.Figure:
    fig: Any = go.Figure()
    palette = ["#FF6B35", "#3A86FF", "#06D6A0", "#8338EC"]

    for index, (name, values) in enumerate(series.items()):
        fig.add_trace(go.Scatter(  # type: ignore[arg-type]
            x=x_values,
            y=values,
            mode="lines+markers",
            name=name,
            line=dict(color=palette[index % len(palette)], width=3),
            marker=dict(size=9),
        ))

    fig.update_layout(  # type: ignore[call-arg]
        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(size=16),
        ),
        xaxis_title="Jumlah Item (n)",
        yaxis_title=y_title,
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=50, t=50, b=50),
        height=450,
        legend_title_text="Algoritma",
    )
    return fig