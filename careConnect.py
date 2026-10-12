import pandas as pd
import random
import string

from PatientProfile import PatientProfile

CSV_PATH = "Vaccination schedule.csv"

def nameGenerator():
    names = [
    "Harpreet Gill", "Gurpreet Dhaliwal", "Jaspreet Brar", "Navpreet Sidhu", "Dilpreet Sandhu",
    "Simran Grewal", "Manveer Bains", "Amrit Sohal", "Kiran Mann", "Rajan Johal",
    "Emily Carter", "Liam Fraser", "Olivia Bennett", "Noah Tremblay", "Ava Morrison",
    "Ethan Wallace", "Sophie Gagnon", "Lucas Reimer", "Chloe Friesen", "Owen Penner",
    "Mei Lin Chen", "Daniel Wong", "Grace Liu", "Kevin Zhang", "Hana Kim",
    "Minh Tran", "Linh Nguyen", "Kenji Sato", "Priya Patel", "Arjun Sharma",
    "Anika Verma", "Rohan Mehta", "Fatima Hassan", "Omar Farouk", "Layla Ahmed",
    "Yusuf Rahman", "Amara Okafor", "Kwame Mensah", "Zainab Bello", "Tunde Adeyemi",
    "Sofia Martinez", "Mateo Garcia", "Isabella Rojas", "Diego Fernandez", "Camila Torres",
    "Anna Kowalski", "Viktor Novak", "Elena Petrova", "Marta Lindgren", "Jonas Becker",
    "Claire Dubois", "Hugo Lefebvre", "Aiyana Flett", "Cody Ross", "Maya Sinclair",
    "Riley Spence", "Hannah Wiebe", "Jacob Dyck", "Nora Klassen", "Samuel Loewen",
    ]
    r = random.randint(0, len(names) - 1)
    return  names[r]


def generateRandomPatients(patientID: int, vaccineCodes: list[str]):
    # Create with dummy values then overwrite because patientProfile.py overwrites dict fields
    p = PatientProfile()

    p.id = patientID
    p.name = nameGenerator()
    p.age = random.randint(1, 100)

    p.sex = "male" if random.randint(1, 2) == 1 else "female"

    maxTaken = min(6, len(vaccineCodes))  # cap for realism + demo
    k = random.randint(0, maxTaken)
    p.vaccines = list(random.sample(vaccineCodes, k))
    p.dueVaccines = vaccinesDue(vaccineCodes, p.vaccines, maxDue=6)

    # Risk factors:
    # 70% none
    # other 30%: immunocompromised, chronic disease, pregnancy allow multiple to appear

    riskOptions = [
    ["immunocompromised"],
    ["chronic_disease"],
    ["pregnancy"],
    ["immunocompromised", "chronic_disease"],
    ["chronic_disease", "pregnancy"],
    ["immunocompromised", "pregnancy"],
    ["immunocompromised", "chronic_disease", "pregnancy"],
    ]

    r = random.random()

    if r < 0.70:
        p.riskFactors = []
    else:
        p.riskFactors = random.choice(riskOptions)

        if "pregnancy" in p.riskFactors and (p.sex != "female" or not (18 <= p.age <= 45)):
            p.riskFactors.remove("pregnancy")

    return p


def vaccinesDue(vaccineCodes, taken, maxDue=6):

    eligible = list(set(vaccineCodes) - set(taken))
    if not eligible:
        return []

    k = random.randint(0, min(maxDue, len(eligible)))
    return random.sample(eligible, k)

def buildPatients():
    df = pd.read_csv(CSV_PATH)

    # List of all distinct vaccines from the file
    vaccineCodes = sorted(df["VACCINECODE"].dropna().unique().tolist())

    patients = []
    # vaccine_rules = []

    usedCodes = set()
    

    # Loop over EVERY row in the CSV (as you asked)
    for _, row in df.iterrows():

        patientID = random.randint(10000, 99999)

        while patientID in usedCodes:
            patientID = random.randint(10000, 99999)

        usedCodes.add(patientID)
            
        p = generateRandomPatients(patientID, vaccineCodes)

        
        # vr = build_vaccine_rule_from_row(row)

        patients.append(p)
        # vaccine_rules.append(vr)

    return patients


def main():
    patients = buildPatients()

    print(f"Created {len(patients)} PatientProfile objects")

    # Example: print first 3
    for i in range(3):
        print("----")
        print("Patient:", patients[i].id, patients[i].name, patients[i].age, patients[i].sex)
        print("Risk Factors:", patients[i].riskFactors)
        print("Vaccines taken:", patients[i].vaccines[:5])  # show first few if large

if __name__ == "__main__":
    main()