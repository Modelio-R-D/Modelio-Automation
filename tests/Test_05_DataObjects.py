#
# Test_05_DataObjects.py
#
# Description:
#   Test Case 5: Process with data objects and data associations
#   Tests: DATA_OBJECT, data_objects config, data_associations config
#
# Data Flow:
#   Write Document -> Draft Document -> Submit for Review
#   Submit for Review -> Submitted Document -> Review Document  
#   Review Document -> Review Comments -> Add Comments
#
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Test05_DataObjects",
    
    "lanes": ["Author", "Reviewer"],
    
    "elements": [
        # Author lane
        ("Start",             START,     "Author"),
        ("Write Document",    USER_TASK, "Author"),
        ("Submit for Review", USER_TASK, "Author"),
        
        # Reviewer lane
        ("Review Document",   USER_TASK, "Reviewer"),
        ("Add Comments",      USER_TASK, "Reviewer"),
        ("End",               END,       "Reviewer"),
    ],
    
    # Data Objects: (name, lane, column, position)
    # Place below the task that outputs them (same column as source task)
    "data_objects": [
        ("Draft Document",     "Author",   1, "below"),   # Below Write Document
        ("Submitted Document", "Author",   2, "below"),   # Below Submit for Review
        ("Review Comments",    "Reviewer", 3, "below"),   # Below Review Document
    ],
    
    # Data Associations: (source, target, direction)
    # direction: "input" (data->task) or "output" (task->data)
    "data_associations": [
        # Write produces draft, draft goes to Submit
        ("Write Document",      "Draft Document",      "output"),
        ("Draft Document",      "Submit for Review",   "input"),
        
        # Submit produces submitted doc, goes to Review
        ("Submit for Review",   "Submitted Document",  "output"),
        ("Submitted Document",  "Review Document",     "input"),
        
        # Review produces comments, comments go to Add Comments
        ("Review Document",     "Review Comments",     "output"),
        ("Review Comments",     "Add Comments",        "input"),
    ],
    
    "flows": [
        ("Start",             "Write Document",    ""),
        ("Write Document",    "Submit for Review", ""),
        ("Submit for Review", "Review Document",   ""),
        ("Review Document",   "Add Comments",      ""),
        ("Add Comments",      "End",               ""),
    ],
    
    "layout": {
        "Start":             0,
        "Write Document":    1,
        "Submit for Review": 2,
        "Review Document":   3,
        "Add Comments":      4,
        "End":               5,
    },
}

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Select a Package."
else:
    print "ERROR: Select a Package first."
