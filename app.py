import streamlit as st
import plotly.express as px
import pandas as pd
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from calculations import calculate_salary, calculate_tax_breakdown
from database import create_database, save_employee, get_employees


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="SmartPay | Payroll Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

create_database()


# ---------------------------------------------------------
# CUSTOM DESIGN
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #0b1020;
        --panel: #121a2b;
        --panel-soft: #172238;
        --border: rgba(148, 163, 184, 0.16);
        --muted: #9aa9bd;
        --text: #edf3fc;
        --blue: #6ea8fe;
        --green: #42d6a4;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 12% 0%, rgba(37, 99, 235, 0.16), transparent 34%),
            radial-gradient(ellipse at 90% 8%, rgba(16, 185, 129, 0.08), transparent 28%),
            var(--bg);
        color: var(--text);
    }

    .block-container {
        max-width: 1320px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4 {
        font-family: 'Manrope', sans-serif !important;
        color: var(--text) !important;
        letter-spacing: -0.025em;
    }

    p, label, .stMarkdown, .stCaption {
        color: #d5deeb;
    }

    [data-testid="stHeader"] {
        background: rgba(11, 16, 32, 0.75);
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #17243a, #111a2b);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px 20px;
        min-height: 116px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.12);
    }

    [data-testid="stMetricLabel"] {
        color: #a9b8cc !important;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #f4f8ff !important;
        font-family: 'Manrope', sans-serif;
        font-weight: 800;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--border) !important;
        border-radius: 18px !important;
        background: rgba(18, 26, 43, 0.72);
    }

    div.stButton > button, div.stDownloadButton > button {
        border: 1px solid rgba(110, 168, 254, 0.35);
        border-radius: 11px;
        min-height: 44px;
        font-weight: 700;
        color: white;
        background: linear-gradient(110deg, #2563eb, #397ee8);
        transition: all 0.2s ease;
    }

    div.stButton > button:hover, div.stDownloadButton > button:hover {
        border-color: #93c5fd;
        background: linear-gradient(110deg, #1d4ed8, #2563eb);
        transform: translateY(-1px);
    }

    input, textarea {
        border-radius: 10px !important;
    }

    [data-baseweb="input"], [data-baseweb="select"] {
        background: #111b2d !important;
        border-radius: 10px !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 13px;
        overflow: hidden;
    }

    hr {
        border-color: var(--border);
    }

    .hero {
        padding: 28px 30px;
        border: 1px solid rgba(125, 163, 220, 0.22);
        border-radius: 22px;
        background: linear-gradient(115deg, rgba(30, 58, 104, 0.72), rgba(17, 27, 46, 0.92) 58%, rgba(16, 70, 68, 0.48));
        box-shadow: 0 18px 45px rgba(0,0,0,0.18);
        margin-bottom: 24px;
    }

    .hero-kicker {
        color: #9fc4ff;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .hero-title {
        color: #f7faff;
        font-family: 'Manrope', sans-serif;
        font-size: clamp(2rem, 4vw, 3rem);
        line-height: 1.12;
        font-weight: 800;
        letter-spacing: -0.05em;
        margin: 0;
    }

    .hero-copy {
        color: #c0cde0;
        margin-top: 10px;
        font-size: 1rem;
    }

    .section-kicker {
        color: #8db8ff;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .section-title {
        font-family: 'Manrope', sans-serif;
        color: #f1f6ff;
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 3px;
    }

    .section-copy {
        color: #9aa9bd;
        font-size: 0.9rem;
        margin-bottom: 16px;
    }

    .net-banner {
        padding: 20px 22px;
        border: 1px solid rgba(66, 214, 164, 0.3);
        border-radius: 16px;
        background: linear-gradient(110deg, rgba(16, 185, 129, 0.14), rgba(18, 26, 43, 0.82));
    }

    .net-label {
        color: #9debd0;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .net-value {
        color: #71e4bd;
        font-family: 'Manrope', sans-serif;
        font-size: clamp(1.8rem, 3vw, 2.5rem);
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-top: 3px;
    }

    .net-note {
        color: #b6c9c7;
        font-size: 0.84rem;
        margin-top: 3px;
    }

    .tiny-note {
        color: #93a4bb;
        font-size: 0.78rem;
    }

    .footer {
        color: #74849b;
        text-align: center;
        font-size: 0.78rem;
        padding-top: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# PDF PAYSLIP GENERATOR
# ---------------------------------------------------------
def generate_payslip_pdf(name, emp_id, result):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "SmartPayTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#2563EB"),
        alignment=TA_CENTER,
        fontSize=24,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        textColor=colors.grey,
    )

    elements = [
        Paragraph("SMARTPAY", title_style),
        Paragraph("EMPLOYEE SALARY STATEMENT", subtitle_style),
        Spacer(1, 25),
    ]

    employee_data = [
        ["Employee Name", name],
        ["Employee ID", emp_id],
        ["Monthly Gross Salary", f"Rs. {result['monthly_gross']:,.2f}"],
        ["Annual Gross Salary", f"Rs. {result['annual_gross']:,.2f}"],
    ]

    employee_table = Table(employee_data, colWidths=[200, 280])
    employee_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#DBEAFE")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1E3A8A")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("PADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    elements.extend([employee_table, Spacer(1, 25)])

    elements.append(Paragraph("SALARY DEDUCTION BREAKDOWN", styles["Heading2"]))

    salary_data = [
        ["Description", "Amount (INR)"],
        ["Income Tax", f"{result['monthly_tax']:,.2f}"],
        ["Provident Fund (12%)", f"{result['pf']:,.2f}"],
        ["Health Insurance (2%)", f"{result['insurance']:,.2f}"],
        ["Total Deductions", f"{result['total_deductions']:,.2f}"],
        ["NET TAKE-HOME SALARY", f"{result['monthly_net']:,.2f}"],
    ]

    salary_table = Table(salary_data, colWidths=[300, 180])
    salary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#DCFCE7")),
                ("TEXTCOLOR", (0, -1), (-1, -1), colors.HexColor("#166534")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("PADDING", (0, 0), (-1, -1), 11),
            ]
        )
    )

    elements.extend(
        [
            salary_table,
            Spacer(1, 30),
            Paragraph(
                "Generated by SmartPay Employee Payroll System",
                subtitle_style,
            ),
        ]
    )

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Payroll management workspace</div>
        <div class="hero-title">SmartPay<span style="color:#78aaff">.</span></div>
        <div class="hero-copy">
            Employee Salary &amp; Tax Management System
            <br>Calculate salaries, understand deductions and generate clear payslips.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# EMPLOYEE INPUT
