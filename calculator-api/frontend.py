import streamlit as st
# from streamlit_chat import message
import requests
import json

API_URL = "http://localhost:8000"  # Update with your API URL

st.set_page_config(page_title="Calculator API", page_icon=":calculator:", layout="wide")
st.title("Calculator API")
st.markdown("This is a simple calculator API that performs basic arithmetic operations: addition, subtraction, multiplication, and division.")
def calculate(num1, num2, operation):
    url = "http://localhost:8000/calculate"
    payload = {
        "num1": num1,
        "num2": num2,
        "operation": operation
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to perform calculation"}
def main():

    st.sidebar.title("Calculator API")
    st.sidebar.markdown("Use this calculator to perform basic arithmetic operations.")
    
    num1 = st.number_input("Enter first number", value=0)
    num2 = st.number_input("Enter second number", value=0)
    
    operation = st.selectbox(
        "Select operation",
        [("+", "Add"), ("-", "Subtract"), ("*", "Multiply"), ("/", "Divide")],
        format_func=lambda x: x[1]
    )
    
    if st.button("Calculate"):
        result = calculate(num1, num2, operation[0])  # Send the symbol, not the label
        if "result" in result:
            st.success(f"The result of {operation[1].lower()}ing {num1} and {num2} is: {result['result']}")
        else:
            st.error(result["error"])
if __name__ == "__main__":
    main()
    st.sidebar.markdown("### About")
    st.sidebar.markdown("This is a simple calculator API built with FastAPI and Streamlit. It allows you to perform basic arithmetic operations like addition, subtraction, multiplication, and division.")
    st.sidebar.markdown("### How to use")
    st.sidebar.markdown("1. Enter the first number.")
    st.sidebar.markdown("2. Enter the second number.")
    st.sidebar.markdown("3. Select the operation you want to perform.")
    st.sidebar.markdown("4. Click on the 'Calculate' button to see the result.")
    st.sidebar.markdown("### API Documentation")
    st.sidebar.markdown("You can find the API documentation [here](http://localhost:8000/docs).")