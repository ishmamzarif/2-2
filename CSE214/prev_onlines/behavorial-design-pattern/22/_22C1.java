// i can have a patient p class here
// with fields for name, id, temp, bp
// it is passed to the visit function
// but ekhane dekhanor dorkar nai ar
abstract class HospitalTemplate {
    public final void visit() {
        System.out.println("Registering patient name, assigning id");
        System.out.println("Temperature and blood pressure");
        assess();
        treatment();
        System.out.println("Discharge summary: patient discharged");
    }
    abstract void assess();
    abstract void treatment();
}

class GeneralDepartment extends HospitalTemplate {
    void assess() {
        System.out.println("Doctor performs normal diagnosis");
    }
    void treatment() {
        System.out.println("Prescribe standard medicine");
    }
}

class PediatricsDepartment extends HospitalTemplate {
    void assess() {
        System.out.println("Doctor checks symptoms by ensuring child comfort level");
    }
    void treatment() {
        System.out.println("Give child-safe medicine, friendly reassurance message");
    }
}

class EmergencyDepartment extends HospitalTemplate {
    void assess() {
        System.out.println("Quick triage check (urgent/non-urgent)");
    }
    void treatment() {
        System.out.println("Immediate emergency procedure");
    }
}

public class _22C1 {
    public static void main(String[] args) {
        System.out.println("General Department:");
        new GeneralDepartment().visit();

        System.out.println("Pediatrics Department:");
        new PediatricsDepartment().visit();

        System.out.println("Emergency Department:");
        new EmergencyDepartment().visit();
    }
}