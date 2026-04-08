def classify_company(signals):
    """
    Classifies company based on extracted signals from extract_signals()

    signals example:
    {
        "manual_roles": int,
        "manual_keywords": int,
        "scaling": bool
    }
    """

    # Extract values safely
    manual_roles = signals.get("manual_roles", 0)
    manual_keywords = signals.get("manual_keywords", 0)
    scaling = signals.get("scaling", False)

    # Rule 1: High manual workload
    if manual_roles >= 5:
        category = "HIGH_MANUAL"

    # Rule 2: Medium workload
    elif manual_roles >= 3 or manual_keywords >= 2:
        category = "MEDIUM_MANUAL"

    # Rule 3: Low workload
    else:
        category = "LOW_MANUAL"

    # Boost rule for scaling companies
    if scaling and category == "MEDIUM_MANUAL":
        category = "HIGH_MANUAL"

    return category


def cluster_roles(job_titles):
    """
    Groups similar job roles into one cluster
    Example: data entry, back office, operations → same category
    """

    keywords = ["data entry", "back office", "operations", "admin"]

    count = 0
    for job in job_titles:
        job = job.lower()
        if any(k in job for k in keywords):
            count += 1

    return count

if __name__ == "__main__":
    from classification import classify_company

    test_data = [
        {"manual_roles": 6, "manual_keywords": 4, "scaling": True},
        {"manual_roles": 1, "manual_keywords": 0, "scaling": False},
        {"manual_roles": 3, "manual_keywords": 2, "scaling": False},
        {"manual_roles": 0, "manual_keywords": 1, "scaling": False},
        {"manual_roles": 5, "manual_keywords": 3, "scaling": False},
    ]

    for i, company in enumerate(test_data):
        result = classify_company(company)
        print(f"Company {i+1}: {result}")
