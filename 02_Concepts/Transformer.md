---
tags: [architecture, attention, deep-learning]
related: [Self-Attention, Multi-Head Attention, Attention Mechanisms]
---

# Transformer

A neural network architecture for sequence-to-sequence tasks that replaces recurrent and convolutional layers entirely with attention mechanisms. The Transformer consists of an encoder-decoder structure where:

- **Encoder**: Stack of 6 identical layers, each with multi-head self-attention and feed-forward networks
- **Decoder**: Stack of 6 identical layers, each with multi-head self-attention, encoder-decoder attention, and feed-forward networks
- **Core Innovation**: Complete elimination of recurrence and convolution in favor of [[Self-Attention]] mechanisms

## Key Properties
- **Parallelizability**: O(1) sequential operations vs O(n) for RNNs, enabling massive training speedup
- **Computational Complexity**: O(n² · d) per layer; favorable when sequence length n < representation dimension d
- **Long-range Dependencies**: Constant path length between any two positions improves learning
- **Interpretability**: Attention weights can be visualized to understand model decisions

## Architecture Components
1. **Embedding & Positional Encoding**: Learned token embeddings + sinusoidal positional encodings
2. **Multi-Head Self-Attention Layers**: 8 parallel attention heads with reduced dimensions
3. **Feed-Forward Networks**: Position-wise MLPs with two linear transformations and ReLU activation
4. **Residual Connections & Layer Normalization**: LayerNorm(x + Sublayer(x)) around each sub-layer

## Impact
Introduced in [[Vaswani_2017_Attention_is_All_You_Need]], the Transformer achieved state-of-the-art results on machine translation tasks and became the foundation for modern language models including [[BERT]], [[GPT]], and others. The architecture has proven effective across NLP, vision, and multimodal tasks.

## Training Details
- Requires careful initialization, warm-up learning rate schedules, and dropout regularization
- Base configuration: 6 layers, d_model=512, 8 attention heads
- Big configuration: 6 layers, d_model=1024, 16 attention heads
- Trains significantly faster than RNN-based approaches (12 hours for base, 3.5 days for big on 8 P100 GPUs)
