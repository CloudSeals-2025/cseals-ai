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

## Multi-Cloud Cost Optimizer Template

The file `cost_optimizer_template.py` provides a starting point for building a multi-cloud cost optimization service that complies with the ethical AI pillars. It demonstrates:

- Secure API access using environment variables for credentials
- An approval workflow hook before applying recommendations
- Integration with `ethical_ai.py` to compute fairness, transparency, privacy, accountability and reliability scores
- Exporting an ethical compliance dashboard in JSON format

Run the example workflow to generate a dashboard:

```bash
python cost_optimizer_template.py
```
