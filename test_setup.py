#!/usr/bin/env python3
"""
Kroosybul AI - Setup Test
Verifies that the environment is configured correctly
"""

import sys
import os
from pathlib import Path


def test_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False


def test_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")

    required_packages = [
        'flask',
        'flask_socketio',
        'anthropic',
        'dotenv',
        'requests'
    ]

    all_installed = True

    for package in required_packages:
        try:
            __import__(package.replace('_', '.'))
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - Not installed")
            all_installed = False

    return all_installed


def test_env_file():
    """Check if .env file exists and has required variables"""
    print("\n🔍 Checking .env file...")

    env_path = Path('.env')

    if not env_path.exists():
        print("❌ .env file not found")
        print("💡 Run: cp .env.example .env")
        return False

    with open(env_path) as f:
        content = f.read()

    if 'ANTHROPIC_API_KEY=' in content:
        # Check if API key is set (not the default)
        if 'your_anthropic_api_key_here' in content:
            print("⚠️  .env file exists but API key not set")
            print("💡 Edit .env and add your Anthropic API key")
            return False
        else:
            print("✅ .env file configured")
            return True
    else:
        print("❌ .env file missing ANTHROPIC_API_KEY")
        return False


def test_directories():
    """Check if required directories exist"""
    print("\n🔍 Checking directories...")

    dirs = ['generated_projects', 'core', 'static', 'templates']
    all_exist = True

    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ {dir_name}/ - Exists")
        else:
            print(f"❌ {dir_name}/ - Not found")
            all_exist = False

    return all_exist


def test_core_modules():
    """Check if core modules can be imported"""
    print("\n🔍 Checking core modules...")

    modules = [
        'core.ai_engine',
        'core.project_generator',
        'core.code_executor'
    ]

    all_importable = True

    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except Exception as e:
            print(f"❌ {module} - Error: {e}")
            all_importable = False

    return all_importable


def test_static_files():
    """Check if static files exist"""
    print("\n🔍 Checking static files...")

    files = [
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js'
    ]

    all_exist = True

    for file_path in files:
        if Path(file_path).exists():
            print(f"✅ {file_path} - Exists")
        else:
            print(f"❌ {file_path} - Not found")
            all_exist = False

    return all_exist


def main():
    """Run all tests"""
    print("=" * 50)
    print("🔥 Kroosybul AI - Setup Test")
    print("=" * 50)

    results = []

    # Run all tests
    results.append(("Python Version", test_python_version()))
    results.append(("Dependencies", test_dependencies()))
    results.append(("Environment File", test_env_file()))
    results.append(("Directories", test_directories()))
    results.append(("Core Modules", test_core_modules()))
    results.append(("Static Files", test_static_files()))

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:<20} {status}")

    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 50)

    if passed == total:
        print("\n🎉 All tests passed! Kroosybul AI is ready to use.")
        print("🚀 Run: python app.py")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        print("💡 Check README.md for setup instructions")
        return 1


if __name__ == '__main__':
    sys.exit(main())
