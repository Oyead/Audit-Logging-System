import threading
from concurrent.futures import ThreadPoolExecutor

from django.db import connections
from django.test import TransactionTestCase

from apps.audit.hashing import compute_entry_hash
from apps.audit.models import AuditLogEntry,ChainHead
from apps.audit.services import append_entry

class ConcurrencyAppendTests(TransactionTestCase):
    # TransactionTestCase: real commits so other connections see/lock ChainHead
    N = 20
    def test_concurrent_appends_from_single_contiguous_chain(self):
        errors=[]
        barrier = threading.Barrier(self.N)

        def worker(i):
            try:
                barrier.wait(timeout=10)
                append_entry({"event":"op","i":i})
            except Exception as e:
                errors.append(e)
            finally:
                connections.close_all()
        with ThreadPoolExecutor(max_workers=self.N) as ex:
            list(ex.map(worker, range(self.N)))
            
        # 1) contiguous seqs 1..N
        self.assertEqual(errors,[])
        entries = list(AuditLogEntry.objects.order_by("seq"))
        self.assertEqual([e.seq for e in entries],list(range(1,self.N + 1)))

        # 2) hashes recompute + chaining
        prev_hash = None
        for e in entries:
            self.assertEqual(e.prev_hash,prev_hash)
            self.assertEqual(e.hash,compute_entry_hash(e.seq,e.prev_hash,e.payload))
            prev_hash=e.hash
        
        # 3) single head advanced to N
        head = ChainHead.objects.get(pk=1)
        self.assertEqual(head.last_seq, self.N)
        self.assertEqual(head.last_hash, entries[-1].hash)

        # (optional) only one ChainHead row exists
        self.assertEqual(ChainHead.objects.count(),1)

