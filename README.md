Notes for [Fine-Tuning LLMs Course](https://maven.com/parlance-labs/fine-tuning)



### Observations on `chat_template` Behavior

| chat_template        | Stopping Behavior                | Privacy Message       | Hallucinations | Notes                       |
|----------------------|----------------------------------|-----------------------|----------------|-----------------------------|
| **Alpaca**           | Did not stop after answer        | No                    | Yes            |                             |
| **Tokenizer Default**| Stopped appropriately            | Yes                   | Yes            |                             |
| **Phi-3**            | Similar to Tokenizer Default     | Yes                   | Yes            |                             |

---

### Useful Resources

- **Injecting New Knowledge into an LLM via Fine-Tuning with ORPO**  
    [Read on Medium](https://medium.com/@celsoaf/injecting-new-knowledge-into-an-llm-via-fine-tuning-with-orpo-017d3bfdb11b)  
    Sample data: `sample_data/data_from_medium_example.json`

---

### RAG vs Fine-Tuning

- [Knowledge Injection in LLMs: Fine-Tuning and RAG](https://zilliz.com/blog/knowledge-injection-in-llms-fine-tuning-and-rag)
- https://aclanthology.org/2024.emnlp-main.15.pdf
- **Summary:** RAG is generally considered better for knowledge injection.


### Other techniques/reading
 - [Language Model Steering] (https://github.com/zjunlp/EasyEdit/tree/main)
 - Editing specific memory [MEMIT] (https://github.com/kmeng01/memit)



### LORA hyper parameter guide
 - https://docs.unsloth.ai/get-started/fine-tuning-guide/lora-hyperparameters-guide



### Hyperparameter Rules

- **chat_template** and **data_type**:
    all chat templates - (https://github.com/axolotl-ai-cloud/axolotl/blob/main/src/axolotl/utils/chat_templates.py)
    1. When using `alpaca`, `completion`, or `input_output`, the `chat_template` key should be absent.
    2. If using another `chat_template` tailored for a specific LLM, clearly define the data type and structure.

- OOM error:
    1. Reduce micro_batch_size and increase gradient_accumulation_steps by same factor to keep effective batch size same
        ex. micro_batch_size : 16 , gradient_accumulation_steps: 4 --> micro_batch_size : 2 , gradient_accumulation_steps: 32 = Effective batch size is 64 in both cases


Try using - llama and qwen


build eval and evaluate llama, qwen and mistral

build a proper roadmap on how to finetune a model given a use case.