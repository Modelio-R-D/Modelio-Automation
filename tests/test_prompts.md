# Test Prompts for Modelio BPMN Generation

Use these prompts to validate macro generation quality across increasing complexity.

---

## Level 1: Simple Process
**Test 1.1 – Leave Request**  
Prompt:
> Create a BPMN process for "Leave Request" with 2 lanes: Employee, Manager.  
> Employee: Start -> Submit Leave Request.  
> Manager: Review -> Approve/Reject gateway.  
> If approved: End (Approved) in Manager lane.  
> If rejected: End (Rejected) in Employee lane.

---

## Level 2: Complex Process
**Test 2.1 – Invoice Processing**  
Prompt:
> Create a BPMN process for "Invoice Processing" with 3 lanes: Vendor, Accounts Payable, Finance Manager.  
> Vendor submits invoice.  
> Accounts Payable validates invoice (gateway: valid/invalid).  
> If invalid: return to vendor, end.  
> If valid: Finance Manager approves (gateway: approve/reject).  
> If approved: Accounts Payable processes payment -> End.  
> If rejected: notify vendor -> End.

---

## Level 3: Medium (Multiple Tasks per Lane)
**Test 3.1 – Hiring Process**  
Prompt:
> Create a BPMN process for "Job Application" with 2 lanes: Candidate, HR.  
> Candidate submits application.  
> HR reviews application (gateway: Qualified/Unqualified).  
> If Unqualified: End Rejected.  
> If Qualified: HR schedules interview -> HR conducts interview -> End Complete.

**Test 3.2 – Order Processing**  
Prompt:
> Create a BPMN process for "Online Order" with 2 lanes: Customer, Warehouse.  
> Customer places order.  
> Warehouse checks stock (gateway: InStock/OutOfStock).  
> If OutOfStock: End Cancelled.  
> If InStock: Warehouse picks items -> Warehouse ships order -> End Shipped.

---

## Level 4: Three Lanes
**Test 4.1 – Expense Claim**  
Prompt:
> Create a BPMN process for "Expense Claim" with 3 lanes: Employee, Manager, Finance.  
> Employee submits expense.  
> Manager approves (gateway: Approved/Rejected).  
> If Rejected: End Rejected.  
> If Approved: Finance processes payment -> End Paid.

**Test 4.2 – Bug Report**  
Prompt:
> Create a BPMN process for "Bug Report" with 3 lanes: User, Developer, QA.  
> User reports bug.  
> Developer fixes bug.  
> QA tests fix (gateway: Pass/Fail).  
> If Fail: End Reopen.  
> If Pass: End Closed.

---

## Level 5: Multiple Gateways
**Test 5.1 – Loan Application**  
Prompt:
> Create a BPMN process for "Loan Application" with 3 lanes: Customer, Bank Clerk, Manager.  
> Customer submits application.  
> Bank Clerk checks documents (gateway: Complete/Incomplete).  
> If Incomplete: End Incomplete.  
> If Complete: Manager reviews (gateway: Approved/Rejected).  
> If Rejected: End Rejected.  
> If Approved: Bank Clerk issues loan -> End Approved.

**Test 5.2 – Invoice Processing (Reference)**  
Prompt:
> Create a BPMN process for "Invoice Processing" with 3 lanes: Vendor, Accounts Payable, Finance Manager.  
> Vendor submits invoice.  
> Accounts Payable validates (gateway: Valid/Invalid).  
> If Invalid: End Invalid.  
> If Valid: Finance Manager approves (gateway: Approved/Rejected).  
> If Approved: Accounts Payable processes payment -> End Paid.  
> If Rejected: Accounts Payable notifies vendor -> End Rejected.

---

## Level 6: Service Tasks (Automated)
**Test 6.1 – Email Notification**  
Prompt:
> Create a BPMN process for "Password Reset" with 2 lanes: User, System.  
> User requests reset (UserTask).  
> System generates token (ServiceTask).  
> System sends email (ServiceTask).  
> User sets new password (UserTask).  
> End.

**Test 6.2 – Mixed Tasks**  
Prompt:
> Create a BPMN process for "Order Confirmation" with 2 lanes: Customer, System.  
> Customer places order (UserTask).  
> System validates payment (ServiceTask) - gateway: Success/Failed.  
> If Failed: End Failed.  
> If Success: System sends confirmation (ServiceTask) -> End Complete.

---

## Testing Checklist
- Functions: Only `createUserTask(process, name)` — no extra params
- Gateways: Short names, e.g., "Valid?" not "Validation: Valid/Invalid"
- End events: No outgoing flows from End events
- Name matching: `flowDefs` names must equal `elementRefs` keys
- Guards: Simple labels, e.g., "Approved" not "(Guard: Approved)"

---

## Recommended Test Order
1. Test 1.1 (simplest)
2. Test 2.1 (adds gateway)
3. Test 4.1 (adds third lane)
4. Test 5.1 (multiple gateways)
