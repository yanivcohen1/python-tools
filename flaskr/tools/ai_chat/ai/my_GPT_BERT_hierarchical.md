my GPT hierarchical breakdown of the blocks:

```
BertForQuestionAnsweringWithReasoning
├── bert: BertModelCustom
│   ├── embeddings: BertEmbeddings
│   │   ├── word_embeddings: Embedding
│   │   ├── position_embeddings: Embedding
│   │   ├── token_type_embeddings: Embedding
│   │   ├── LayerNorm: LayerNorm
│   │   └── dropout: dropout
│   ├── encoder: BertEncoder
│   │   └── layers: ModuleList [12 x BertLayer]
│   │       └── BertLayer (repeated 12 times)
│   │           ├── attention: BertAttention
│   │           │   ├── self: BertSelfAttention
│   │           │   │   ├── query: linear
│   │           │   │   ├── key: linear
│   │           │   │   ├── value: linear
│   │           │   │   └── dropout: Dropout
│   │           │   └── output: BertSelfOutput
│   │           │       ├── dense: linear
│   │           │       ├── LayerNorm: LayerNorm
│   │           │       └── dropout: Dropout
│   │           ├── intermediate: BertIntermediate
│   │           │   ├── dense: linear
│   │           │   └── intermediate_act_fn: nn.GELU(dense(hidden_states))
│   │           └── output: BertOutput
│   │               ├── dense: linear
│   │               ├── LayerNorm: LayerNorm
│   │               └── dropout: Dropout
│   └── pooler: BertPooler
│       ├── dense: linear
│       └── activation: nn.Tanh(dense(cls_token))
├── qa_outputs: linear_layer (768-in, 2-out)
└── reasoning_output: linear_layer (768-in, 3-out)
```
