import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

interface Mediator {
    void requestInvestigation(String patientId, String type);
    void submitResult(String patientId, String type, String result);
}

abstract class InvestigationUnit {
    final String type;
    final String label;
    private final Mediator mediator;

    InvestigationUnit(Mediator mediator, String type, String label) {
        this.mediator = mediator;
        this.type = type;
        this.label = label;
    }

    abstract boolean isUrgent(String result);

    void performInvestigation(String patientId, String result) {
        mediator.submitResult(patientId, type, result);
    }
}

class PathologyLab extends InvestigationUnit {
    PathologyLab(Mediator mediator) { super(mediator, "Pathology", "Pathology test"); }
    boolean isUrgent(String result) { return result.equals("CRITICAL"); }
}

class RadiologyUnit extends InvestigationUnit {
    RadiologyUnit(Mediator mediator) { super(mediator, "Radiology", "Radiology investigation"); }
    boolean isUrgent(String result) { return result.equals("NOT OK"); }
}

class Doctor {
    private final Mediator mediator;
    Doctor(Mediator mediator) { this.mediator = mediator; }

    void requestInvestigations(String patientId, String... types) {
        for (String type : types) {
            mediator.requestInvestigation(patientId, type);
        }
    }

    void notifyUrgent(String patientId, String type, String result) {
        System.out.println("URGENT notification sent to Doctor.");
    }

    void notifyComplete(String patientId) {
        System.out.println("Complete results sent to Doctor.");
    }
}

class PatientRecord {
    Set<String> requested = new HashSet<>();
    Map<String, String> results = new HashMap<>();
}

class EmergencyCenter implements Mediator {
    private Doctor doctor;
    private final Map<String, InvestigationUnit> units = new HashMap<>();
    private final Map<String, PatientRecord> records = new HashMap<>();

    void setDoctor(Doctor doctor) { this.doctor = doctor; }
    void registerUnit(InvestigationUnit unit) { units.put(unit.type, unit); }

    public void requestInvestigation(String patientId, String type) {
        records.computeIfAbsent(patientId, k -> new PatientRecord()).requested.add(type);
        System.out.println(units.get(type).label + " requested for Patient " + patientId + ".");
    }

    public void submitResult(String patientId, String type, String result) {
        PatientRecord record = records.get(patientId);
        record.results.put(type, result);
        System.out.println(type + " result received for Patient " + patientId + ": " + result);

        InvestigationUnit unit = units.get(type);
        if (unit.isUrgent(result)) {
            doctor.notifyUrgent(patientId, type, result);
            System.out.println("URGENT notification sent to Patient " + patientId + ".");
        }

        if (record.results.keySet().containsAll(record.requested)) {
            System.out.println("All requested investigations completed for Patient " + patientId + ".");
            doctor.notifyComplete(patientId);
            System.out.println("Complete results sent to Patient " + patientId + ".");
        }
    }
}

public class _23C1 {
    public static void main(String[] args) {
        EmergencyCenter center = new EmergencyCenter();
        Doctor doctor = new Doctor(center);
        center.setDoctor(doctor);

        PathologyLab pathologyLab = new PathologyLab(center);
        RadiologyUnit radiologyUnit = new RadiologyUnit(center);
        center.registerUnit(pathologyLab);
        center.registerUnit(radiologyUnit);

        doctor.requestInvestigations("P101", "Pathology", "Radiology");

        pathologyLab.performInvestigation("P101", "CRITICAL");
        radiologyUnit.performInvestigation("P101", "OK");

        System.out.println();

        doctor.requestInvestigations("P102", "Radiology");
        radiologyUnit.performInvestigation("P102", "NOT OK");
    }
}