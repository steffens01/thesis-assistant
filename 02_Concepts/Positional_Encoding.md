---
tags: [positional-encoding, sequence-modeling, transformer]
related: [Transformer, Self-Attention, Sequence-to-Sequence Models]
---

# Positional Encoding

A method to inject information about the relative or absolute position of tokens into the [[Transformer]] architecture. Since the Transformer lacks recurrence and convolution, positional information must be explicitly provided.

## Key Challenge
- The [[Transformer]] applies the same attention and feed-forward operations at each position without sequential processing
- Without position information, the model would be permutation-invariant (treating input as an unordered set)
- Solution: Add positional encodings to input embeddings before the encoder/decoder stacks

## Sinusoidal Positional Encoding (Used in Transformers)

Position information is encoded using sine and cosine functions of different frequencies:

$$PE_{(\text{pos}, 2i)} = \sin\left(\frac{\text{pos}}{10000^{2i/d_{\text{model}}}}\right)$$

$$PE_{(\text{pos}, 2i+1)} = \cos\left(\frac{\text{pos}}{10000^{2i/d_{\text{model}}}}\right)$$

Where:
- $\text{pos}$ is the position in the sequence
- $i$ is the dimension index (0 to $d_{\text{model}}/2$)
- Wavelengths form geometric progression from $2\pi$ to $10000 \cdot 2\pi$

## Why Sinusoids?

### Theoretical Advantages
1. **Relative Position Learning**: For any fixed offset $k$, $PE_{\text{pos}+k}$ can be represented as a linear function of $PE_{\text{pos}}$
   - Allows model to learn to attend by relative positions naturally
2. **Extrapolation**: Can generalize to sequence lengths longer than those seen during training
   - Important for deployment on longer sequences than training data

### Mathematical Properties
- **Orthogonality**: Different dimensions encode different frequency components
- **Bounded values**: All PE values between -1 and 1, stable for learning
- **Smooth gradients**: Continuous functions enabling gradient-based optimization

## Alternative: Learned Positional Embeddings

The paper also experimented with learned positional embeddings (separate learnable vectors for each position):

$$PE_{\text{pos}} \in \mathbb{R}^{d_{\text{model}}} \text{ (learnable parameter)}$$

**Results**: Nearly identical performance to sinusoidal encoding (Table 3, row E)
- Sinusoid version preferred because it extrapolates better
- Learned embeddings would need pre-computed embeddings for any sequence length

## Practical Implementation

1. Compute $PE$ matrix of shape $(seq\_length, d_{\text{model}})$
2. Add to input embeddings: $\text{embedding}(x) + PE$
3. Applied identically at both encoder and decoder input layers
4. Embeddings scaled by $\sqrt{d_{\text{model}}}$ before adding to positional encodings

## Impact on Model Performance

- **Critical for Transformer**: Ablation studies show position information is essential
- **Stable across architectures**: Effective whether applied at input or learned per layer
- **Enables sequence understanding**: Allows self-attention to distinguish between positions and learn sequential relationships

## Modern Developments

Variants developed for specific applications:
- **Rotary Positional Embeddings (RoPE)**: Uses complex number rotations for better extrapolation
- **Relative Position Biases**: Applied directly to attention logits
- **ALiBi (Attention with Linear Biases)**: No learned positions, uses linear position biases
- **Flash Attention**: Integration with attention implementation optimizations
