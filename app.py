import streamlit as st
import pandas as pd
import re

# Load the Excel data (simulated here, replace with actual file if needed)
df = pd.read_excel("Untitled spreadsheet (2).xlsx", sheet_name="Sheet1")

st.title("Business Rule Engine for Loan Eligibility")

st.header("1. User Input Parameters")

# Extract parameters
parameters = df['Parameters']
user_inputs = {}

# User Input Form
with st.form("eligibility_form"):
    for param in parameters:
        user_inputs[param] = st.text_input(f"Enter value for {param}")
    submitted = st.form_submit_button("Check Eligibility")

# Prepare lender rule map
lenders = df.columns[2:]  # skip Parameters and Gating Criteria
rules_map = {}
for lender in lenders:
    rules_map[lender] = df[lender].tolist()

# Evaluation logic
def evaluate(user_val, rule):
    try:
        if pd.isna(rule):
            return True
        match = re.match(r"(>=|>|<=|<|==)?(\d+)", str(rule))
        if match:
            op, threshold = match.groups()
            threshold = int(threshold)
            user_val = int(user_val)
            if op == ">=": return user_val >= threshold
            elif op == ">": return user_val > threshold
            elif op == "<=": return user_val <= threshold
            elif op == "<": return user_val < threshold
            elif op == "==": return user_val == threshold
    except:
        return False
    return False

# Display eligible lenders
if submitted:
    st.subheader("Eligible Lenders")
    eligible_lenders = []
    for lender in lenders:
        all_pass = True
        for i, param in enumerate(parameters):
            if not evaluate(user_inputs[param], rules_map[lender][i]):
                all_pass = False
                break
        if all_pass:
            eligible_lenders.append(lender)
    
    if eligible_lenders:
        st.success(", ".join(eligible_lenders))
    else:
        st.error("No lender matched your criteria.")

st.header("Lender Rules")

# Editable DataFrame
editable_df = df.copy()
edited = st.data_editor(editable_df)

if st.button("Save Changes"):
    edited.to_excel("updated_lender_rules.xlsx", index=False)
    st.success("Rules updated and saved to 'updated_lender_rules.xlsx'")

