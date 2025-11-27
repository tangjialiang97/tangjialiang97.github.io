---
title: "Learning Student Network under Universal Label Noise"
collection: publications
category: manuscripts
permalink: /publication/tip
date: 2023-10-01
venue: 'IEEE Transactions on Image Processing'
paperurl: 'https://ieeexplore.ieee.org/document/10614116'
citation: 'Tang, Jialiang, Ning Jiang, Hongyuan Zhu, Joey Tianyi Zhou, and Chen Gong. "Learning student network under universal label noise." IEEE Transactions on Image Processing (2024).'
---

Data-free knowledge distillation aims to learn a small student network from a large pre-trained teacher network without the aid of original training data. Recent works propose to gather alternative data from the Internet for training student network. In a more realistic scenario, the data on the Internet contains two types of label noise, namely: 1) closed-set label noise, where some examples belong to the known categories but are mislabeled; and 2) open-set label noise, where the true labels of some mislabeled examples are outside the known categories. However, the latter is largely ignored by existing works, leading to limited student network performance. Therefore, this paper proposes a novel data-free knowledge distillation paradigm by utilizing a webly-collected dataset under universal label noise, which means both closed-set and open-set label noise should be tackled. Specifically, we first split the collected noisy dataset into clean set, closed noisy set, and open noisy set based on the prediction uncertainty of various data types. For the closed-set noisy examples, their labels are refined by teacher network. Meanwhile, a noise-robust hybrid contrastive learning is performed on the clean set and refined closed noisy set to encourage student network to learn the categorical and instance knowledge inherited by teacher network. For the open-set noisy examples unexplored by previous work, we regard them as unlabeled and conduct self-supervised learning on them to enrich the supervision signal for student network. Intensive experimental results on image classification tasks demonstrate that our approach can achieve superior performance to state-of-the-art data-free knowledge distillation methods.
