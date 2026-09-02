abstract class ReturnState {
    String name;
    ReturnState(String name) { this.name = name; }

    void updateReason(ReturnRequest request, String reason) { invalid("updateReason"); }
    void approve(ReturnRequest request) { invalid("approve"); }
    void reject(ReturnRequest request) { invalid("reject"); }
    void cancel(ReturnRequest request) { invalid("cancel"); }
    void itemDelivered(ReturnRequest request) { invalid("itemDelivered"); }
    void inspect(ReturnRequest request, boolean eligible) { invalid("inspect"); }
    void refundSuccessful(ReturnRequest request) { invalid("refundSuccessful"); }
    void refundFailed(ReturnRequest request) { invalid("refundFailed"); }

    void invalid(String action) {
        System.out.println("Cannot perform " + action + " in " + name + " state");
    }
}

class RequestedState extends ReturnState {
    RequestedState() { super("Requested"); }
    void updateReason(ReturnRequest request, String reason) {
        request.setReason(reason);
        System.out.println("Reason updated to: " + reason);
    }
    void approve(ReturnRequest request) {
        System.out.println("Request approved");
        request.setState(new ApprovedState());
    }
    void reject(ReturnRequest request) {
        System.out.println("Request rejected");
        request.setState(new RejectedState());
    }
    void cancel(ReturnRequest request) {
        System.out.println("Request cancelled");
        request.setState(new CancelledState());
    }
}

class ApprovedState extends ReturnState {
    ApprovedState() { super("Approved"); }
    void cancel(ReturnRequest request) {
        System.out.println("Request cancelled");
        request.setState(new CancelledState());
    }
    void itemDelivered(ReturnRequest request) {
        System.out.println("Item marked as delivered");
        request.setState(new DeliveredState());
    }
}

class DeliveredState extends ReturnState {
    DeliveredState() { super("Delivered"); }
    void inspect(ReturnRequest request, boolean eligible) {
        if (eligible) {
            System.out.println("Item passed inspection, processing refund");
            request.setState(new ProcessingRefundState());
        } else {
            System.out.println("Item failed inspection, request rejected");
            request.setState(new RejectedState());
        }
    }
}

class ProcessingRefundState extends ReturnState {
    ProcessingRefundState() { super("Processing Refund"); }
    void refundSuccessful(ReturnRequest request) {
        System.out.println("Refund successful");
        request.setState(new RefundedState());
    }
    void refundFailed(ReturnRequest request) {
        System.out.println("Refund failed, can be retried");
    }
}

class RefundedState extends ReturnState {
    RefundedState() { super("Refunded"); }
}

class RejectedState extends ReturnState {
    RejectedState() { super("Rejected"); }
}

class CancelledState extends ReturnState {
    CancelledState() { super("Cancelled"); }
}

class ReturnRequest {
    private ReturnState state = new RequestedState();
    private String reason;

    void setState(ReturnState state) { this.state = state; }
    void setReason(String reason) { this.reason = reason; }
    String status() { return state.name; }

    void updateReason(String reason) { state.updateReason(this, reason); }
    void approve() { state.approve(this); }
    void reject() { state.reject(this); }
    void cancel() { state.cancel(this); }
    void itemDelivered() { state.itemDelivered(this); }
    void inspect(boolean eligible) { state.inspect(this, eligible); }
    void refundSuccessful() { state.refundSuccessful(this); }
    void refundFailed() { state.refundFailed(this); }
}

public class _23B1 {
    public static void main(String[] args) {
        ReturnRequest request = new ReturnRequest();
        System.out.println("Status: " + request.status());

        request.updateReason("Wrong size");
        request.approve();
        System.out.println("Status: " + request.status());

        request.updateReason("Trying to change after approval");
        request.itemDelivered();
        System.out.println("Status: " + request.status());

        request.cancel();
        request.inspect(true);
        System.out.println("Status: " + request.status());

        request.refundFailed();
        request.refundSuccessful();
        System.out.println("Status: " + request.status());

        request.approve();

        System.out.println();
        ReturnRequest request2 = new ReturnRequest();
        request2.approve();
        request2.itemDelivered();
        request2.inspect(false);
        System.out.println("Status: " + request2.status());
    }
}