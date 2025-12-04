# BPMN Helpers API Reference

This document describes all element types, configuration options, and functions available in `BPMN_Helpers.py`.

## Element Type Constants

Use these constants in the `elements` section of your configuration.

### Start Events

| Constant | Visual | Description |
|----------|--------|-------------|
| `START` | ○ (green circle) | Standard process start point |
| `MESSAGE_START` | ✉○ (envelope + green circle) | Process triggered by receiving a message |
| `TIMER_START` | ⏰○ (clock + green circle) | Process triggered by timer/schedule |

### End Events

| Constant | Visual | Description |
|----------|--------|-------------|
| `END` | ● (red circle) | Standard process end point |
| `MESSAGE_END` | ✉● (envelope + red circle) | End event that sends a message |

### Tasks

| Constant | Visual | Description |
|----------|--------|-------------|
| `USER_TASK` | 👤▭ (person icon + rectangle) | Human activity requiring IT interaction |
| `SERVICE_TASK` | ⚙▭ (gear icon + rectangle) | Automated/system task |
| `MANUAL_TASK` | ✋▭ (hand icon + rectangle) | Physical task without IT involvement |

### Gateways

| Constant | Visual | Description |
|----------|--------|-------------|
| `EXCLUSIVE_GW` | ◇✕ (diamond with X) | XOR - exactly one outgoing path chosen |
| `PARALLEL_GW` | ◇+ (diamond with +) | AND - all paths execute in parallel |

## Configuration Object

The `CONFIG` dictionary defines your entire process. Here's the complete structure:

```python
CONFIG = {
    # REQUIRED FIELDS
    "name": "ProcessName",           # Base name (gets unique suffix added)
    "lanes": ["Lane1", "Lane2"],     # Swim lanes, top to bottom order
    "elements": [...],               # List of (name, type, lane) tuples
    "flows": [...],                  # List of (source, target, guard) tuples
    "layout": {...},                 # Dict mapping element names to columns
    
    # OPTIONAL FIELDS (with defaults)
    "SPACING": 150,                  # Horizontal distance between columns (pixels)
    "START_X": 80,                   # X coordinate of column 0
    "TASK_WIDTH": 120,               # Width of task rectangles
    "TASK_HEIGHT": 60,               # Height of task rectangles
    "WAIT_TIME_MS": 50,              # Milliseconds between unmask checks
    "MAX_ATTEMPTS": 3,               # Maximum unmask retry attempts
}
```

### Elements List

Format: `(name, type, lane)`

```python
"elements": [
    ("Submit Request", START, "Requester"),
    ("Review Request", USER_TASK, "Reviewer"),
    ("Decision", EXCLUSIVE_GW, "Reviewer"),
    ("Approved", END, "Requester"),
    ("Rejected", END, "Requester"),
]
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Display name and unique identifier |
| `type` | constant | One of the element type constants |
| `lane` | string | Must exactly match a lane in the `lanes` list |

### Flows List

Format: `(source, target, guard)`

```python
"flows": [
    ("Submit Request", "Review Request", ""),
    ("Review Request", "Decision", ""),
    ("Decision", "Approved", "Yes"),
    ("Decision", "Rejected", "No"),
]
```

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Name of source element (must match exactly) |
| `target` | string | Name of target element (must match exactly) |
| `guard` | string | Condition label for the flow (empty string if none) |

**Guard usage**:
- Empty string `""` for unconditional flows
- Text label like `"Yes"`, `"No"`, `"Approved"` for conditional flows
- Commonly used on gateway outflows

### Layout Dictionary

Format: `{element_name: column_index}`

```python
"layout": {
    "Submit Request": 0,
    "Review Request": 1,
    "Decision": 2,
    "Approved": 3,
    "Rejected": 3,  # Same column as Approved (different lanes)
}
```

| Field | Type | Description |
|-------|------|-------------|
| `element_name` | string | Must match element name exactly |
| `column_index` | integer | Horizontal position (0 = leftmost) |

**Layout tips**:
- Column indices can have gaps (0, 1, 5, 10 is fine)
- Elements in the same lane at the same column will overlap
- Elements in different lanes can share a column (parallel positioning)
- Events and gateways are typically single columns
- Plan complex processes on paper first

## Main Function

### `createBPMNFromConfig(parentPackage, config)`

Creates a complete BPMN process diagram from a configuration dictionary.

**Parameters**:
- `parentPackage` - Modelio Package element where the process will be created
- `config` - Dictionary following the CONFIG structure above

**Returns**: The created BpmnProcess element

**Example**:
```python
from org.modelio.metamodel.uml.statik import Package

execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = { ... }

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        process = createBPMNFromConfig(element, CONFIG)
        print "Created: " + process.getName()
```

## Internal Functions (Advanced)

These functions are used internally but can be called directly for custom scenarios.

### Element Creation

```python
_createStartEvent(process, name)       # Create standard start event
_createMessageStartEvent(process, name) # Create message start event
_createTimerStartEvent(process, name)   # Create timer start event
_createEndEvent(process, name)          # Create standard end event
_createMessageEndEvent(process, name)   # Create message end event
_createUserTask(process, name)          # Create user task
_createServiceTask(process, name)       # Create service task
_createManualTask(process, name)        # Create manual task
_createExclusiveGateway(process, name)  # Create exclusive gateway
_createParallelGateway(process, name)   # Create parallel gateway
```

### Lane Management

```python
_createLane(laneSet, name)              # Create a lane in a lane set
_addToLane(element, lane)               # Assign element to lane
```

### Flow Creation

```python
_createSequenceFlow(process, source, target, guard="")
```

### Diagram Utilities

```python
_getGraphics(diagramHandle, element)    # Get diagram graphics for element
_getBounds(diagramHandle, element)      # Get element bounds as dict
_getLaneCenterY(diagramHandle, lane)    # Get Y coordinate for lane center
```

## Configuration Examples

### Minimal Process

```python
CONFIG = {
    "name": "Minimal",
    "lanes": ["User"],
    "elements": [
        ("Start", START, "User"),
        ("End", END, "User"),
    ],
    "flows": [
        ("Start", "End", ""),
    ],
    "layout": {
        "Start": 0,
        "End": 1,
    },
}
```

### Decision Process

```python
CONFIG = {
    "name": "Decision",
    "lanes": ["User", "System"],
    "elements": [
        ("Request", START, "User"),
        ("Process", SERVICE_TASK, "System"),
        ("Check", EXCLUSIVE_GW, "System"),
        ("Success", END, "User"),
        ("Failure", END, "User"),
    ],
    "flows": [
        ("Request", "Process", ""),
        ("Process", "Check", ""),
        ("Check", "Success", "Valid"),
        ("Check", "Failure", "Invalid"),
    ],
    "layout": {
        "Request": 0,
        "Process": 1,
        "Check": 2,
        "Success": 3,
        "Failure": 3,
    },
}
```

### Parallel Execution

```python
CONFIG = {
    "name": "Parallel",
    "lanes": ["Coordinator", "Team A", "Team B"],
    "elements": [
        ("Start", START, "Coordinator"),
        ("Split", PARALLEL_GW, "Coordinator"),
        ("Task A", USER_TASK, "Team A"),
        ("Task B", USER_TASK, "Team B"),
        ("Join", PARALLEL_GW, "Coordinator"),
        ("End", END, "Coordinator"),
    ],
    "flows": [
        ("Start", "Split", ""),
        ("Split", "Task A", ""),
        ("Split", "Task B", ""),
        ("Task A", "Join", ""),
        ("Task B", "Join", ""),
        ("Join", "End", ""),
    ],
    "layout": {
        "Start": 0,
        "Split": 1,
        "Task A": 2,
        "Task B": 2,
        "Join": 3,
        "End": 4,
    },
}
```

## Error Handling

The helper library prints diagnostic messages during execution:

```
==================================================================
BPMN PROCESS CREATION
==================================================================
Process Name: MyProcess_12345

== PHASE 1: CREATE PROCESS & LANES ==============================
[1] Process: MyProcess_12345
[2] Lanes: User, Admin

== PHASE 2: CREATE ELEMENTS =====================================
[3] User: 3 elements
[4] Admin: 2 elements
  Total: 5 elements

...
```

### Common Error Messages

| Message | Cause | Solution |
|---------|-------|----------|
| `ERROR: Unknown element type: X` | Invalid type constant | Use valid constant from list above |
| `ERROR: Please select a Package` | Wrong element selected | Select a Package in model explorer |
| `[Unmask] ... FAILED` | Element not displayed | Usually auto-resolves; check layout |

## Version History

- **v2.0** (December 2025): Complete rewrite with configuration-based approach
- **v1.x**: Original inline implementations
