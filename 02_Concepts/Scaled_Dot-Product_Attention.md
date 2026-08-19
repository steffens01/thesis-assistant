---
tags: [attention, mechanism, sequence-modeling]
related: [Multi-Head Attention, Transformer, Attention Mechanisms]
---

# Scaled Dot-Product Attention

The core attention mechanism used in the [[Transformer]] architecture. It computes attention as a weighted sum of values, where weights are determined by the compatibility between queries and keys.

## Mathematical Definition

$$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Where:
- $Q$ (Query): $n \times d_k$ matrix of query vectors
- $K$ (Key): $m \times d_k$ matrix of key vectors  
- $V$ (Value): $m \times d_v$ matrix of value vectors
- $d_k$: Dimension of keys
- Output: $n \times d_v$ matrix of attention outputs

## Scaling Factor
The critical innovation is dividing by $\sqrt{d_k}$:

**Problem**: For large $d_k$, dot products $q \cdot k$ can grow very large, pushing the softmax into regions with extremely small gradients, making training difficult.

**Solution**: Scale by $\frac{1}{\sqrt{d_k}}$ where variance of $q \cdot k$ is $d_k$ when components are independent with mean 0 and variance 1.

**Result**: Normalized attention weights with better gradient flow during training.

## Comparison with Alternatives

### Additive Attention (Bahdanau Attention)
- Uses feed-forward network with single hidden layer: $\text{score}(s_t, h_i) = v^T \tanh(W_s[s_t; h_i])$
- **Similar theoretical complexity** to dot-product attention
- **Slower in practice** due to feed-forward computation (cannot use optimized matrix multiplication)
- **Better performance** for small $d_k$ values

### Dot-Product Attention (without scaling)
- Identical to Scaled Dot-Product Attention but omits the $\frac{1}{\sqrt{d_k}}$ scaling
- **Much faster and more space-efficient** than additive attention (leverages optimized matrix ops)
- **Underperforms** for large $d_k$ due to gradient flow issues

## Practical Details in Transformers
- Applied in [[Multi-Head Attention]] separately for each of the 8 parallel heads
- In decoder self-attention: masked by setting illegal connections to $-\infty$ before softmax (preserves auto-regressive property)
- In encoder-decoder attention: queries from decoder, keys/values from encoder
- Computational complexity: $O(n^2 \cdot d_k)$ for sequence length $n$, constant path length between positions

## Impact
Scaled Dot-Product Attention became the standard attention mechanism in modern deep learning due to:
1. Computational efficiency
2. Gradient stability
3. Effectiveness across diverse sequence modeling tasks
4. Foundation for all subsequent Transformer-based models ([[BERT]], [[GPT]], Vision Transformers, etc.)
