import { useEffect, useMemo, useState } from "react";
import { api } from "./services/api";
import "./index.css";

const EVIDENCE_ID = "EVIDENCE-C92B2AADB8F1";

const NAV_ITEMS = [
  ["dashboard", "▦", "Dashboard"],
  ["evidence", "◈", "Evidence"],
  ["recordings", "▶", "Recordings"],
  ["timeline", "◷", "Timeline"],
  ["recovery", "↻", "Recovery"],
  ["provenance", "⌘", "Provenance"],
  ["custody", "✓", "Chain of Custody"],
  ["reports", "▤", "Reports"],
];

function App() {
  const [active, setActive] = useState("dashboard");
  const [health, setHealth] = useState("connecting");
  const [recordings, setRecordings] = useState([]);
  const [provenance, setProvenance] = useState(null);
  const [evidence, setEvidence] = useState(null);
  const [custody, setCustody] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        setError("");

        const [
          healthData,
          evidenceData,
          recordingData,
          provenanceData,
          custodyData,
        ] = await Promise.all([
          api.health(),
          api.evidence(),
          api.recordings(EVIDENCE_ID),
          api.provenance(EVIDENCE_ID),
          api.custody(EVIDENCE_ID),
        ]);

        setHealth(healthData.status);
        setRecordings(recordingData);
        setProvenance(provenanceData);
        setCustody(custodyData);

        if (Array.isArray(evidenceData)) {
          setEvidence(
            evidenceData.find((item) => item.id === EVIDENCE_ID) ||
              evidenceData[0]
          );
        } else {
          setEvidence(evidenceData);
        }
      } catch (err) {
        console.error(err);
        setHealth("offline");
        setError(err.message || "Unable to connect to forensic API.");
      }
    }

    loadData();
  }, []);

  const recoveredCount = useMemo(
    () =>
      recordings.filter(
        (recording) =>
          String(recording.status).toLowerCase() === "recovered"
      ).length,
    [recordings]
  );

  const normalCount = recordings.length - recoveredCount;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">DF</div>
          <div>
            <div className="brand-title">DVR FORENSICS</div>
            <div className="brand-subtitle">SIH26150</div>
          </div>
        </div>

        <div className="nav-label">INVESTIGATION</div>

        <nav>
          {NAV_ITEMS.map(([id, icon, label]) => (
            <button
              key={id}
              className={`nav-item ${active === id ? "active" : ""}`}
              onClick={() => setActive(id)}
            >
              <span className="nav-icon">{icon}</span>
              <span>{label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="demo-badge">
            <span className="demo-dot" />
            SYNTHETIC DEMO ENVIRONMENT
          </div>

          <div className="sidebar-version">
            Forensic Platform v0.3.0
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <div className="eyebrow">FORENSIC ANALYSIS PLATFORM</div>
            <h1>{getPageTitle(active)}</h1>
          </div>

          <div className="connection">
            <span
              className={`connection-dot ${
                health === "healthy" ? "online" : ""
              }`}
            />
            <span>
              API {health === "healthy" ? "CONNECTED" : "OFFLINE"}
            </span>
            <span className="connection-url">
              127.0.0.1:8001
            </span>
          </div>
        </header>

        {error && (
          <div className="error-banner">
            <strong>API Error:</strong> {error}
          </div>
        )}

        {active === "dashboard" && (
          <Dashboard
            evidence={evidence}
            recordings={recordings}
            custody={custody}
            provenance={provenance}
            recoveredCount={recoveredCount}
            normalCount={normalCount}
          />
        )}

        {active === "evidence" && (
          <EvidencePanel evidence={evidence} />
        )}

        {active === "recordings" && (
          <RecordingsPanel recordings={recordings} />
        )}

        {active === "timeline" && (
          <TimelinePanel custody={custody} />
        )}

        {active === "recovery" && (
          <RecoveryPanel
            recordings={recordings}
            evidenceId={EVIDENCE_ID}
          />
        )}

        {active === "provenance" && (
          <ProvenancePanel provenance={provenance} />
        )}

        {active === "custody" && (
          <CustodyPanel custody={custody} />
        )}

        {active === "reports" && <ReportsPanel />}
      </main>
    </div>
  );
}

function Dashboard({
  evidence,
  recordings,
  custody,
  provenance,
  recoveredCount,
  normalCount,
}) {
  return (
    <div className="page">
      <div className="demo-notice">
        <span>●</span>
        <div>
          <strong>Synthetic reference environment</strong>
          <p>
            This demonstration uses the validated DemoSecure fixture.
            Recovery results are synthetic and must not be interpreted
            as real-world deleted-video recovery.
          </p>
        </div>
      </div>

      <section className="stats-grid">
        <StatCard
          label="Evidence Items"
          value={evidence ? "01" : "—"}
          detail="Active investigation"
          icon="◈"
        />

        <StatCard
          label="Recordings"
          value={String(recordings.length).padStart(2, "0")}
          detail={`${normalCount} normal · ${recoveredCount} recovered`}
          icon="▶"
        />

        <StatCard
          label="Integrity"
          value="VERIFIED"
          detail="Chain verification"
          icon="✓"
          success
        />

        <StatCard
          label="Vendor"
          value={evidence?.vendor || "DemoSecure"}
          detail={evidence?.model || "Reference adapter"}
          icon="▣"
        />
      </section>

      <section className="content-grid">
        <div className="panel evidence-card">
          <div className="panel-header">
            <div>
              <span className="panel-kicker">ACTIVE EVIDENCE</span>
              <h2>Evidence Overview</h2>
            </div>
            <span className="status-pill">DETECTED</span>
          </div>

          {evidence ? (
            <div className="evidence-details">
              <div className="file-icon">IMG</div>

              <div className="file-main">
                <h3>{evidence.filename}</h3>
                <p>{evidence.source}</p>

                <div className="hash-block">
                  <span>SHA-256</span>
                  <code>{evidence.sha256}</code>
                </div>
              </div>

              <div className="metadata">
                <Meta label="SIZE" value={`${evidence.size_bytes} B`} />
                <Meta label="STATUS" value={evidence.status} />
                <Meta label="VENDOR" value={evidence.vendor} />
              </div>
            </div>
          ) : (
            <div className="empty-state">Loading evidence...</div>
          )}
        </div>

        <div className="panel activity-card">
          <div className="panel-header">
            <div>
              <span className="panel-kicker">AUDIT TRAIL</span>
              <h2>Recent Activity</h2>
            </div>
          </div>

          <div className="activity-list">
            {custody.slice(-5).reverse().map((event, index) => (
              <div className="activity-item" key={event.id || index}>
                <div className="activity-line" />
                <div className="activity-marker">✓</div>

                <div>
                  <strong>{event.event_type}</strong>
                  <p>
                    {event.description || "Forensic event recorded"}
                  </p>
                </div>
              </div>
            ))}

            {!custody.length && (
              <div className="empty-state">
                No custody events available.
              </div>
            )}
          </div>
        </div>
      </section>

      <section className="panel recordings-card">
        <div className="panel-header">
          <div>
            <span className="panel-kicker">DISCOVERED MEDIA</span>
            <h2>Recording Inventory</h2>
          </div>

          <span className="count-badge">{recordings.length} ITEMS</span>
        </div>

        <RecordingTable recordings={recordings} />
      </section>

      <section className="bottom-grid">
        <div className="panel mini-panel">
          <span className="panel-kicker">PROVENANCE</span>
          <div className="big-number">
            {provenance?.nodes?.length ?? "—"}
          </div>
          <p>Evidence graph nodes</p>
        </div>

        <div className="panel mini-panel">
          <span className="panel-kicker">RELATIONSHIPS</span>
          <div className="big-number">
            {provenance?.edges?.length ?? "—"}
          </div>
          <p>Provenance relationships</p>
        </div>

        <div className="panel mini-panel">
          <span className="panel-kicker">CHAIN OF CUSTODY</span>
          <div className="big-number">
            {custody.length || "—"}
          </div>
          <p>Recorded forensic events</p>
        </div>
      </section>
    </div>
  );
}

function EvidencePanel({ evidence }) {
  return (
    <div className="page">
      <div className="panel large-panel">
        <div className="panel-header">
          <div>
            <span className="panel-kicker">EVIDENCE ITEM</span>
            <h2>Digital Evidence Details</h2>
          </div>
          <span className="status-pill">DETECTED</span>
        </div>

        {evidence ? (
          <div className="detail-grid">
            <Meta label="EVIDENCE ID" value={evidence.id} />
            <Meta label="FILENAME" value={evidence.filename} />
            <Meta label="SOURCE" value={evidence.source} />
            <Meta label="SIZE" value={`${evidence.size_bytes} bytes`} />
            <Meta label="VENDOR" value={evidence.vendor} />
            <Meta label="STATUS" value={evidence.status} />
            <Meta label="SHA-256" value={evidence.sha256} wide />
          </div>
        ) : (
          <div className="empty-state">Loading evidence...</div>
        )}
      </div>
    </div>
  );
}

function RecordingsPanel({ recordings }) {
  return (
    <div className="page">
      <div className="panel large-panel">
        <div className="panel-header">
          <div>
            <span className="panel-kicker">MEDIA INVENTORY</span>
            <h2>Discovered Recordings</h2>
          </div>
        </div>

        <RecordingTable recordings={recordings} />
      </div>
    </div>
  );
}

function TimelinePanel({ custody }) {
  return (
    <div className="page">
      <div className="panel large-panel">
        <div className="panel-header">
          <div>
            <span className="panel-kicker">FORENSIC TIMELINE</span>
            <h2>Investigation Events</h2>
          </div>
        </div>

        <div className="timeline">
          {custody.map((event, index) => (
            <div className="timeline-item" key={event.id || index}>
              <div className="timeline-marker" />
              <div>
                <div className="timeline-type">
                  {event.event_type}
                </div>
                <p>
                  {event.description || "Forensic event recorded"}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function RecoveryPanel({ recordings, evidenceId }) {
  const [artifacts, setArtifacts] = useState([]);
  const [loading, setLoading] = useState(false);

  async function loadArtifacts() {
    try {
      const data = await api.recoveryArtifacts(evidenceId);
      setArtifacts(data);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    loadArtifacts();
  }, []);

  async function recover(recordingId) {
    setLoading(true);

    try {
      await api.recover(evidenceId, recordingId);
      await loadArtifacts();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="demo-notice">
        <span>●</span>
        <div>
          <strong>Synthetic recovery engine</strong>
          <p>
            Recovery in this reference implementation creates a
            separate deterministic artifact and never modifies the
            original evidence.
          </p>
        </div>
      </div>

      <div className="panel large-panel">
        <div className="panel-header">
          <div>
            <span className="panel-kicker">RECOVERY</span>
            <h2>Recovery Artifacts</h2>
          </div>
        </div>

        <div className="recovery-list">
          {recordings.map((recording) => (
            <div className="recovery-row" key={recording.id}>
              <div>
                <strong>{recording.id}</strong>
                <p>{recording.camera || "Camera unavailable"}</p>
              </div>

              <span
                className={`recording-status ${
                  String(recording.status).toLowerCase()
                }`}
              >
                {recording.status}
              </span>

              <button
                className="action-button"
                onClick={() => recover(recording.id)}
                disabled={loading}
              >
                {loading ? "PROCESSING..." : "RECOVER"}
              </button>
            </div>
          ))}
        </div>

        <div className="artifact-section">
          <span className="panel-kicker">GENERATED ARTIFACTS</span>

          {artifacts.length ? (
            artifacts.map((artifact) => (
              <div className="artifact-row" key={artifact.id}>
                <div>
                  <strong>{artifact.id}</strong>
                  <p>{artifact.method}</p>
                </div>

                <span className="status-pill">
                  {artifact.confidence}
                </span>

                <code>{artifact.sha256}</code>
              </div>
            ))
          ) : (
            <div className="empty-state">
              No recovery artifacts generated.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function ProvenancePanel({ provenance }) {
  return (
    <div className="page">
      <div className="panel large-panel">
        <div className="panel-header">
          <div>
            <span className="panel-kicker">EVIDENCE GRAPH</span>
            <h2>Provenance</h2>
          </div>

          <span className="count-badge">
            {provenance?.nodes?.length || 0} NODES
          </span>
        </div>

        <div className="graph">
          {provenance?.nodes?.map((node) => (
            <div className="graph-node" key={node.id}>
              <span>{node.type || "NODE"}</span>
              <strong>{node.id}</strong>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function CustodyPanel({ custody }) {
  return (
    <div className="page">
      <div className="panel large-panel">
        <div className="panel-header">
          <div>
            <span className="panel-kicker">INTEGRITY</span>
            <h2>Chain of Custody</h2>
          </div>

          <span className="verified-badge">✓ VERIFIED</span>
        </div>

        <div className="custody-list">
          {custody.map((event, index) => (
            <div className="custody-row" key={event.id || index}>
              <span className="custody-number">
                {String(index + 1).padStart(2, "0")}
              </span>

              <div>
                <strong>{event.event_type}</strong>
                <p>{event.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function ReportsPanel() {
  return (
    <div className="page">
      <div className="panel report-placeholder">
        <div className="report-icon">▤</div>
        <h2>Forensic Reports</h2>
        <p>
          Report generation is the next reporting module. The
          underlying evidence, custody, recovery, and provenance
          APIs are already available.
        </p>
        <button className="action-button" disabled>
          REPORT ENGINE — COMING NEXT
        </button>
      </div>
    </div>
  );
}

function RecordingTable({ recordings }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>RECORDING</th>
            <th>CAMERA</th>
            <th>CHANNEL</th>
            <th>START</th>
            <th>END</th>
            <th>STATUS</th>
          </tr>
        </thead>

        <tbody>
          {recordings.map((recording) => (
            <tr key={recording.id}>
              <td>
                <strong>{recording.id}</strong>
              </td>
              <td>{recording.camera || "—"}</td>
              <td>{recording.channel ?? "—"}</td>
              <td>{recording.start_time || "—"}</td>
              <td>{recording.end_time || "—"}</td>
              <td>
                <span
                  className={`recording-status ${
                    String(recording.status).toLowerCase()
                  }`}
                >
                  {recording.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {!recordings.length && (
        <div className="empty-state">No recordings discovered.</div>
      )}
    </div>
  );
}

function StatCard({ label, value, detail, icon, success }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <div className="stat-label">{label}</div>
      <div className={`stat-value ${success ? "success" : ""}`}>
        {value}
      </div>
      <div className="stat-detail">{detail}</div>
    </div>
  );
}

function Meta({ label, value, wide = false }) {
  return (
    <div className={`meta ${wide ? "wide" : ""}`}>
      <span>{label}</span>
      <strong>{value || "—"}</strong>
    </div>
  );
}

function getPageTitle(active) {
  const item = NAV_ITEMS.find(([id]) => id === active);
  return item ? item[2] : "Dashboard";
}

export default App;