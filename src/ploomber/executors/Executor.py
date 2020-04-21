from ploomber.constants import TaskStatus


class Executor:
    """
    Abstract class for executors.

    *Executors API is subject to change*

    Executors handle task execution, they receive a dag as a parameter and
    call task.build() on each task. To iterate over tasks, it is recommended
    that they use dag.values() as it returns tasks in topological order.

    Tasks self-report its execution status (Executed/Errored) but if the
    executor runs it in a different process, it is responsible for reporting
    the status change back to the task object, as this change triggers
    changes in status in dowsmtream tasks (e.g. if a task fails, downstream
    dependencies are aborted)

    It is safe to skip task.build() on tasks that are either Skipped or
    Aborted.

    Notes
    -----
    The following is still being defined: do we need to send the whole dag
    object? Looks like we are good by just sending the tasks
    """
    def __call__(self, dag):
        exec_status = set([t.exec_status for t in dag.values()])

        if exec_status - {TaskStatus.WaitingExecution,
                          TaskStatus.WaitingUpstream,
                          TaskStatus.Skipped}:
            raise ValueError('Tasks should only have either '
                             'TaskStatus.WaitingExecution or '
                             'TaskStatus.WaitingUpstream before attempting '
                             'to execute, got status: {}'
                             .format(exec_status))
