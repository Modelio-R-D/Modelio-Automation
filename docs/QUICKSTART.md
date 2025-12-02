# Quick Start Guide

This guide will help you create your first BPMN diagram using Claude AI and Modelio.

## Prerequisites

1. **Modelio 5.0+** installed ([download here](https://www.modelio.org/downloads.html))
2. Access to **Claude** ([claude.ai](https://claude.ai/))

## Step 1: Set Up Claude Project

1. Go to [claude.ai](https://claude.ai/)
2. Create a new **Project** (click "Projects" in the sidebar)
3. In project settings, add **Custom Instructions**
4. Copy the entire contents of [`CLAUDE_INSTRUCTIONS.md`](../CLAUDE_INSTRUCTIONS.md) into the custom instructions
5. Save the project

## Step 2: Describe Your Process

Start a conversation with Claude in your project. Describe your business process in natural language:

```
Create a BPMN diagram for a simple order fulfillment process:

Lanes:
- Customer
- Sales
- Warehouse

Process:
1. Customer places an order
2. Sales receives and validates the order
3. If valid, Sales confirms the order
4. Warehouse picks and ships the items
5. Customer receives the delivery

Include appropriate gateways for the validation decision.
```

## Step 3: Get the Generated Macro

Claude will generate a complete Python macro for Modelio. The output will look something like:

```python
#
# OrderFulfillmentProcess.py
#
# Description: BPMN process for order fulfillment
# Applicable on: Package
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
# ... rest of imports and code
```

## Step 4: Run in Modelio

1. **Copy** the entire generated script
2. Open **Modelio**
3. Create or open a project
4. **Select a Package** in the model explorer (right-click > Create > Package if needed)
5. Go to **Script > Run Script** (or press the script button)
6. **Paste** the script
7. Click **Run**

## Step 5: View Your Diagram

1. In the model explorer, expand your package
2. Find the newly created process (e.g., "OrderFulfillment_12345")
3. Double-click the diagram to open it
4. You should see your BPMN diagram with all lanes, elements, and flows!

## Customizing the Output

### Change Element Sizes

Edit the configuration at the top of the generated script:

```python
TASK_WIDTH = 120    # Make tasks wider
TASK_HEIGHT = 60    # Make tasks taller
SPACING = 150       # More space between elements
```

### Adjust Layout

Modify the `elementLayout` dictionary to change column positions:

```python
elementLayout = {
    "Place Order": (0, "Customer"),      # Column 0
    "Receive Order": (1, "Sales"),       # Column 1
    "Validate Order": (2, "Sales"),      # Column 2
    # ...
}
```

## Troubleshooting

### Script doesn't run
- Make sure you've selected a **Package** before running
- Check the Modelio console for error messages

### Elements not visible
- The script handles this automatically with manual unmask fallback
- Check the console output for `[Unmask]` messages

### Text is cut off
- Increase `TASK_WIDTH` and `TASK_HEIGHT` in the configuration
- Increase `SPACING` if elements overlap

### Unicode errors
- Ensure the script uses only ASCII characters
- Avoid special characters like arrows (→) or boxes (▭) in print statements

## Next Steps

- Check out the [ExpenseApprovalProcess.py](../examples/ExpenseApprovalProcess.py) for a complete example
- Read the [BPMN_Template.py](../templates/BPMN_Template.py) to understand all available functions
- Review [CLAUDE_INSTRUCTIONS.md](../CLAUDE_INSTRUCTIONS.md) for the full list of supported elements

## Tips for Better Results

1. **Be specific** about lane names and their roles
2. **Describe decisions** clearly (e.g., "if approved" → Exclusive Gateway)
3. **Mention parallel activities** for Parallel Gateways
4. **Include error paths** and exception handling
5. **Name your elements** descriptively (Claude will use these names)
