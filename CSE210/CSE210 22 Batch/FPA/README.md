## How to Test

0. Go to the directory "./Testing"

1. Run the `fpa_tester.py` to generate a truth table with **N** number of rows.  
   - The table will be saved as a `.txt` file.

2. Open `FPA.circ` in **Logisim-evolution**.

3. Go to the subcircuit `Circuit_Tester`.

4. Click **Simulate → Test Vector → Load Vector**.

5. Load the generated `.txt` file.  
   - It should run automatically. If not, press **Run**.

6. **Test Results:**  
   - Failed tests will appear first.  
   - Passed tests will appear after.
