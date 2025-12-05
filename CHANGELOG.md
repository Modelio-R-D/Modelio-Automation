# Changelog

All notable changes to this project will be documented in this file.

## [v2.2] - December 2025

### Fixed
- **Data Association semantics**: Corrected `StartingActivity`/`EndingActivity` and `SourceRef`/`TargetRef` settings for proper BPMN compliance
  - `output`: Sets `StartingActivity = Task`, `TargetRef = DataObject`
  - `input`: Sets `EndingActivity = Task`, `SourceRef = DataObject`

### Changed
- **Lane-by-lane positioning**: Data objects are now positioned lane-by-lane (top to bottom) to handle Modelio's automatic lane expansion when data objects extend beyond boundaries

---

## [v2.1] - December 2025

### Added
- **Data Objects**: New `DATA_OBJECT` element type for representing documents and data in processes
- **Data Associations**: Connect tasks to data objects with `input`/`output` direction
- `data_objects` configuration section: `(name, lane, column, position)`
- `data_associations` configuration section: `(source, target, direction)`
- New configuration options:
  - `DATA_WIDTH` (default: 40) - Width of data objects
  - `DATA_HEIGHT` (default: 50) - Height of data objects
  - `DATA_OFFSET_X` (default: 20) - X offset from column center
  - `DATA_OFFSET_Y` (default: 80) - Y offset from lane center (positive = below)
- Position option: `"above"` or `"below"` for data object placement relative to tasks

### Documentation
- Updated `CLAUDE_INSTRUCTIONS.md` to v7.1 with data object examples
- Updated `API_REFERENCE.md` with complete data object/association documentation

---

## [v2.0] - December 2025

### Added
- **Two-file architecture**: Separates reusable helper library from process configuration
- `BPMN_Helpers.py` - Standalone helper library to install once in Modelio macros folder
- `createBPMNFromConfig()` - Single function to create entire process from configuration dict
- Element type constants (`START`, `END`, `USER_TASK`, `SERVICE_TASK`, `MANUAL_TASK`, `EXCLUSIVE_GW`, `PARALLEL_GW`, `MESSAGE_START`, `MESSAGE_END`, `TIMER_START`)
- Configuration-based approach with `CONFIG` dictionary
- Support for Claude, ChatGPT, Gemini, and LM Studio/Qwen

### Changed
- AI now generates ~50-100 lines of configuration instead of 500+ lines of full scripts
- Faster generation, fewer syntax errors, easier debugging
- Process scripts use `execfile()` to load helper library

### Documentation
- Added `docs/QUICK_START.md` - Step-by-step setup guide
- Added `docs/API_REFERENCE.md` - Complete configuration reference
- Added `docs/APPROACHES.md` - Comparison of single-file vs two-file approaches

---

## Single-File Version History

The following versions used a single-file approach where all helper functions were included inline in each generated script.

## [v0.9.1] - December 2025

### Added
- Guards for gateway conditions (displayed on sequence flows)

## [v0.9.0] - December 2025

### Added
- Configurable task dimensions (`TASK_WIDTH`, `TASK_HEIGHT`)
- Tasks are resized to ensure text fits properly
- Increased default `SPACING` to 150 for better readability

### Changed
- Events and gateways keep their original dimensions
- Log output now shows element dimensions

## [v0.8.3] - December 2025

### Fixed
- **Critical fix**: Manual unmask now works correctly by placing elements at the Y position inside their lane
- Unmask at (0,0) was failing - must unmask inside the correct lane

### Added
- Lane Y position calculation for manual unmask
- Detailed unmask logging with lane name and Y position

## [v0.8.2] - December 2025

### Added
- Manual unmask fallback for elements not auto-unmasked
- Automatic retry for missing elements after wait timeout

## [v0.8.1] - December 2025

### Added
- Detailed attempt logging during wait phase
- Shows found/missing elements count per attempt
- Lists missing element names (truncated to 12 chars)

## [v0.8.0] - December 2025

### Added
- Discovery: Modelio auto-unmasks elements when diagram is created
- Wait mechanism to check for element availability
- No longer need to manually call unmask() for initial display

### Changed
- Removed explicit unmask calls for all elements
- Added polling loop to wait for elements

## [v0.7.0] - November 2025

### Added
- Detailed reposition logging
- Lane change detection with before/after comparison
- `*** LANE CHANGED ***` markers in output

## [v0.6.0] - November 2025

### Added
- Lane change detection during repositioning
- Comparison of lane bounds before and after each move

## [v0.5.0] - November 2025

### Fixed
- Read lane Y positions once before repositioning
- Use fixed Y values to avoid lane drift

## [v0.3.0] - November 2025

### Added
- Complete BPMN template with all helper functions
- Support for all common BPMN element types
- Message and Timer start/end events
- `createBPMNDiagram()` function with automatic layout

## [v0.2.0-single] - November 2025

### Added
- Initial template structure
- Basic BPMN element creation functions
- Lane and flow support

---

## Key Discoveries

### Data Association Semantics (v7.1)

BPMN data associations have specific semantics:

| Direction | Arrow | BPMN Properties |
|-----------|-------|-----------------|
| `output` | Task → Data | `StartingActivity=Task`, `TargetRef=Data` |
| `input` | Data → Task | `SourceRef=Data`, `EndingActivity=Task` |

Typical pattern for data flowing between tasks:
```
Task A --(output)--> Data Object --(input)--> Task B
```

### Lane Expansion with Data Objects (v7.1)

When data objects are positioned below/above tasks, they may extend beyond lane boundaries. Modelio auto-expands lanes to accommodate this, which shifts subsequent lanes down. Solution: position data objects lane-by-lane and re-read lane coordinates after each lane.

### Auto-Unmask Behavior (v0.8.0)

Modelio automatically unmasks elements when a diagram is created, but:
- Auto-unmask is **non-deterministic** - sometimes all elements appear, sometimes only partial
- Waiting **does not reliably help** - Modelio appears to freeze in some state
- Solution: Quick check (3 attempts, 50ms) then manual unmask fallback

### Lane-Aware Unmask (v0.8.3)

Manual unmask must be done at the correct Y position:

```python
# WRONG - will fail
diagramHandle.unmask(elem, 0, 0)

# CORRECT - inside the lane
diagramHandle.unmask(elem, 100, laneY[laneName])
```

### Two-File Benefits (v2.0)

| Metric | Single-File | Two-File |
|--------|-------------|----------|
| Lines per script | 500-700 | 50-150 |
| AI generation time | ~45 sec | ~15 sec |
| Syntax error rate | ~30% | ~0% |
| Bug fix effort | Edit every file | Edit once |