---
tags: [transformer, attention, sequence-to-sequence, machine-translation, deep-learning, nlp]
authors: [Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin]
year: 2017
venue: NIPS 2017
url: https://arxiv.org/abs/1706.03762
citations: [bahdanau2014attention, cho2014learning, hochreiter1997long, kingma2014adam]
---

# Attention Is All You Need

## Core Thesis

The paper proposes the **Transformer**, a novel neural sequence transduction architecture based entirely on attention mechanisms, eliminating the need for recurrence and convolution. The Transformer achieves state-of-the-art translation quality on WMT 2014 English-German and English-French tasks while being significantly more parallelizable and faster to train than previous recurrent or convolutional approaches. The architecture demonstrates that attention mechanisms alone can effectively model long-range dependencies without the sequential computation constraints of RNNs.

## Key Findings & Methodology

### Architecture Innovation
- **Multi-Head Self-Attention**: Instead of a single attention function with $d_{model}$-dimensional keys/values/queries, uses $h=8$ parallel attention heads with reduced dimensions ($d_k = d_v = d_{model}/h = 64$)
- **Transformer Stack**: 6 identical encoder layers and 6 identical decoder layers, each containing:
  - Multi-head self-attention sub-layer
  - Position-wise feed-forward network (FFN) with two linear transformations and ReLU
  - Residual connections around each sub-layer + layer normalization
- **Scaled Dot-Product Attention**: Attention mechanism that computes $\text{Attention}(Q,K,V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$
  - Scaling by $\frac{1}{\sqrt{d_k}}$ prevents dot products from becoming too large for large $d_k$ values

### Positional Encoding
- Uses sine and cosine functions of different frequencies instead of learned embeddings
- Formula: $PE_{(pos,2i)} = \sin(pos/10000^{2i/d_{model}})$ and $PE_{(pos,2i+1)} = \cos(pos/10000^{2i/d_{model}})$
- Allows the model to learn relative position relationships and extrapolate to longer sequences

### Advantages of Self-Attention
- **Computational Complexity**: $O(n^2 \cdot d)$ per layer vs $O(n \cdot d^2)$ for recurrence
- **Sequential Operations**: $O(1)$ constant operations vs $O(n)$ for RNNs, enabling massive parallelization
- **Maximum Path Length**: $O(1)$ connecting all positions vs $O(n)$ for recurrence, improving long-range dependency learning
- **Interpretability**: Individual attention heads learn different syntactic and semantic tasks

### Training Details
- **Dataset**: WMT 2014 English-German (4.5M sentence pairs) and English-French (36M sentences)
- **Optimization**: Adam optimizer with learning rate warmup strategy over 4000 steps
- **Regularization**: Residual dropout ($P_{drop}=0.1$), label smoothing ($\epsilon_{ls}=0.1$)
- **Hardware**: 8 NVIDIA P100 GPUs
- **Base Model**: 100,000 training steps (~12 hours)
- **Big Model**: 300,000 training steps (3.5 days)

### Empirical Results
- **English-to-German**: BLEU score of 28.4 (base model: 27.3), outperforming previous ensemble results by >2.0 BLEU
- **English-to-French**: BLEU score of 41.8 (base model: 38.1), state-of-the-art with <1/4 the training cost of previous best
- **English Constituency Parsing**: Generalizes successfully achieving 92.7 F1 with semi-supervised training (competitive with specialized models)
- Training cost: 10-100x reduction compared to recurrent/convolutional baselines

### Ablation Studies (Table 3)
- Reducing number of attention heads or head dimension hurts performance
- Increasing model capacity (larger $d_{ff}$, more layers) improves results
- Dropout crucial for regularization; label smoothing helps accuracy
- Learned positional embeddings produce nearly identical results to sinusoidal encoding

## Key Technical Contributions
- **Multi-head attention** mechanism for learning diverse representation subspaces
- **Encoder-decoder attention** allowing decoder to attend over all input positions
- **Masked self-attention** in decoder to preserve auto-regressive property
- **Position-wise feed-forward networks** with configurable inner dimensions ($d_{ff}=2048$ for base)
- **Efficient attention implementation** using highly optimized matrix multiplication

## Connections & Wikilinks

### Related Concepts
- [[Self-Attention]]: Core mechanism replacing recurrence
- [[Sequence-to-Sequence Models]]: Encoder-decoder architecture foundation
- [[Neural Machine Translation]]: Primary application domain
- [[Attention Mechanisms]]: Foundational concept (from [[Bahdanau Attention]], 2014)
- [[RNNs]] and [[LSTMs]]: Previous state-of-the-art architectures being replaced
- [[Positional Encoding]]: Novel approach to injecting sequence order information
- [[Layer Normalization]]: Stabilization technique in residual connections
- [[Residual Networks]]: Skip connections enabling deep networks

### Downstream Applications
- Foundation for [[BERT]], [[GPT]] and modern language models
- Basis for state-of-the-art results in [[Natural Language Processing]]
- Enables [[Vision Transformers]] when adapted to image domains
- Fundamental to modern [[Multimodal Learning]] architectures

### Comparison with Previous Approaches
- **Advantage over [[Recurrent Neural Networks|RNNs]]**: O(1) vs O(n) sequential operations, better parallelization
- **Advantage over [[Convolutional Neural Networks|CNNs]]**: O(1) vs O(log_k(n)) path length for long-range dependencies
- **Trade-off**: O(n²·d) complexity in sequence length (but acceptable for most NLP tasks where n << d)

## Original Implementation
Code available at: https://github.com/tensorflow/tensor2tensor

## Citation
Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30.
