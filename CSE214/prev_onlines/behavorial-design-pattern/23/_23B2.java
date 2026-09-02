package behavioural;

import java.util.*;

class Task {
    private String id;
    private int start;
    private int end;
    private String priority;

    public Task(String id, int start, int end, String priority) {
        this.id = id;
        this.start = start;
        this.end = end;
        this.priority = priority;
    }

    public String getId() {
        return id;
    }

    public int getStart() {
        return start;
    }

    public int getEnd() {
        return end;
    }

    public String getPriority() {
        return priority;
    }

    public int getExecutionTime() {
        return end - start;
    }

    @Override
    public String toString() {
        return "task [id=" + id + ", start=" + start + ", end=" + end + ", priority=" + priority
                + ", getExecutionTime()=" + getExecutionTime() + "]";
    }

}

interface SchedulingStrategy {
    Task selectTask(List<Task> tasks);

    String getName();
}

class FCFS implements SchedulingStrategy {

    @Override
    public Task selectTask(List<Task> tasks) {
        Task selectedTask = tasks.get(0);
        for (Task task : tasks) {
            if (task.getStart() < selectedTask.getStart()) {
                selectedTask = task;
            }
        }
        return selectedTask;
    }

    @Override
    public String getName() {
        return "First Come, First Served";
    }
}

class PriorityScheduling implements SchedulingStrategy {

    private int getPriorityValue(String priority) {

        if (priority.equalsIgnoreCase("HIGH")) {

            return 3;

        }

        if (priority.equalsIgnoreCase("MEDIUM")) {

            return 2;

        }

        return 1; // LOW

    }

    @Override
    public Task selectTask(List<Task> tasks) {
        Task selected = tasks.get(0);
        for (Task task : tasks) {
            int currentPriority = getPriorityValue(task.getPriority());
            int selectedPriority = getPriorityValue(selected.getPriority());
            if (currentPriority > selectedPriority) {
                selected = task;
            } else if (currentPriority == selectedPriority && task.getStart() < selected.getStart()) {
                selected = task;
            }
        }
        return selected;
    }

    @Override
    public String getName() {
        return "Priority Scheduling";
    }
}

class SJF implements SchedulingStrategy {

    @Override
    public Task selectTask(List<Task> tasks) {
        Task selectedTask = tasks.get(0);
        for (Task task : tasks) {
            if (task.getExecutionTime() < selectedTask.getExecutionTime()) {
                selectedTask = task;
            }
        }
        return selectedTask;
    }

    @Override
    public String getName() {
        return "Shortest Job First";
    }
}

enum Policy {
    FCFS, PRIORITY, SJF
}

class TaskScheduler {
    private List<Task> waitingtasks;
    private Policy preferredPolicy;

    private SchedulingStrategy fcfs;
    private SchedulingStrategy ps;
    private SchedulingStrategy sjf;

    public TaskScheduler(Policy preferredPolicy) {
        this.waitingtasks = new ArrayList<>();
        this.preferredPolicy = preferredPolicy;
        this.fcfs = new FCFS();
        this.ps = new PriorityScheduling();
        this.sjf = new SJF();
    }

    public void addTask(Task task) {

        waitingtasks.add(task);
        System.out.println("Added: " + task);

    }

    public void setPreferredPolicy(Policy policy) {

        this.preferredPolicy = policy;
        System.out.println(

                "Preferred policy changed to: " + policy

        );

    }

    private SchedulingStrategy determinePolicy(){
        for(Task task: waitingtasks){
            if(task.getPriority().equalsIgnoreCase("High")){
                return ps;
            }
        }
        int count=0;
        for(Task task: waitingtasks){
            if (task.getExecutionTime()<=3) {
                count++;
            }
        }
        if (count>=3) {
            return sjf;
        }
        if (preferredPolicy==Policy.FCFS) {
            return fcfs;
        }
        if (preferredPolicy==Policy.PRIORITY) {
            return ps;
        }
        return sjf;
    }

        public void executeNextTask() {

        if (waitingtasks.isEmpty()) {

            System.out.println("No tasks waiting.");

            return;

        }

        // Determine policy AGAIN

        // before every task

        SchedulingStrategy strategy = determinePolicy();

        // Select task using selected strategy

        Task selectedTask = strategy.selectTask(waitingtasks);

        // Remove from queue

        waitingtasks.remove(selectedTask);

        // Execute

        System.out.println(

            "Executing: " + selectedTask.getId()

        );

        System.out.println(

            "Policy Used: " + strategy.getName()

        );

        System.out.println(

            "Execution Time: " +

            selectedTask.getExecutionTime()

        );

        System.out.println("----------------------------");

    }

    public void executeAll() {

        while (!waitingtasks.isEmpty()) {

            executeNextTask();

        }

    }
}

public class _23B2 {
    public static void main(String[] args) {
        TaskScheduler scheduler =

                new TaskScheduler(Policy.FCFS);

        // Add tasks

        scheduler.addTask(

            new Task("T1", 0, 8, "MEDIUM")

        );

        scheduler.addTask(

            new Task("T2", 1, 4, "LOW")

        );

        scheduler.addTask(

            new Task("T3", 2, 4, "MEDIUM")

        );

        scheduler.addTask(

            new Task("T4", 3, 4, "LOW")

        );

        scheduler.addTask(

            new Task("T5", 4, 9, "HIGH")

        );

        System.out.println("\n=== EXECUTION ===");

        scheduler.executeAll();

    
    }
}