# ---------------------------------------------------------
st.markdown(
    """
    <div class="section-kicker">01 / Employee details</div>
    <div class="section-title">Create a salary calculation</div>
    <div class="section-copy">Enter the employee information and monthly gross salary to get started.</div>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    input_col1, input_col2 = st.columns(2)

    with input_col1:
        employee_name = st.text_input(
            "Employee name",
            placeholder="e.g. Alex Johnson",
            key="employee_name_input",
        )

    with input_col2:
        employee_id = st.text_input(
            "Employee ID",
            placeholder="e.g. EMP001",
            key="employee_id_input",
        )

    monthly_salary = st.number_input(
        "Monthly gross salary (₹)",
        min_value=1.0,
        value=60000.0,
        step=1000.0,
        key="monthly_salary_input",
    )

    calculate_clicked = st.button(
        "Calculate salary  →",
        type="primary",
        use_container_width=True,
    )

if calculate_clicked:
    if not employee_name.strip() or not employee_id.strip():
        st.error("Please enter both the employee name and employee ID.")
    else:
        try:
            result = calculate_salary(monthly_salary)
            saved = save_employee(
                employee_name.strip(),
                employee_id.strip(),
                monthly_salary,
                result["monthly_net"],
            )

            st.session_state["smartpay_result"] = result
            st.session_state["smartpay_employee_name"] = employee_name.strip()
            st.session_state["smartpay_employee_id"] = employee_id.strip()
            st.session_state["smartpay_saved"] = saved
        except ValueError as error:
            st.error(str(error))


# ---------------------------------------------------------
# RESULTS - KEPT IN SESSION STATE SO THEY REMAIN VISIBLE
# ---------------------------------------------------------
result = st.session_state.get("smartpay_result")

if result:
    current_name = st.session_state["smartpay_employee_name"]
    current_id = st.session_state["smartpay_employee_id"]

    st.divider()
    st.markdown(
        """
        <div class="section-kicker">02 / Calculation overview</div>
        <div class="section-title">Salary at a glance</div>
        <div class="section-copy">A complete view of the employee's monthly payroll calculation.</div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(f"Employee: **{current_name}**  ·  Employee ID: **{current_id}**")

    if st.session_state.get("smartpay_saved"):
        st.success("Employee record saved successfully.")
    else:
        st.warning("This Employee ID already exists. The calculation is shown, but the record was not saved again.")

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="net-banner">
                <div class="net-label">Monthly take-home salary</div>
                <div class="net-value">₹{result['monthly_net']:,.2f}</div>
                <div class="net-note">Your estimated monthly salary after the configured deductions.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")
        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Monthly gross salary", f"₹{result['monthly_gross']:,.2f}")
        metric2.metric("Total monthly deductions", f"₹{result['total_deductions']:,.2f}")
        metric3.metric("Annual take-home salary", f"₹{result['annual_net']:,.2f}")

    # DEDUCTIONS
    st.markdown(
        """
        <div class="section-kicker">03 / Deductions</div>
        <div class="section-title">Where the deductions go</div>
        <div class="section-copy">A breakdown of the amounts deducted from monthly gross salary.</div>
        """,
        unsafe_allow_html=True,
    )

    tax_col, pf_col, insurance_col = st.columns(3)
    tax_col.metric("Income tax", f"₹{result['monthly_tax']:,.2f}")
    pf_col.metric("Provident Fund · 12%", f"₹{result['pf']:,.2f}")
    insurance_col.metric("Health insurance · 2%", f"₹{result['insurance']:,.2f}")

    # CHART
    st.markdown(
        """
        <div class="section-kicker">04 / Visual analysis</div>
        <div class="section-title">Monthly salary distribution</div>
        <div class="section-copy">See how gross salary is divided between take-home pay and deductions.</div>
        """,
        unsafe_allow_html=True,
    )

    chart_data = pd.DataFrame(
        {
            "Component": [
                "Take-home salary",
                "Income tax",
                "Provident Fund",
                "Health insurance",
            ],
            "Amount": [
                result["monthly_net"],
                result["monthly_tax"],
                result["pf"],
                result["insurance"],
            ],
        }
    )

    chart_col, detail_col = st.columns([1.15, 0.85])

    with chart_col:
        with st.container(border=True):
            fig = px.pie(
                chart_data,
                names="Component",
                values="Amount",
                hole=0.64,
                color_discrete_sequence=["#42D6A4", "#6EA8FE", "#A78BFA", "#F6BD60"],
            )
            fig.update_traces(
                textposition="outside",
                textinfo="percent",
                marker=dict(line=dict(color="#121A2B", width=3)),
                hovertemplate="%{label}<br>₹%{value:,.2f}<extra></extra>",
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#EAF1FC", family="DM Sans"),
                showlegend=True,
                legend=dict(orientation="h", y=-0.12, x=0, font=dict(size=11)),
                margin=dict(t=18, b=45, l=15, r=15),
                height=360,
            )
            st.plotly_chart(fig, use_container_width=True)

    with detail_col:
        with st.container(border=True):
            st.markdown("#### Deduction calculations")
            st.metric("Provident Fund", f"₹{result['pf']:,.2f}")
            st.caption(f"₹{monthly_salary:,.2f} × 12%")
            st.divider()
            st.metric("Health insurance", f"₹{result['insurance']:,.2f}")
            st.caption(f"₹{monthly_salary:,.2f} × 2%")
            st.divider()
            st.metric("Monthly income tax", f"₹{result['monthly_tax']:,.2f}")
            st.caption(f"Annual tax of ₹{result['annual_tax']:,.2f} ÷ 12")

    # SALARY STATEMENT
    st.markdown(
        """
        <div class="section-kicker">05 / Salary statement</div>
        <div class="section-title">Monthly salary statement</div>
        <div class="section-copy">A clear itemized view of gross pay, deductions and final take-home pay.</div>
        """,
        unsafe_allow_html=True,
    )

    salary_summary = pd.DataFrame(
        {
            "Description": [
                "Gross monthly salary",
                "Income tax",
                "Provident Fund",
                "Health insurance",
                "Total deductions",
                "Net take-home salary",
            ],
            "Amount (₹)": [
                result["monthly_gross"],
                result["monthly_tax"],
                result["pf"],
                result["insurance"],
                result["total_deductions"],
                result["monthly_net"],
            ],
        }
    )

    with st.container(border=True):
        st.dataframe(
            salary_summary.style.format({"Amount (₹)": "₹{:,.2f}"}),
            use_container_width=True,
            hide_index=True,
        )

    # ANNUAL SUMMARY
    st.markdown(
        """
        <div class="section-kicker">06 / Annual overview</div>
        <div class="section-title">Annual salary summary</div>
        <div class="section-copy">Monthly payroll values projected across 12 months.</div>
        """,
        unsafe_allow_html=True,
    )

    annual1, annual2, annual3 = st.columns(3)
    annual1.metric("Annual gross salary", f"₹{result['annual_gross']:,.2f}")
    annual2.metric("Annual income tax", f"₹{result['annual_tax']:,.2f}")
    annual3.metric("Annual net salary", f"₹{result['annual_net']:,.2f}")

    # TAX SLAB BREAKDOWN
    st.markdown(
        """
        <div class="section-kicker">07 / Tax calculation</div>
        <div class="section-title">Progressive tax slab breakdown</div>
        <div class="section-copy">The annual income is split across slabs; each rate applies only to its relevant portion.</div>
        """,
        unsafe_allow_html=True,
    )

    tax_details = calculate_tax_breakdown(result["annual_gross"])
    tax_df = pd.DataFrame(tax_details)

    if not tax_df.empty:
        tax_df.columns = [
            "Taxable income portion (₹)",
            "Tax rate",
            "Tax contribution (₹)",
        ]
        with st.container(border=True):
            st.dataframe(
                tax_df.style.format(
                    {
                        "Taxable income portion (₹)": "₹{:,.2f}",
                        "Tax contribution (₹)": "₹{:,.2f}",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
            st.info(f"Total annual tax: ₹{result['annual_tax']:,.2f}")
    else:
        st.info("No taxable income falls within the configured tax slabs.")

    # DOWNLOADABLE REPORTS
    st.markdown(
        """
        <div class="section-kicker">08 / Export</div>
        <div class="section-title">Download salary report</div>
        <div class="section-copy">Generate a PDF payslip or download a plain-text salary statement.</div>
        """,
        unsafe_allow_html=True,
    )

    pdf_file = generate_payslip_pdf(current_name, current_id, result)

    text_report = f"""SMARTPAY - EMPLOYEE SALARY STATEMENT
Employee Name: {current_name}
Employee ID: {current_id}

MONTHLY SALARY
Gross Salary: Rs. {result['monthly_gross']:,.2f}
Income Tax: Rs. {result['monthly_tax']:,.2f}
Provident Fund: Rs. {result['pf']:,.2f}
Health Insurance: Rs. {result['insurance']:,.2f}
Total Deductions: Rs. {result['total_deductions']:,.2f}
Net Take-Home Salary: Rs. {result['monthly_net']:,.2f}

ANNUAL SUMMARY
Annual Gross Salary: Rs. {result['annual_gross']:,.2f}
Annual Income Tax: Rs. {result['annual_tax']:,.2f}
Annual Net Salary: Rs. {result['annual_net']:,.2f}

Note: Educational demonstration using configurable sample rates.
"""

    download_col1, download_col2 = st.columns(2)
    with download_col1:
        st.download_button(
            "Download PDF payslip",
            data=pdf_file,
            file_name=f"SmartPay_Payslip_{current_id}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with download_col2:
        st.download_button(
            "Download text statement",
            data=text_report,
            file_name=f"SmartPay_Statement_{current_id}.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ---------------------------------------------------------
# EMPLOYEE DATABASE
# ---------------------------------------------------------
st.divider()
st.markdown(
    """
    <div class="section-kicker">09 / Records</div>
    <div class="section-title">Employee records</div>
    <div class="section-copy">View employee salary records saved in the SmartPay database.</div>
    """,
    unsafe_allow_html=True,
)

if st.button("View saved employees", use_container_width=True):
    records = get_employees()

    if records:
        employee_df = pd.DataFrame(
            records,
            columns=[
                "Record ID",
                "Employee Name",
                "Employee ID",
                "Monthly Gross Salary",
                "Net Salary",
            ],
        )
        st.dataframe(employee_df, use_container_width=True, hide_index=True)
    else:
        st.info("No employee records found yet.")


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        SMARTPAY · Employee Payroll &amp; Tax Management System
        <br>Educational demonstration using configurable sample tax and deduction rates.
    </div>
    """,
    unsafe_allow_html=True,
)
