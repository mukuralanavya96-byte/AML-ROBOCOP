import pandas as pd
import networkx as nx
from pathlib import Path


# ==========================================
# 1. LOAD TRANSACTION DATA
# ==========================================

BASE_DIR = Path(__file__).parent
FILE_PATH = BASE_DIR / "graph_transactions.csv"

print("\n🛡️ AML ROBOCOP - GRAPH INVESTIGATION")
print("=" * 50)

try:
    df = pd.read_csv(FILE_PATH)

    required_columns = [
        "Transaction ID",
        "Sender Account",
        "Receiver Account",
        "Amount",
        "Status"
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

    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="raise"
    )

    if df.empty:
        raise ValueError("Transaction file is empty.")

except FileNotFoundError:
    print("ERROR: graph_transactions.csv was not found.")
    raise SystemExit(1)

except Exception as error:
    print(f"ERROR loading transaction data: {error}")
    raise SystemExit(1)


# ==========================================
# 2. BUILD ACCOUNT RELATIONSHIP GRAPH
# ==========================================

graph = nx.DiGraph()

for _, row in df.iterrows():
    sender = str(row["Sender Account"]).strip()
    receiver = str(row["Receiver Account"]).strip()

    if not sender or not receiver:
        continue

    graph.add_edge(
        sender,
        receiver,
        amount=float(row["Amount"]),
        transaction_id=str(row["Transaction ID"]),
        status=str(row["Status"])
    )


# ==========================================
# 3. DISPLAY GRAPH SUMMARY
# ==========================================

print("\nGRAPH SUMMARY")
print("-" * 50)

print(f"Total accounts (nodes): {graph.number_of_nodes()}")
print(f"Total connections (edges): {graph.number_of_edges()}")
print(f"Transactions loaded: {len(df)}")


# ==========================================
# 4. DISPLAY TRANSACTION CONNECTIONS
# ==========================================

print("\nACCOUNT CONNECTIONS")
print("-" * 50)

for sender, receiver, details in graph.edges(data=True):
    print(
        f"{sender} -> {receiver} | "
        f"Amount: ₹{details['amount']:,.0f} | "
        f"Transaction: {details['transaction_id']} | "
        f"Status: {details['status']}"
    )


# ==========================================
# 5. ACCOUNT RELATIONSHIP SUMMARY
# ==========================================

print("\nACCOUNT RELATIONSHIP SUMMARY")
print("-" * 50)

for account in sorted(graph.nodes()):
    outgoing = list(graph.successors(account))
    incoming = list(graph.predecessors(account))

    print(f"\nAccount: {account}")
    print(f"  Sends to: {outgoing}")
    print(f"  Receives from: {incoming}")


# ==========================================
# 6. MULTI-STEP ACCOUNT INVESTIGATION
# ==========================================

print("\n" + "=" * 50)
print("MULTI-STEP ACCOUNT INVESTIGATION")
print("=" * 50)

selected_account = input(
    "\nEnter account to investigate (example A001): "
).strip()

if selected_account not in graph:
    print(
        f"Account '{selected_account}' was not found. "
        "Please check the account ID."
    )

else:
    reachable_accounts = nx.descendants(
        graph,
        selected_account
    )

    print(f"\nStarting account: {selected_account}")
    print(
        "Reachable downstream accounts: "
        f"{len(reachable_accounts)}"
    )

    if reachable_accounts:
        print("\nTransaction paths:")

        for account in sorted(reachable_accounts):
            path = nx.shortest_path(
                graph,
                source=selected_account,
                target=account
            )

            print(" -> ".join(path))

    else:
        print("No downstream accounts found.")


# ==========================================
# 7. INVESTIGATION DISCLAIMER
# ==========================================

print("\n" + "=" * 50)
print("INVESTIGATION NOTE")
print("=" * 50)

print(
    "This is an educational prototype using sample data."
)
print(
    "Account connections alone do not prove suspicious activity."
)
print(
    "Human review is required before making AML decisions."
)

print("\nGraph investigation completed.")