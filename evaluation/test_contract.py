"""Evaluator-owned tests, withheld from the generating model."""
import pytest
from payment_client import pay


class Server:
    def __init__(self):
        self.charges = {}
        self.calls = []
        self.lost = False

    def charge(self, payload, *, idempotency_key):
        self.calls.append((payload, idempotency_key))
        if idempotency_key not in self.charges:
            self.charges[idempotency_key] = {"id": len(self.charges)+1, "amount":payload["amount"]}
        if not self.lost:
            self.lost = True
            raise TimeoutError("committed but response lost")
        return self.charges[idempotency_key]


def test_committed_response_loss_does_not_create_second_charge():
    server = Server()
    result = pay(server, {"amount":100})
    assert result == {"id":1, "amount":100}
    assert len(server.charges) == 1
    assert len(server.calls) == 2


def test_identical_new_call_is_new_logical_payment():
    server = Server()
    first = pay(server, {"amount":100})
    second = pay(server, {"amount":100})
    assert first["id"] != second["id"]
    assert len(server.charges) == 2


def test_exact_timeout_instance_and_limit():
    errors = [TimeoutError(str(i)) for i in range(3)]
    class Transport:
        calls = []
        def charge(self, payload, *, idempotency_key):
            self.calls.append(idempotency_key)
            raise errors[len(self.calls)-1]
    transport = Transport()
    with pytest.raises(TimeoutError) as raised:
        pay(transport, {})
    assert raised.value is errors[-1]
    assert len(transport.calls) == 3
    assert len(set(transport.calls)) == 1


def test_other_error_immediate_and_preserved():
    error = ValueError("declined")
    class Transport:
        calls = 0
        def charge(self, payload, *, idempotency_key):
            self.calls += 1
            raise error
    transport = Transport()
    with pytest.raises(ValueError) as raised:
        pay(transport, {})
    assert raised.value is error
    assert transport.calls == 1


def test_success_retains_payload_and_result():
    payload = {"amount":100, "metadata":{"invoice":42}}
    result = object()
    class Transport:
        def charge(self, sent, *, idempotency_key):
            assert sent is payload
            assert isinstance(idempotency_key, str) and idempotency_key
            return result
    assert pay(Transport(), payload) is result
