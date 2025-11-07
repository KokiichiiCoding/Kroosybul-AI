#!/usr/bin/env python3
"""
Test script for new features in Kroosybul AI
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all new modules can be imported"""
    print("Testing imports...")

    try:
        from core.project_templates import ProjectTemplates
        print("✓ ProjectTemplates imported successfully")

        from core.enhanced_features import EnhancedAIFeatures, MultiModelSupport, ReusableComponentLibrary
        print("✓ EnhancedAIFeatures imported successfully")
        print("✓ MultiModelSupport imported successfully")
        print("✓ ReusableComponentLibrary imported successfully")

        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_project_templates():
    """Test project templates functionality"""
    print("\nTesting project templates...")

    try:
        from core.project_templates import ProjectTemplates

        # Get all templates
        templates = ProjectTemplates.get_all_templates()
        print(f"✓ Found {len(templates)} total templates")

        # Test specific templates
        discord_bot = ProjectTemplates.get_template_by_id('discord_bot')
        if discord_bot:
            print(f"✓ Discord Bot template: {discord_bot['name']}")

        flask_dashboard = ProjectTemplates.get_template_by_id('flask_dashboard')
        if flask_dashboard:
            print(f"✓ Flask Dashboard template: {flask_dashboard['name']}")

        ai_agent = ProjectTemplates.get_template_by_id('ai_agent_langchain')
        if ai_agent:
            print(f"✓ AI Agent (LangChain) template: {ai_agent['name']}")

        # Test category filtering
        web_templates = ProjectTemplates.get_templates_by_category('web')
        print(f"✓ Found {len(web_templates)} web templates")

        ai_templates = ProjectTemplates.get_templates_by_category('ai')
        print(f"✓ Found {len(ai_templates)} AI templates")

        bot_templates = ProjectTemplates.get_templates_by_category('bot')
        print(f"✓ Found {len(bot_templates)} bot templates")

        return True
    except Exception as e:
        print(f"✗ Template test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multi_model_support():
    """Test multi-model support"""
    print("\nTesting multi-model support...")

    try:
        from core.enhanced_features import MultiModelSupport

        multi_model = MultiModelSupport()
        available_models = multi_model.get_available_models()

        print(f"✓ Found {len(available_models)} available AI models")

        for model in available_models:
            print(f"  - {model['name']} ({model['provider']})")

        return True
    except Exception as e:
        print(f"✗ Multi-model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_component_library():
    """Test reusable component library"""
    print("\nTesting component library...")

    try:
        from core.enhanced_features import ReusableComponentLibrary
        import tempfile
        import shutil

        # Create a temporary directory for testing
        temp_dir = tempfile.mkdtemp()

        try:
            component_lib = ReusableComponentLibrary(storage_path=temp_dir)

            # Test saving a component
            component_lib.save_component(
                name="Test Function",
                code="def test(): return 'Hello'",
                language="python",
                description="A simple test function",
                tags=["test", "example"]
            )
            print("✓ Component saved successfully")

            # Test searching
            results = component_lib.search_components(query="test", language="python")
            if results:
                print(f"✓ Found {len(results)} components")

            # Test retrieval
            component = component_lib.get_component("Test Function", "python")
            if component:
                print(f"✓ Retrieved component: {component['name']}")

        finally:
            # Clean up
            shutil.rmtree(temp_dir, ignore_errors=True)

        return True
    except Exception as e:
        print(f"✗ Component library test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_dependency_analysis():
    """Test dependency analysis"""
    print("\nTesting dependency analysis...")

    try:
        # Mock AI engine for testing
        class MockAIEngine:
            def __init__(self):
                self.client = None
                self.model = "mock"

        from core.enhanced_features import EnhancedAIFeatures

        ai_engine = MockAIEngine()
        enhanced = EnhancedAIFeatures(ai_engine)

        # Test Python dependency detection
        python_code = """
import flask
from sqlalchemy import create_engine
import requests
"""
        deps = enhanced.analyze_dependencies(python_code, "python")
        print(f"✓ Python dependencies detected: {deps}")

        # Test JavaScript dependency detection
        js_code = """
const express = require('express');
import axios from 'axios';
"""
        deps = enhanced.analyze_dependencies(js_code, "javascript")
        print(f"✓ JavaScript dependencies detected: {deps}")

        return True
    except Exception as e:
        print(f"✗ Dependency analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Kroosybul AI - New Features Test Suite")
    print("=" * 60)

    tests = [
        ("Imports", test_imports),
        ("Project Templates", test_project_templates),
        ("Multi-Model Support", test_multi_model_support),
        ("Component Library", test_component_library),
        ("Dependency Analysis", test_dependency_analysis),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
