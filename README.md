# cseals-ai
CloudSeals AI Agents

## Ethical AI Evaluation

This repository includes an example Python script `ethical_ai.py` that demonstrates how to score key ethical AI pillars and generate a simple bias report:

- **Fairness** – uses statistical parity difference and disparate impact ratio
- **Transparency** – whether a model exposes an `explain` method
- **Privacy** – checks if the dataset contains obvious personal identifiers
- **Accountability** – number of logged events
- **Reliability** – mean absolute error of predictions

Run the script to see example scores:

```bash
python ethical_ai.py --dataset path/to/data.jsonl --bias-report bias.json
```
