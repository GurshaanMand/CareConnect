import heapq

def score_patient(p):
    score = 0.0
    reasons = []

    # Age score (0 to 0.25)
    if p.age >= 65 and p.age < 75:
        score += 0.4*0.7
        reasons.append("Senior (65-74)")

    elif p.age >= 75 and p.age <85:
        score += 0.4*0.8
        reasons.append("Senior (75-84)")

    elif p.age >= 85 and p.age <95:
        score += 0.4*0.9
        reasons.append("Senior (85-94)")
        
    elif p.age >=95 and p.age <= 100:
        score += 0.4*1
        reasons.append("Senior (95-100)")

    elif p.age < 5:
        score += 0.4*1
        reasons.append("Young child (<5)")

    elif p.age < 18:
        score += 0.4*0.8
        reasons.append("Minor (<18)")

    else:
        score += 0.4*0.4
        reasons.append("Adult (18-64)")

    # Risk factors (0 to 0.45 cap)
    risk_score = 0.0
    rf = set(p.riskFactors)  # convert list -> set for easy membership

    if "immunocompromised" in rf:
        risk_score += 0.4/3*0.5
        reasons.append("High risk: immunocompromised")
    if "chronic_disease" in rf:
        risk_score += 0.4/3*0.25
        reasons.append("Risk: chronic disease")
    if "pregnancy" in rf:
        risk_score += 0.4/3*0.25
        reasons.append("Risk: pregnancy")

    score += risk_score

    takenCount = len(p.vaccines)

    # fewer vaccines taken = higher urgency
    ratio = takenCount/24

    if ratio<=0.10:
        gapScore = 0.30*1

    elif ratio<=0.2 and ratio > 0.1:
        gapScore = 0.30*0.9

    elif ratio<=0.3 and ratio > 0.2:
        gapScore = 0.30*0.8

    elif ratio<=0.4 and ratio > 0.3:
        gapScore = 0.30*0.7

    elif ratio<=0.5 and ratio > 0.4:
        gapScore = 0.30*0.6

    elif ratio<=0.6 and ratio > 0.5:
        gapScore = 0.30*0.5

    elif ratio<=0.7 and ratio > 0.6:
        gapScore = 0.30*0.4

    elif ratio<=0.8 and ratio > 0.7:
        gapScore = 0.30*0.3

    elif ratio<=0.9 and ratio > 0.8:
        gapScore = 0.30*0.2

    else:
        gapScore = 0.30*0.1

    score += gapScore

    if takenCount <= 2:
        reasons.append("Low vaccination history")

    # Clamp final score to [0, 1] (optional but safe)
    score = max(0.0, min(score, 1.0))

    return score, reasons

def priorityHeap(patients):

    heap = []

    for p in patients:
        score, reasons = score_patient(p)

        # push negative score to simulate max heap
        heapq.heappush(heap, (-score, p.id, p, reasons))
    return heap