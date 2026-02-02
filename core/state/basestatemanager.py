from helper import log_error
class BaseStateManager:
    def __init__(self, initial_state, allowed_transitions, log_fn=None, state_name="STATE"):
        """
        :param initial_state: The starting state (an enum member)
        :param allowed_transitions: dict of {state: [allowed_next_states]}
        :param log_fn: Optional function to log state transitions
        :param state_name: String name of this state manager (used for logging/debug)
        """
        self.state = initial_state
        self.previous_state = None
        self.allowed_transitions = allowed_transitions
        self.log_fn = log_fn
        self.state_name = state_name

    def set_state(self, new_state):
        if new_state == self.state:
            return
        if new_state in self.allowed_transitions.get(self.state, []):
            if self.log_fn:
                self.log_fn(self.state, new_state, self.state_name)
            self.previous_state = self.state
            self.state = new_state
            print(self.get_state())
        else:
            log_error(f"{new_state} not in allowed transitions for {self.state}")
            
    def is_state(self, state):
        return self.state == state

    def get_state(self):
        return f"{self.state_name}: {self.state}"

    def revert_to_previous(self):
        if self.previous_state is not None:
            self.set_state(self.previous_state)
