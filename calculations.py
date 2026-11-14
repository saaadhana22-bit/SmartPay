
# SMARTPAY - SALARY CALCULATION ENGINE

PF_RATE = 0.12
INSURANCE_RATE = 0.02


# 1. Calculate annual gross salary
def calculate_gross_salary(monthly_salary):
    return monthly_salary * 12


# 2. Calculate progressive income tax
def calculate_tax(annual_salary):

    if annual_salary <= 300000:
        tax = 0

    elif annual_salary <= 600000:
        tax = (annual_salary - 300000) * 0.05

    elif annual_salary <= 900000:
        tax = 15000 + (annual_salary - 600000) * 0.10

    elif annual_salary <= 1200000:
        tax = 45000 + (annual_salary - 900000) * 0.15

    else:
        tax = 90000 + (annual_salary - 1200000) * 0.20

    return tax


# 3. Calculate Provident Fund
def calculate_pf(monthly_salary):
    return monthly_salary * PF_RATE


# 4. Calculate health insurance
def calculate_insurance(monthly_salary):
    return monthly_salary * INSURANCE_RATE


# 5. Calculate complete salary breakdown
def calculate_salary(monthly_salary):

    if monthly_salary <= 0:
        raise ValueError("Salary must be greater than zero.")

    annual_salary = calculate_gross_salary(monthly_salary)

    annual_tax = calculate_tax(annual_salary)

    monthly_tax = annual_tax / 12

    pf = calculate_pf(monthly_salary)

    insurance = calculate_insurance(monthly_salary)

    total_deductions = monthly_tax + pf + insurance

    net_salary = monthly_salary - total_deductions

    return {
        "monthly_gross": monthly_salary,
        "annual_gross": annual_salary,
        "annual_tax": annual_tax,
        "monthly_tax": monthly_tax,
        "pf": pf,
        "insurance": insurance,
        "total_deductions": total_deductions,
        "monthly_net": net_salary,
        "annual_net": net_salary * 12
    }

# 6. Show detailed progressive tax calculation
def calculate_tax_breakdown(annual_salary):

    slabs = [
        (300000, 0.00),
        (600000, 0.05),
        (900000, 0.10),
        (1200000, 0.15),
        (float("inf"), 0.20)
    ]

    breakdown = []
    previous_limit = 0

    for limit, rate in slabs:

        taxable_amount = max(
            0,
            min(annual_salary, limit) - previous_limit
        )

        if taxable_amount > 0:
            tax_amount = taxable_amount * rate

            breakdown.append({
                "Taxable Portion": taxable_amount,
                "Tax Rate": f"{rate * 100:.0f}%",
                "Tax Amount": tax_amount
            })

        if annual_salary <= limit:
            break

        previous_limit = limit

    return breakdown
