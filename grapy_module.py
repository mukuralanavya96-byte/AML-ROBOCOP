from pathlib import Path

import networkx as nx
import pandas as pd


BASE_DIR = Path(__file__).parent
FILE_PATH = BASE_DIR / "graph_transactions.csv"


def load_transaction_graph():
    """Load sample transactions and build an account relationship graph."""

    if not FILE_PATH.exists():
        raise FileNotFoundError(
            "graph_transactions.csv was not found."
        )

    df = pd.read_csv(FILE_PATH)

    required_columns = [
        "Transaction ID",
        "Sender Account",
        "Receiver Account",
        "Amount",
        "Status",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing columns: " + ", ".join(missing_columns)
        )

    if df.empty:
        raise ValueError("The transaction file is empty.")

    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="raise",
    )

    graph = nx.DiGraph()

    for _, row in df.iterrows():
        sender = str(row["Sender Account"]).strip()
        receiver = str(row["Receiver Account"]).strip()

        if not sender or not receiver:
            continue

        # Store each transaction's details on the connection.
        # For repeated connections, retain all transactions.
        if graph.has_edge(sender, receiver):
            graph[sender][receiver]["transactions"].append({
                "transaction_id": str(row["Transaction ID"]),
                "amount": float(row["Amount"]),
                "status": str(row["Status"]),
            })
        else:
            graph.add_edge(
                sender,
                receiver,
                transactions=[{
                    "transaction_id": str(row["Transaction ID"]),
                    "amount": float(row["Amount"]),
                    "status": str(row["Status"]),
                }],
            )

    return df, graph


def get_account_summary(graph, account_id):
    """Return the connections and downstream accounts for an account."""

    if account_id not in graph:
        return None

    incoming = list(graph.predecessors(account_id))
    outgoing = list(graph.successors(account_id))
    downstream = sorted(nx.descendants(graph, account_id))

    return {
        "account": account_id,
        "incoming": incoming,
        "outgoing": outgoing,
        "downstream": downstream,
    }


def get_transaction_connections(graph):
    """Return transaction-level details for every account connection."""

    rows = []

    for sender, receiver, details in graph.edges(data=True):
        for transaction in details["transactions"]:
            rows.append({
                "Sender Account": sender,
                "Receiver Account": receiver,
                "Transaction ID": transaction["transaction_id"],
                "Amount": transaction["amount"],
                "Status": transaction["status"],
            })

    return pd.DataFrame(rows)