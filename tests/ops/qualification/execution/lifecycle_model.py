"""Independent lifecycle reference; no SQL, production imports or authority.

Identities are opaque inputs. This describes the single-attempt journal contract,
not signature verification, replay decisions, OS cleanup or service scheduling.
An uncertain interruption is an explicit input; reopening alone cannot infer that
a live worker died. Every accepted transition appends one event, except reopen.
"""


class LifecycleModel:
    def __init__(self):
        self.state = None
        self.validity = 'VALID'
        self.request_identity = None
        self.has_container = False
        self.launch_intents = 0
        self.captured_identity = None
        self.attestation = None
        self.result_authentication = None
        self.events = 0

    def apply(self, action, *, identity=None):
        """Predict ACCEPTED, RETRY, CONFLICT or REJECTED without store feedback."""
        if action == 'reopen':
            return 'ACCEPTED'
        if action in ('submit', 'conflicting_submit'):
            if self.state is not None:
                return 'RETRY' if identity == self.request_identity else 'CONFLICT'
            self.request_identity = identity
            self.state = 'DISPATCHED'
        elif action == 'commit' and self.result_authentication is not None:
            return 'RETRY' if identity == self.result_authentication else 'CONFLICT'
        elif self.state is None:
            return 'REJECTED'
        elif action == 'void':
            if self.validity == 'VOID':
                return 'REJECTED'
            self.validity = 'VOID'
        elif action in ('uncertain', 'abort'):
            # Diagnostic interruption may still be recorded after cancellation.
            if self.state not in ('DISPATCHED', 'START_INTENT', 'RUNNING'):
                return 'REJECTED'
            self.state = 'IN_DOUBT' if action == 'uncertain' else 'ABORTED'
        elif self.validity == 'VOID':
            return 'REJECTED'
        elif action == 'container':
            if self.state != 'DISPATCHED' or self.has_container:
                return 'REJECTED'
            self.has_container = True
        elif action == 'intent':
            if self.state != 'DISPATCHED' or not self.has_container:
                return 'REJECTED'
            self.state = 'START_INTENT'
            self.launch_intents += 1
        elif action == 'running':
            if self.state != 'START_INTENT':
                return 'REJECTED'
            self.state = 'RUNNING'
        elif action == 'capture':
            if self.state != 'RUNNING':
                return 'REJECTED'
            self.state = 'CAPTURED'
            self.captured_identity = identity
        elif action == 'publish':
            if self.state != 'CAPTURED':
                return 'REJECTED'
            self.state = 'ATTESTED'
            self.attestation = identity
        elif action == 'commit':
            if self.state != 'ATTESTED':
                return 'REJECTED'
            self.result_authentication = identity
        else:
            raise ValueError('unknown reference-model action: ' + action)
        self.events += 1
        return 'ACCEPTED'
