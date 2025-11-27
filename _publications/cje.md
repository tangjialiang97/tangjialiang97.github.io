---
title: "Exploring Neural Radiance Fields for Thermal View Synthesis Solely with Thermal Inputs"
collection: publications
category: manuscripts
permalink: /publication/cje
date: 2025-06-08
venue: 'Chinese Journal of Electronics'
paperurl: 'https://gcatnjust.github.io/ChenGong/paper/ding_cje25.pdf'
citation: 'Ding, Haixuan, Jialiang Tang, Sheng Wan, and Chen Gong. "Exploring Neural Radiance Fields for Thermal View Synthesis Solely with Thermal Inputs." Chinese Journal of Electronics (2025).'
---

Novel View Synthesis (NVS) for thermal scenes aims to generate thermal images from unseen viewpoints, which shows great potential in various applications, such as nighttime autonomous driving, industrial inspection, and agricultural monitoring. Recently, Neural Radiance Fields (NeRF) have emerged as a powerful approach for NVS in thermal scenes, which typically require paired RGB and thermal images to produce realistic thermal images from new views. However, practical limitations, such as insufficient lighting, the prohibitive cost of RGB image acquisition, or the lack of RGB cameras, make it challenging or even impossible to obtain high-quality RGB images, which prevents the existing NeRF methods from generating realistic thermal images. To address this problem, we devise a simple yet effective NeRF framework based on Thermal Radiation Prediction, which is termed ‘NeRF-TRP’, for NVS in thermal scenes. Unlike the existing NeRF techniques that rely on paired RGB and thermal images, NeRF-TRP exclusively utilizes thermal images as input. By leveraging the principle of thermal imaging, NeRF-TRP predicts the thermal radiation emitted by objects to render thermal images from novel views. Meanwhile, motivated by the thermal equilibrium observed in thermal scenes, we design a patchbased regularization to enhance the realism of the generated thermal images. Extensive experiments on thermal images demonstrate that NeRF-TRP not only produces more accurate thermal image synthesis, but also reveals superior efficiency in both training and rendering when compared with various representative baseline approaches.