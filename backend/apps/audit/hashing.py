import json
import hashlib
def cannoical_json(data):
    #data -> whatever kind of data passed (probabay a dict in this project as used in the test below)
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    #sort_keys=True sorts the keys of the dict so it returns in the same order everytime
    #separators=(',', ':') Removes the whitespace
    #ensure_ascii=False doesn't actually modify the output but writes the letter as they are 
print(cannoical_json({"user_id": 42, "action": "LOGIN"}))
#Result : {"action":"LOGIN","user_id":42} -> sorted and no white spaces

def compute_entry_hash(seq,prev_hash,payload):
#seq -> The sequence/entry number (e.g., 1, 2, 3). Ensures log entries stay in chronological order and prevents missing entries
#prev -> The SHA-256 hash of the entry immediately before this one (or a string of zeros like "0000..." for the first entry). This links every log entry to its parent.
#payload -> The actual audit event data (e.g., who did what).
   preimage = cannoical_json({
       "seq":seq,
       "prev_hash":prev_hash,
       "payload":payload,
   })
   return hashlib.sha256(preimage.encode("utf-8")).hexdigest()
