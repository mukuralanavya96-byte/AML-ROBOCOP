AML Robocop 🛡️

An educational Anti-Money Laundering (AML) prototype for transaction monitoring, risk analysis, account investigation, and AI-powered policy assistance.

🚀 Features

- Transaction Monitoring: Analyze transaction data using configurable rules.
- Risk Scoring: Identify transactions that require further review.
- Account Investigation: Explore account activity and transaction connections.
- Graph Analysis: Investigate relationships between accounts.
- AI Policy Assistant: Use a local Ollama language model to explain relevant AML policy information.
- Report Downloads: Export risk scores, account reports, and flagged transactions as CSV files.
- Interactive Dashboard: Explore results through a Streamlit interface.

🛠️ Technologies

- Python
- Streamlit
- Pandas
- NetworkX
- Scikit-learn
- Ollama
- Llama 3.2

💻 Getting Started

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd AML-ROBOCOP

Replace "YOUR_GITHUB_REPOSITORY_URL" with this repository's HTTPS URL.

2. Install dependencies

python -m pip install streamlit pandas networkx scikit-learn ollama

3. Install and start Ollama

Install Ollama from https://ollama.com and download the model:

ollama pull llama3.2:3b

4. Run the dashboard

streamlit run dashboard.py

📂 Project Structure

- "dashboard.py" — Main Streamlit dashboard
- "graph_builder.py" — Transaction graph analysis
- "graph_module.py" — Account connection utilities
- "rag_module.py" — Local AI policy retrieval and response
- "aml_policy.txt" — Example AML policy text
- "graph_transactions.csv" — Example graph transaction data

⚠️ Disclaimer

This is an educational prototype, not a production AML compliance system. Risk scores and alerts are indicators for further investigation, not proof of money laundering. Human review is required.

📄 License

Add a license file if you intend to distribute this project under an open-source license.
