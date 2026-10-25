import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AML Robocop",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AML Robocop")
st.subheader("Transaction Monitoring & Account Investigation")

st.warning(
    "Educational prototype only. Scores are based on demo rules. "
    "Alerts do not prove money laundering."
)

st.sidebar.header("Detection Settings")

amount_limit = st.sidebar.number_input(
    "Individual amount threshold (₹)",
    min_value=1000,
    value=100000,
    step=10000
)

repeat_limit = st.sidebar.number_input(
    "Transactions per account to flag",
    min_value=2,
    value=3,
    step=1
)

total_limit = st.sidebar.number_input(
    "Combined account amount threshold (₹)",
    min_value=1000,
    value=100000,
    step=10000
)

uploaded_file = st.file_uploader(
    "Upload transaction CSV",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        required = ["Transaction ID", "Amount", "Account ID"]
        missing = [col for col in required if col not in df.columns]

        if missing:
            st.error("Missing CSV columns: " + ", ".join(missing))

        else:
            df["Amount"] = pd.to_numeric(
                df["Amount"], errors="coerce"
            )
            df["Account ID"] = (
                df["Account ID"].astype("string").str.strip()
            )

            df = df.dropna(
                subset=["Amount", "Account ID", "Transaction ID"]
            ).copy()

            df = df[
                (df["Amount"] >= 0)
                & (df["Account ID"] != "")
            ].copy()

            if df.empty:
                st.warning("No valid transactions found.")

            else:
                stats = df.groupby("Account ID").agg(
                    Account_Count=("Transaction ID", "count"),
                    Account_Total=("Amount", "sum")
                )

                df["Account Transaction Count"] = (
                    df["Account ID"].map(stats["Account_Count"])
                )
                df["Account Total Amount"] = (
                    df["Account ID"].map(stats["Account_Total"])
                )

                df["Amount Points"] = (
                    df["Amount"] >= amount_limit
                ).astype(int) * 50

                df["Frequency Points"] = (
                    df["Account Transaction Count"] >= repeat_limit
                ).astype(int) * 30

                df["Combined Amount Points"] = (
                    df["Account Total Amount"] >= total_limit
                ).astype(int) * 20

                df["Risk Score"] = (
                    df["Amount Points"]
                    + df["Frequency Points"]
                    + df["Combined Amount Points"]
                )

                df["Risk Level"] = df["Risk Score"].apply(
                    lambda score:
                    "High" if score >= 50
                    else "Medium" if score >= 30
                    else "Low"
                )

                def explain(row):
                    reasons = []
                    if row["Amount Points"] > 0:
                        reasons.append("High individual amount")
                    if row["Frequency Points"] > 0:
                        reasons.append("Repeated account activity")
                    if row["Combined Amount Points"] > 0:
                        reasons.append("Combined account amount meets threshold")
                    return "; ".join(reasons) or "No demo rule triggered"

                df["Review Reason"] = df.apply(explain, axis=1)

                account_report = (
                    df.groupby("Account ID")
                    .agg(
                        Transaction_Count=("Transaction ID", "count"),
                        Total_Amount=("Amount", "sum"),
                        Highest_Transaction=("Amount", "max"),
                        Highest_Risk_Score=("Risk Score", "max")
                    )
                    .reset_index()
                )

                account_report["Review Status"] = account_report.apply(
                    lambda row:
                    "Review required"
                    if (
                        row["Transaction_Count"] >= repeat_limit
                        or row["Total_Amount"] >= total_limit
                        or row["Highest_Transaction"] >= amount_limit
                    )
                    else "No demo rule triggered",
                    axis=1
                )

                st.header("📊 Dashboard Summary")

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Transactions", len(df))
                c2.metric(
                    "High Risk",
                    int((df["Risk Level"] == "High").sum())
                )
                c3.metric(
                    "Medium Risk",
                    int((df["Risk Level"] == "Medium").sum())
                )
                c4.metric(
                    "Accounts for Review",
                    int(
                        (account_report["Review Status"]
                         == "Review required").sum()
                    )
                )

                st.divider()
                st.header("🔎 Transaction Records")
                st.dataframe(df, use_container_width=True)

                st.header("🕵️ Account Investigation Explorer")

                selected_account = st.selectbox(
                    "Select an account",
                    sorted(df["Account ID"].unique().tolist())
                )

                selected_df = df[
                    df["Account ID"] == selected_account
                ].copy()

                account_total = selected_df["Amount"].sum()
                transaction_count = len(selected_df)
                highest_score = selected_df["Risk Score"].max()

                a1, a2, a3 = st.columns(3)
                a1.metric("Selected Account", selected_account)
                a2.metric("Transaction Count", transaction_count)
                a3.metric("Total Transaction Amount", f"₹{account_total:,.0f}")

                st.write(
                    f"Highest demo risk score: **{highest_score}**"
                )

                st.subheader("Selected Account Transactions")
                st.dataframe(
                    selected_df[
                        [
                            "Transaction ID",
                            "Amount",
                            "Risk Score",
                            "Risk Level",
                            "Review Reason"
                        ]
                    ],
                    use_container_width=True
                )

                st.subheader("Selected Account Amount Chart")
                st.bar_chart(
                    selected_df.set_index("Transaction ID")["Amount"]
                )

                st.divider()
                st.header("📋 All Account Investigation Reports")
                st.dataframe(account_report, use_container_width=True)

                flagged = df[df["Risk Score"] > 0].copy()

                st.header("⬇️ Download Reports")

                st.download_button(
                    "Download All Risk Scores",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name="aml_risk_scores.csv",
                    mime="text/csv"
                )

                st.download_button(
                    "Download Account Report",
                    data=account_report.to_csv(index=False).encode("utf-8"),
                    file_name="aml_account_report.csv",
                    mime="text/csv"
                )

                st.download_button(
                    "Download Flagged Transactions",
                    data=flagged.to_csv(index=False).encode("utf-8"),
                    file_name="aml_flagged_transactions.csv",
                    mime="text/csv"
                )

                st.info(
                    "Demo scoring: amount threshold = 50 points; "
                    "repeated activity = 30 points; combined account "
                    "amount = 20 points. This is not a validated AML model."
                )

    except Exception as error:
        st.error(f"Could not analyze CSV: {error}")

else:
    st.info(
        "Upload a CSV containing Transaction ID, Amount, "
        "and Account ID columns."
    )