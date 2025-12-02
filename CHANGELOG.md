# Changelog

All notable changes to this project will be documented in this file.

## [v9.0] - December 2025

### Added
- Configurable task dimensions (TASK_WIDTH, TASK_HEIGHT)
- Tasks are resized to ensure text fits properly
- Increased default SPACING to 150 for better readability

### Changed
- Events and gateways keep their original dimensions
- Log output now shows element dimensions

## [v8.3] - December 2025

### Fixed
- **Critical fix**: Manual unmask now works correctly by placing elements at the Y position inside their lane
- Unmask at (0,0) was failing - must unmask inside the correct lane

### Added
- Lane Y position calculation for manual unmask
- Detailed unmask logging with lane name and Y position

## [v8.2] - December 2025

### Added
- Manual unmask fallback for elements not auto-unmasked
- Automatic retry for missing elements after wait timeout

## [v8.1] - December 2025

### Added
- Detailed attempt logging during wait phase
- Shows found/missing elements count per attempt
- Lists missing element names (truncated to 12 chars)

## [v8.0] - December 2025

### Added
- Discovery: Modelio auto-unmasks elements when diagram is created
- Wait mechanism to check for element availability
- No longer need to manually call unmask() for initial display

### Changed
- Removed explicit unmask calls for all elements
- Added polling loop to wait for elements

## [v7.0] - December 2025

### Added
- Detailed reposition logging
- Lane change detection with before/after comparison
- `*** LANE CHANGED ***` markers in output

## [v6.0] - December 2025

### Added
- Lane change detection during repositioning
- Comparison of lane bounds before and after each move

## [v5.0] - December 2025

### Fixed
- Read lane Y positions once before repositioning
- Use fixed Y values to avoid lane drift

## [v3.0] - December 2025

### Added
- Complete BPMN template with all helper functions
- Support for all common BPMN element types
- Message and Timer start/end events
- createBPMNDiagram() function with automatic layout

## [v2.0] - November 2025

### Added
- Initial template structure
- Basic BPMN element creation functions
- Lane and flow support

## Key Discoveries

### Auto-Unmask Behavior (v8.0)
Modelio automatically unmasks elements when a diagram is created, but:
- Auto-unmask is **random** - sometimes all elements, sometimes partial
- Waiting **does not help** - Modelio appears to freeze in some state
- Solution: Quick check (3 attempts, 50ms) then manual unmask fallback

### Lane-Aware Unmask (v8.3)
Manual unmask must be done at the correct Y position:
```python
# WRONG - will fail
diagramHandle.unmask(elem, 0, 0)

# CORRECT - inside the lane
diagramHandle.unmask(elem, 100, laneY[laneName])
```
