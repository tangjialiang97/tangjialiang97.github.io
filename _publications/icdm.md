---
title: "Empowering Large Language Models for Time Series Forecasting with Patterns and Semantics"
collection: publications
category: conferences
permalink: /publication/icdm
date: 2025-08-01
venue: 'ICDM'
paperurl: 'https://arxiv.org/abs/2503.09656'
citation: 'Tang, Jialiang, Shuo Chen, Chen Gong, Jing Zhang, and Dacheng Tao. "LLM-PS: Empowering Large Language Models for Time Series Forecasting with Temporal Patterns and Semantics." arXiv preprint arXiv:2503.09656 (2025).'
---

Time Series Forecasting (TSF) is critical in many real-world domains like financial planning and health monitoring. Recent studies have revealed that Large Language Models (LLMs), with their powerful in-contextual modeling capabilities, hold significant potential for TSF. However, existing LLM-based methods usually perform suboptimally because they neglect the inherent characteristics of time series data. Unlike the textual data used in LLM pre-training, the time series data is semantically sparse and comprises distinctive temporal patterns. To address this problem, we propose LLM-PS to empower the LLM for TSF by learning the fundamental \textit{Patterns} and meaningful \textit{Semantics} from time series data. Our LLM-PS incorporates a new multi-scale convolutional neural network adept at capturing both short-term fluctuations and long-term trends within the time series. Meanwhile, we introduce a time-to-text module for extracting valuable semantics across continuous time intervals rather than isolated time points. By integrating these patterns and semantics, LLM-PS effectively models temporal dependencies, enabling a deep comprehension of time series and delivering accurate forecasts. Intensive experimental results demonstrate that LLM-PS achieves state-of-the-art performance in both short- and long-term forecasting tasks, as well as in few- and zero-shot settings.
