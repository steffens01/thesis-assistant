---
tags: [attention, mechanism, neural-networks]
related: [Transformer, Attention Mechanisms, Self-Attention]
---

# Multi-Head Attention

An attention mechanism that applies multiple parallel attention functions instead of using a single attention head. This allows the model to jointly attend to information from different representation subspaces.

## Mechanism
Instead of computing a single attention function with $d_{model}$-dimensional keys, values, and queries:

1. Linearly project queries, keys, and values $h$ times with different learned projections to dimensions $d_k$, $d_k$, and $d_v$
2. Perform attention function in parallel on each projection: $h$ different attention outputs
3. Concatenate all outputs and project again to final $d_{model}$ dimensions

$$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1,...,\text{head}_h)W^O$$

where $\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$

## Benefits
- **Representation Diversity**: Each head can learn to attend to different aspects of the input (syntactic, semantic, positional patterns)
- **Computational Efficiency**: With $h=8$ heads and $d_k = d_v = d_{model}/h = 64$, total cost is similar to single-head attention
- **Improved Performance**: Single-head attention underperforms by ~0.9 BLEU in machine translation tasks
- **Interpretability**: Individual attention heads exhibit behaviors related to syntactic and semantic structure

## Typical Configuration
- Number of heads: $h = 8$
- Dimension per head: $d_k = d_v = 512/8 = 64$
- Projection matrices: 
  - $W_i^Q, W_i^K \in \mathbb{R}^{d_{model} \times d_k}$
  - $W_i^V \in \mathbb{R}^{d_{model} \times d_v}$
  - $W^O \in \mathbb{R}^{hd_v \times d_{model}}$

## Alternatives Not Used
- Single attention head: Worse performance (lower BLEU scores)
- Too many heads (e.g., 16, 32): Diminishing returns or degradation

## Application in Transformers
Used in three ways:
1. **Encoder self-attention**: Keys, values, queries all from encoder layer
2. **Decoder self-attention**: Keys, values, queries all from decoder layer (with masking)
3. **Encoder-decoder attention**: Queries from decoder, keys/values from encoder
