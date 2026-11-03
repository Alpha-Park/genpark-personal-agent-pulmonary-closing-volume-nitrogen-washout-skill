"""
Pulmonary Closing Volume & Single-Breath Nitrogen Washout (SBN2) Engine.
Provides deterministic, zero-dependency modeling of Closing Volume (CV), Closing Capacity (CC),
Phase III alveolar plateau slope (%N2/L), and early small airway (< 2mm) closure.
"""

from typing import Dict, Any, List, Optional


class PulmonaryClosingVolumeClient:
    """
    Deterministic client for calculating Pulmonary Closing Volume and Closing Capacity.
    Assesses terminal bronchiolar patency, ventilation distribution heterogeneity,
    and early peripheral airway obstruction prior to detectable spirometric decline.
    """

    def __init__(self):
        pass

    def evaluate_closing_volume(
        self,
        vital_capacity_l: float,
        closing_volume_l: float,
        residual_volume_l: float,
        phase3_slope_pct_n2_per_l: float = 1.2,
        age_years: int = 35
    ) -> Dict[str, Any]:
        """
        Calculates Closing Volume percentage (CV/VC %), Closing Capacity percentage (CC/TLC %),
        and small airway patency score.
        Normative values:
        - CV/VC %: 10.0 - 20.0% (predicted approx 0.35 * age + 3.0)
        - CC/TLC %: 30.0 - 45.0%
        - Phase III slope: 0.8 - 2.0 %N2/L (elevates in inhomogeneous ventilation)
        """
        if vital_capacity_l <= 0 or closing_volume_l < 0 or residual_volume_l <= 0:
            return {"error": "Lung volumes must be strictly positive (CV non-negative)"}
        if closing_volume_l >= vital_capacity_l:
            return {"error": "Closing volume cannot exceed vital capacity"}

        # Total Lung Capacity (TLC = VC + RV)
        tlc_l = round(vital_capacity_l + residual_volume_l, 2)

        # Closing Capacity (CC = CV + RV)
        cc_l = round(closing_volume_l + residual_volume_l, 2)

        # CV/VC % and CC/TLC %
        cv_vc_pct = round((closing_volume_l / vital_capacity_l) * 100.0, 1)
        cc_tlc_pct = round((cc_l / tlc_l) * 100.0, 1)

        # Age-predicted CV/VC %
        predicted_cv_vc_pct = round(0.35 * max(18, age_years) + 3.0, 1)
        cv_ratio_to_pred = round(cv_vc_pct / predicted_cv_vc_pct, 2)

        # Small Airway Health Score (0 - 100)
        score = 80.0
        if cv_ratio_to_pred <= 1.15:
            score += 15.0
        elif cv_ratio_to_pred > 1.60:
            score -= 30.0
        elif cv_ratio_to_pred > 1.30:
            score -= 15.0

        if phase3_slope_pct_n2_per_l <= 1.5:
            score += 5.0
        elif phase3_slope_pct_n2_per_l > 3.0:
            score -= 20.0
        elif phase3_slope_pct_n2_per_l > 2.0:
            score -= 10.0

        small_airway_score = round(min(100.0, max(5.0, score)), 1)

        if small_airway_score >= 85.0 and cv_ratio_to_pred <= 1.20 and phase3_slope_pct_n2_per_l <= 1.8:
            tier = "OPTIMAL_SMALL_AIRWAY_PATENCY"
            interp = f"Normal closing volume (CV/VC {cv_vc_pct}%, predicted {predicted_cv_vc_pct}%) and homogeneous alveolar slope ({phase3_slope_pct_n2_per_l} %N2/L); no premature dependent bronchiolar collapse."
            guidance = "Excellent small airway integrity. Alveolar ventilation distribution is highly uniform across lung zones."
        elif cv_ratio_to_pred > 1.45 or phase3_slope_pct_n2_per_l > 2.5:
            tier = "PREMATURE_AIRWAY_CLOSURE_SUSPECTED"
            interp = f"Markedly elevated closing volume (CV/VC {cv_vc_pct}% > {predicted_cv_vc_pct}% pred) and steep alveolar slope ({phase3_slope_pct_n2_per_l} %N2/L); reflects premature collapse of dependent small bronchioles (< 2mm)."
            guidance = "Premature airway closure detected. Small airways may close during resting tidal volume. Minimize particulate exposure and consider bronchodilator evaluation."
        else:
            tier = "MILD_VENTILATION_INHOMOGENEITY"
            interp = f"Borderline closing volume elevation (CV/VC {cv_vc_pct}%, ratio {cv_ratio_to_pred}x pred); slight ventilation non-uniformity."
            guidance = "Maintain aerobic conditioning and practice diaphragmatic deep breathing to enhance dependent lung zone expansion."

        return {
            "vital_capacity_l": vital_capacity_l,
            "closing_volume_l": closing_volume_l,
            "residual_volume_l": residual_volume_l,
            "total_lung_capacity_l": tlc_l,
            "closing_capacity_l": cc_l,
            "cv_vc_pct": cv_vc_pct,
            "cc_tlc_pct": cc_tlc_pct,
            "predicted_cv_vc_pct": predicted_cv_vc_pct,
            "phase3_slope_pct_n2_per_l": phase3_slope_pct_n2_per_l,
            "small_airway_score": small_airway_score,
            "classification": tier,
            "physiological_interpretation": interp,
            "actionable_guidance": guidance
        }
