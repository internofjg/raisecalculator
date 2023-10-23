import streamlit as st
import numpy as np
import scipy.optimize

# Set the page title and layout
st.set_page_config(page_title="加碼計算機", page_icon=None, layout='centered', initial_sidebar_state='auto')

def add_lot_opt_sol(p0, x0, p1, final_return, p_exp, exp_return_loss_ratio):
    def f(x):
        x1 = x[0]  # ADD LOT
        p_final = x[1]  # WORST CASE
        r = p_final * (x0 + x1) - p0 * x0 - p1 * x1  # 利潤
        return_loss_ratio = (p_exp - p1) / (p_final - p1)
        return (r - (final_return / 1000)) ** 2 + (return_loss_ratio - exp_return_loss_ratio) ** 2

    sol = scipy.optimize.minimize(f, [0, 0])
    return sol

# Streamlit Title
st.title('JG說真的-加碼計算機')

# Information below title and above input fields
info_text = """
<div style="font-size: 16px; color: gray; font-style: italic; text-align: center;">
    <em>加碼計算機風險報酬比為1:3</em>
</div>
"""
st.markdown(info_text, unsafe_allow_html=True)

# Streamlit Input fields
cost_price = st.number_input("庫存成本價", value=0.0, step=0.1)
cost_amount = st.number_input("庫存張數", value=0, step=1)
add_price = st.number_input("想加碼價位", value=0.0, step=0.1)
expect_price = st.number_input("預期股價會上漲到多少", value=0.0, step=0.1)
exit_money = st.number_input("加碼後獲利回吐，至少保有多少獲利離場?", value=0.0, step=0.1)

#Statement
statement = """
<div style="font-size: 16px; color: red; font-style: italic; text-align: center;">
    <em>**聲明：本工具只供參考用途，並不構成任何投資的建議意見！**</em>
</div>
"""
st.markdown(statement, unsafe_allow_html=True)

# Calculate and display the results
if st.button('計算'):
    ans = add_lot_opt_sol(cost_price, cost_amount, add_price, exit_money, expect_price, -3)

    if ans.x[0] < 1:
        st.markdown("<span style='font-size: 20px; color: red; font-weight: bold;'>不建議加碼</span>", unsafe_allow_html=True)
    else:
        result_text = f"""
        <div style="font-size: 20px">
            若想在價格 {add_price} 塊加碼，
            建議加碼 <span style="color: red">{int(ans.x[0])}</span> 張, 
            出場價格 <span style="color: red">{ans.x[1]:.2f}</span> 塊
        </div>
        """
        st.markdown(result_text, unsafe_allow_html=True)
