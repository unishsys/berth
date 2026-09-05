"""Offline security regression tests for supported and rejected chart configurations."""
import subprocess
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def render(*values):
    args = ['helm', 'template', 'spyglass', 'charts/spyglass']
    for value in values:
        args += ['--set', value]
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)

class ChartSecurity(unittest.TestCase):
    def test_supported_defaults(self):
        p = render()
        self.assertEqual(p.returncode, 0, p.stderr)
        for expected in ['replicas: 1', 'type: Recreate', 'path: /readyz', 'kind: PersistentVolumeClaim', 'poddisruptionbudgets', 'persistentvolumeclaims', 'storageclasses']:
            self.assertIn(expected, p.stdout)
        self.assertNotIn('AI_ALLOW_CLOUD_WITHOUT_AUTH', p.stdout)

    def test_unsafe_topologies_are_rejected(self):
        for value in ['replicaCount=2', 'auth.mode=none', 'auth.mode=typo', 'auth.mode=proxy-header', 'ai.persistence.accessMode=ReadWriteMany', 'strategy.type=RollingUpdate']:
            with self.subTest(value=value):
                self.assertNotEqual(render(value).returncode, 0)

    def test_proxy_requires_explicit_peers(self):
        p = render('auth.mode=proxy-header', 'auth.proxyTrustedCIDRs[0]=10.10.0.0/24')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('AUTH_PROXY_TRUSTED_CIDRS', p.stdout)

if __name__ == '__main__':
    unittest.main()
