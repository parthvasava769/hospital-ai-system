class AIAssistanceAgent:
    """
    AI Agent that analyzes symptoms and provides medical suggestions.
    This is a rule-based version that can later be replaced with an LLM.
    """

    symptom_rules = {
        "fever": {
            "possible_conditions": ["Flu", "Viral Infection"],
            "recommended_tests": ["CBC Blood Test"]
        },
        "chest pain": {
            "possible_conditions": ["Heart Disease", "Angina"],
            "recommended_tests": ["ECG", "Blood Pressure"]
        },
        "headache": {
            "possible_conditions": ["Migraine", "Stress"],
            "recommended_tests": ["Neurological Exam"]
        },
        "fatigue": {
            "possible_conditions": ["Anemia", "Vitamin Deficiency"],
            "recommended_tests": ["CBC Blood Test", "Vitamin D Test"]
        }
    }

    @staticmethod
    def analyze_symptoms(symptoms: str):

        symptoms = symptoms.lower()

        results = {
            "possible_conditions": [],
            "recommended_tests": []
        }

        for key, value in AIAssistanceAgent.symptom_rules.items():

            if key in symptoms:
                results["possible_conditions"].extend(value["possible_conditions"])
                results["recommended_tests"].extend(value["recommended_tests"])

        if not results["possible_conditions"]:
            results["possible_conditions"].append("Further medical evaluation required")

        return results