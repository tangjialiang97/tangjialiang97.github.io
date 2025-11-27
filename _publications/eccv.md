---
title: "Direct Distillation between Different Domains"
collection: publications
category: conferences
permalink: /publication/eccv
date: 2024-01-01
venue: 'ECCV'
paperurl: 'https://arxiv.org/pdf/2401.06826'
citation: 'Tang, Jialiang, Shuo Chen, Gang Niu, Hongyuan Zhu, Joey Tianyi Zhou, Chen Gong, and Masashi Sugiyama. "Direct distillation between different domains." In European Conference on Computer Vision, pp. 154-172. Cham: Springer Nature Switzerland, 2024.'
---

Knowledge Distillation (KD) aims to learn a compact student network using knowledge from a large pre-trained teacher network, where both networks are trained on data from the same distribution. However, in practical applications, the student network may be required to perform in a new scenario (i.e., the target domain), which usually exhibits significant differences from the known scenario of the teacher network (i.e., the source domain). The traditional domain adaptation techniques can be integrated with KD in a two-stage process to bridge the domain gap, but the ultimate reliability of two-stage approaches tends to be limited due to the high computational consumption and the additional errors accumulated from both stages. To solve this problem, we propose a new one-stage method dubbed “Direct Distillation between Different Domains” (4Ds). We first design a learnable adapter based on the Fourier transform to separate the domain-invariant knowledge from the domain-specific knowledge. Then, we build a fusion-activation mechanism to transfer the valuable domain-invariant knowledge to the student network, while simultaneously encouraging the adapter within the teacher network to learn the domain-specific knowledge of the target data. As a result, the teacher network can effectively transfer categorical knowledge that aligns with the target domain of the student network. Intensive experiments on various benchmark datasets demonstrate that our proposed 4Ds method successfully produces reliable student networks and outperforms state-of-the-art approaches. Code is available at https://github.com/tangjialiang97/4Ds.
