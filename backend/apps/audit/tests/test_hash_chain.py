from apps.audit.hashing import compute_entry_hash

def test_determine_same_input():
    h1 = compute_entry_hash(1, None, {"action": "LOGIN", "user_id": 42})
    h2 = compute_entry_hash(1, None, {"action": "LOGIN", "user_id": 42})
    assert h1 == h2
def test_deterministic_key_order_does_not_matter():
    a = compute_entry_hash(1, None, {"a": 1, "b": 2})
    b = compute_entry_hash(1, None, {"b": 2, "a": 1})
    assert a == b  
def test_payload_change_changes_hash():
    h1 = compute_entry_hash(1, None, {"action": "LOGIN", "user_id": 42})
    h2 = compute_entry_hash(1, None, {"action": "LOGIN", "user_id": 99})
    assert h1 != h2
def test_seq_change_changes_hash():
    a = compute_entry_hash(1, None, {"action": "LOGIN"})
    b = compute_entry_hash(2, None, {"action": "LOGIN"})
    assert a != b
def test_chaining_hash_of_n_depends_on_hash_of_n_minus_1():
    first = compute_entry_hash(1, None, {"action": "LOGIN", "user_id": 42})
    other_first = compute_entry_hash(1, None, {"action": "LOGIN", "user_id": 7})
    assert first != other_first

    tail_a = compute_entry_hash(2, first, {"action": "DELETE", "user_id": 42})
    tail_b = compute_entry_hash(2, other_first, {"action": "DELETE", "user_id": 42})
    assert tail_a != tail_b  # identical N, different prev_hash -> different hash