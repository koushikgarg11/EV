import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_etl import test_validate_coordinates, test_missing_values
from tests.test_gis_engine import test_kdtree_spatial_index, test_catchment_coverage
from tests.test_decision_engine import test_mcda_scoring, test_explainability

def run_all_tests():
    print("=== Running Unit Test Suite ===")
    
    tests = [
        ("test_validate_coordinates", test_validate_coordinates),
        ("test_missing_values", test_missing_values),
        ("test_kdtree_spatial_index", test_kdtree_spatial_index),
        ("test_catchment_coverage", test_catchment_coverage),
        ("test_mcda_scoring", test_mcda_scoring),
        ("test_explainability", test_explainability)
    ]
    
    passed = 0
    for name, func in tests:
        try:
            func()
            print(f"[PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name} - {e}")
            
    print(f"\nTest Summary: {passed}/{len(tests)} tests passed.")
    if passed == len(tests):
        print("ALL TESTS PASSED SUCCESSFULLY!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
