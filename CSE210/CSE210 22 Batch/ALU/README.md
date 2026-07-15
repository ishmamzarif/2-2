# ALU Truth Table Verification

## Steps

1. In Logisim:

   * Go to **Project → Analyze Circuit**
   * Generate the full truth table
   * Copy the table

2. Create `truth_table.txt` and paste the copied table into it.

3. Run:

```bash
python3 truth_table_tester.py
```

4. Check results in `alu_errors.txt`.

## Optional

Generate HTML error report:

```bash
python3 table_to_html.py
```
