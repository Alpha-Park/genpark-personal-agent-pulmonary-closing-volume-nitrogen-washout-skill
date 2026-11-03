"""
Example Usage: Pulmonary Closing Volume & Nitrogen Washout (SBN2).
Demonstrates zero-dependency calculation of Closing Volume (CV/VC %), Closing Capacity (CC/TLC %), and small airway scoring.
"""

from client import PulmonaryClosingVolumeClient


def main():
    client = PulmonaryClosingVolumeClient()
    print("=== Pulmonary Closing Volume & Nitrogen Washout (SBN2) Demo ===")

    # Test Case 1: Healthy young adult with pristine small airways
    res1 = client.evaluate_closing_volume(
        vital_capacity_l=4.8,
        closing_volume_l=0.62,
        residual_volume_l=1.35,
        phase3_slope_pct_n2_per_l=1.1,
        age_years=28
    )
    print("\nTest Case 1: Normal Small Airway Patency (28 yo)")
    print(f"  Vital Capacity: {res1['vital_capacity_l']} L | TLC: {res1['total_lung_capacity_l']} L")
    print(f"  Closing Volume: {res1['closing_volume_l']} L (CV/VC: {res1['cv_vc_pct']}%, Predicted: {res1['predicted_cv_vc_pct']}%)")
    print(f"  Closing Capacity: {res1['closing_capacity_l']} L (CC/TLC: {res1['cc_tlc_pct']}%)")
    print(f"  Phase III Plateau Slope: {res1['phase3_slope_pct_n2_per_l']} %N2/L")
    print(f"  Small Airway Score: {res1['small_airway_score']} / 100")
    print(f"  Classification: {res1['classification']}")
    print(f"  Physiological Interpretation: {res1['physiological_interpretation']}")
    print(f"  Actionable Guidance: {res1['actionable_guidance']}")

    # Test Case 2: Early peripheral small airway closure
    res2 = client.evaluate_closing_volume(
        vital_capacity_l=3.9,
        closing_volume_l=0.95,
        residual_volume_l=1.65,
        phase3_slope_pct_n2_per_l=2.8,
        age_years=45
    )
    print("\nTest Case 2: Premature Airway Closure Pattern")
    print(f"  Closing Volume: {res2['closing_volume_l']} L (CV/VC: {res2['cv_vc_pct']}%, Predicted: {res2['predicted_cv_vc_pct']}%)")
    print(f"  Phase III Slope: {res2['phase3_slope_pct_n2_per_l']} %N2/L")
    print(f"  Small Airway Score: {res2['small_airway_score']} / 100")
    print(f"  Classification: {res2['classification']}")
    print(f"  Actionable Guidance: {res2['actionable_guidance']}")


if __name__ == "__main__":
    main()
