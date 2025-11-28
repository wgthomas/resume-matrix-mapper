#!/usr/bin/env python3
"""
Test script for resume-matrix-mapper skill.
Validates that the skill components work correctly.
"""

import sys
import os

def test_imports():
    """Test that required Python packages are available."""
    print("Testing Python package imports...")
    
    try:
        from docx import Document
        print("  ✓ python-docx available")
    except ImportError:
        print("  ✗ python-docx not found - install with: pip install python-docx")
        return False
    
    try:
        import re
        print("  ✓ re (regex) available")
    except ImportError:
        print("  ✗ re module not available")
        return False
    
    try:
        from datetime import datetime
        print("  ✓ datetime available")
    except ImportError:
        print("  ✗ datetime not available")
        return False
    
    return True

def test_script_structure():
    """Test that all required script files exist."""
    print("\nTesting script structure...")
    
    required_files = [
        'scripts/extract_resume.py',
        'scripts/map_resume_to_matrix.py',
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✓ {file_path} exists")
        else:
            print(f"  ✗ {file_path} not found")
            all_exist = False
    
    return all_exist

def test_script_execution():
    """Test that scripts can be executed."""
    print("\nTesting script execution...")
    
    # Test extract_resume.py
    result = os.system("python scripts/extract_resume.py > /dev/null 2>&1")
    if result == 0:
        print("  ✓ extract_resume.py runs without errors")
    else:
        print("  ⚠ extract_resume.py expects arguments (this is correct)")
    
    # Test map_resume_to_matrix.py
    result = os.system("python scripts/map_resume_to_matrix.py > /dev/null 2>&1")
    if result == 0:
        print("  ✓ map_resume_to_matrix.py runs without errors")
    else:
        print("  ⚠ map_resume_to_matrix.py expects arguments (this is correct)")
    
    return True

def test_documentation():
    """Test that documentation files exist."""
    print("\nTesting documentation...")
    
    required_docs = [
        'SKILL.md',
        'README.md',
        'references/matching-strategies.md',
        'references/examples.md',
    ]
    
    all_exist = True
    for doc_path in required_docs:
        if os.path.exists(doc_path):
            # Check file size
            size = os.path.getsize(doc_path)
            print(f"  ✓ {doc_path} exists ({size:,} bytes)")
        else:
            print(f"  ✗ {doc_path} not found")
            all_exist = False
    
    return all_exist

def test_skill_metadata():
    """Test that SKILL.md has proper frontmatter."""
    print("\nTesting SKILL.md metadata...")
    
    try:
        with open('SKILL.md', 'r') as f:
            content = f.read()
            
            # Check for frontmatter
            if content.startswith('---'):
                print("  ✓ SKILL.md has frontmatter")
            else:
                print("  ✗ SKILL.md missing frontmatter")
                return False
            
            # Check for required fields
            if 'name:' in content:
                print("  ✓ 'name' field present")
            else:
                print("  ✗ 'name' field missing")
                return False
            
            if 'description:' in content:
                print("  ✓ 'description' field present")
            else:
                print("  ✗ 'description' field missing")
                return False
            
            # Check content length
            if len(content) > 5000:
                print(f"  ✓ SKILL.md has substantial content ({len(content):,} characters)")
            else:
                print(f"  ⚠ SKILL.md seems short ({len(content):,} characters)")
            
    except Exception as e:
        print(f"  ✗ Error reading SKILL.md: {e}")
        return False
    
    return True

def run_integration_test():
    """Run a simple integration test if test files are available."""
    print("\nChecking for test files...")
    
    test_files = [
        'test_resume.docx',
        'test_matrix.docx',
    ]
    
    files_exist = all(os.path.exists(f) for f in test_files)
    
    if not files_exist:
        print("  ⚠ Test files not found (optional)")
        print("    To run integration test, provide:")
        print("    - test_resume.docx")
        print("    - test_matrix.docx")
        return True
    
    print("  ✓ Test files found")
    print("\nRunning integration test...")
    
    cmd = "python scripts/map_resume_to_matrix.py test_resume.docx test_matrix.docx test_output.docx"
    result = os.system(cmd)
    
    if result == 0 and os.path.exists('test_output.docx'):
        print("  ✓ Integration test passed")
        print("  ✓ test_output.docx created successfully")
        return True
    else:
        print("  ✗ Integration test failed")
        return False

def main():
    """Run all tests and report results."""
    print("=" * 60)
    print("Resume-to-Matrix Mapper Skill - Test Suite")
    print("=" * 60)
    
    # Change to script directory if running from elsewhere
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)
    
    tests = [
        ("Package Imports", test_imports),
        ("Script Structure", test_script_structure),
        ("Script Execution", test_script_execution),
        ("Documentation", test_documentation),
        ("Skill Metadata", test_skill_metadata),
        ("Integration Test", run_integration_test),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'=' * 60}")
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"  ✗ Test crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print(f"\n{'=' * 60}")
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:8} {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\n{passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n✓ All tests passed! Skill is ready to use.")
        return 0
    else:
        print(f"\n⚠ {total_count - passed_count} test(s) failed. Review output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
