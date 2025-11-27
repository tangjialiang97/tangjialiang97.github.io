---
title: "Open-World Semi-Supervised Learning under Compound Distribution Shifts"
collection: publications
category: conferences
permalink: /publication/bmvc
date: 2024-02-01
venue: 'GitHub Journal of Bugs'
paperurl: 'https://bmva-archive.org.uk/bmvc/2024/papers/Paper_762/paper.pdf'
citation: 'Xu, Shijia, Lin Zhao, Jialiang Tang, Guangyu Li, and Chen Gong. "Open-World Semi-Supervised Learning under Compound Distribution Shifts." (2024).'
---

Open-world Semi-Supervised Learning (OSSL) has drawn significant attention recently which assumes that the scarce labeled data and abundant unlabeled data for classifier training are sampled from different distributions. Existing methods typically assume that all unlabeled examples are drawn from the same domain following the same distribution. Nevertheless, this assumption may be violated as the unlabeled data are often collected from multiple unknown domains practically. Therefore, this paper tries to solve the OSSL problem under compound distribution shifts, in which the unlabeled data are from multiple unknown domains which may deviate from the distribution of labeled data. Specifically, we propose a novel Adversarial Mutual Information Disentanglement (AMID) framework to capture domain-invariant features for classifier training without the knowledge of domains. Particularly, we find that the class tokens of the pre-trained Vision Transformer (ViT) carry critical cues reflecting the styles of unlabeled data which can be deployed to attribute unlabeled data into different discovered domains. Subsequently, we train a feature encoder which captures the domain-invariant features shared among the attributed domains via designed adversarial confusion loss, so that the trained feature encoder can accurately represent the semantic information of unlabeled examples regardless of their domains. To further enhance feature disentanglement and enlarge the gap between useful domain-invariant features and interfered domain-specific features, we minimize the mutual information between the outputs of the encoders corresponding to domain-invariant features and domain-specific features. Comprehensive experiments conducted on various benchmark datasets demonstrate the effectiveness and generalizability of our approach in resolving the issue of compound distribution shifts in OSSL.
