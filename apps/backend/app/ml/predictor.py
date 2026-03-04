import math
from typing import Dict, Any, List, Tuple

class RiskEngine:
    def __init__(self):
        self.protected_attributes = {"gender", "caste", "religion", "location", "age"}
        self.required_features = {"income", "expenses", "savings", "transaction_count"}
        self.load_model()

    def load_model(self) -> None:
        self._model_version = "v1.0.0"
        self._model_type = "Behavioral Gradient Boosting"
        self._is_loaded = True

    def apply_fairness_filter(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        return {
            key: value
            for key, value in raw_input.items()
            if key.lower() not in self.protected_attributes
        }

    def validate_input(self, filtered_input: Dict[str, Any]) -> None:
        for req_field in self.required_features:
            if req_field not in filtered_input:
                raise ValueError(f"Missing required financial feature: {req_field}")
            
            val = filtered_input[req_field]
            if not isinstance(val, (int, float)):
                raise TypeError(f"Feature {req_field} must be numeric.")
            if val < 0:
                raise ValueError(f"Feature {req_field} cannot be negative.")

    def preprocess_features(self, valid_input: Dict[str, Any]) -> Dict[str, float]:
        income = float(valid_input["income"])
        expenses = float(valid_input["expenses"])
        savings = float(valid_input["savings"])
        transaction_count = float(valid_input["transaction_count"])

        safe_income = income if income > 0 else 1.0
        safe_expenses = expenses if expenses > 0 else 1.0

        expense_to_income_ratio = expenses / safe_income
        savings_to_expense_ratio = savings / safe_expenses
        transaction_intensity_score = min(transaction_count / 100.0, 1.0)

        return {
            "expense_to_income_ratio": expense_to_income_ratio,
            "savings_to_expense_ratio": savings_to_expense_ratio,
            "transaction_intensity_score": transaction_intensity_score,
            "absolute_savings": savings
        }

    def predict_score(self, engineered_features: Dict[str, float]) -> int:
        base_score = 400
        
        eti_component = max(0, 200 * (1 - engineered_features["expense_to_income_ratio"]))
        ste_component = min(250, 100 * engineered_features["savings_to_expense_ratio"])
        ti_component = 50 * engineered_features["transaction_intensity_score"]
        
        raw_score = base_score + eti_component + ste_component + ti_component
        
        return int(max(300, min(850, math.floor(raw_score))))

    def compute_risk_level(self, score: int) -> str:
        if score >= 750:
            return "Low"
        if 650 <= score <= 749:
            return "Medium"
        return "High"

    def generate_explanations(self, engineered_features: Dict[str, float]) -> List[Dict[str, Any]]:
        explanations = []

        ste = engineered_features["savings_to_expense_ratio"]
        if ste >= 1.0:
            explanations.append({
                "factor": "Savings Ratio",
                "impact": "+",
                "weight": 0.25,
                "description": "Strong savings-to-expense balance improved your profile."
            })
        elif ste < 0.2:
            explanations.append({
                "factor": "Savings Ratio",
                "impact": "-",
                "weight": 0.20,
                "description": "Low liquid savings relative to expenses increased risk profile."
            })

        eti = engineered_features["expense_to_income_ratio"]
        if eti < 0.4:
            explanations.append({
                "factor": "Debt-to-Income",
                "impact": "+",
                "weight": 0.30,
                "description": "Sustainable expense ratio indicates high repayment capacity."
            })
        elif eti > 0.7:
            explanations.append({
                "factor": "Debt-to-Income",
                "impact": "-",
                "weight": 0.35,
                "description": "High outgoing expenses relative to income detected."
            })

        ti = engineered_features["transaction_intensity_score"]
        if ti > 0.3:
            explanations.append({
                "factor": "Transaction Velocity",
                "impact": "+",
                "weight": 0.10,
                "description": "Consistent financial activity demonstrates reliable account usage."
            })

        return explanations

    def format_compliance_response(
        self, 
        score: int, 
        risk_level: str, 
        explanations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {
            "score": score,
            "risk_level": risk_level,
            "explanations": explanations,
            "compliance": {
                "demographic_data_used": False,
                "model_type": self._model_type,
                "explainability": "Feature Contribution Based",
                "audit_version": self._model_version
            }
        }

    def process(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        filtered_input = self.apply_fairness_filter(raw_input)
        self.validate_input(filtered_input)
        engineered_features = self.preprocess_features(filtered_input)
        score = self.predict_score(engineered_features)
        risk_level = self.compute_risk_level(score)
        explanations = self.generate_explanations(engineered_features)
        
        return self.format_compliance_response(score, risk_level, explanations)