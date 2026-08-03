@echo off
title BUTLER UNIFIED INSPECTOR
set "PYTHON_EXE="
if exist ".butler_python_path" set /p PYTHON_EXE=<.butler_python_path
if not defined PYTHON_EXE set "PYTHON_EXE=python"

echo ============================================
echo BUTLER UNIFIED INSPECTOR
echo ============================================

"%PYTHON_EXE%" Inspector0_PhysicalMap.py . Inspector0_PhysicalMap.json
if errorlevel 1 goto :failed
"%PYTHON_EXE%" Inspector1_EntityMap.py Inspector0_PhysicalMap.json Inspector1_EntityMap.json
if errorlevel 1 goto :failed
"%PYTHON_EXE%" Inspector1_EntityMap.py Inspector0_PhysicalMap.json UnifiedInspectorFacts.json
if errorlevel 1 goto :failed
"%PYTHON_EXE%" Inspector2_ImportMap.py Inspector0_PhysicalMap.json Inspector2_ImportMap.json
if errorlevel 1 goto :failed
"%PYTHON_EXE%" Inspector3_RegistrationAST.py Inspector0_PhysicalMap.json Inspector3_RegistrationAST.json
if errorlevel 1 goto :failed
"%PYTHON_EXE%" Inspector4_CallGraph.py Inspector0_PhysicalMap.json Inspector4_CallGraph.json
if errorlevel 1 goto :failed
"%PYTHON_EXE%" Inspector5_LinkMap.py Inspector0_PhysicalMap.json Inspector5_LinkMap.json
if errorlevel 1 goto :failed
"%PYTHON_EXE%" LinkMapBuilder.py LinkMap.json
if errorlevel 1 goto :failed
"%PYTHON_EXE%" DependencyModelBuilder.py LinkMap.json DependencyModel.json
if errorlevel 1 goto :failed
"%PYTHON_EXE%" Inspector5_DependencyGraph.py
if errorlevel 1 goto :failed
"%PYTHON_EXE%" Inspector-Discovery_v3_1_TEST.py --build
if errorlevel 1 goto :failed
"%PYTHON_EXE%" Generate_UnifiedInspector_Report.py
if errorlevel 1 goto :failed
"%PYTHON_EXE%" Inspector_Status_Report.py
if errorlevel 1 goto :failed
"%PYTHON_EXE%" UnifiedInspector_ACCEPTANCE.py
if errorlevel 1 goto :failed

echo ============================================
echo READY: full Inspector chain rebuilt
echo ============================================
exit /b 0

:failed
echo ============================================
echo FAILED: Inspector chain stopped
echo ============================================
exit /b 1
