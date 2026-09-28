import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css';

function App() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <header className="mb-8 border-b border-slate-800 pb-6">
          <p className="text-sm uppercase tracking-[0.2em] text-cyan-400">SAT-SA</p>
          <h1 className="mt-3 text-4xl font-semibold">Supervisory Analytics Tool</h1>
          <p className="mt-3 max-w-3xl text-slate-300">
            Human-led supervisory review of periodic SOC data for execution gaps, peer deviations,
            negative-space indicators, and prioritization.
          </p>
        </header>

        <section className="grid gap-4 md:grid-cols-3">
          {[
            ['Entities', '12 priority entities'],
            ['Findings', '7 active supervisory findings'],
            ['Audit', '4 recent review actions'],
          ].map(([label, value]) => (
            <div key={label} className="rounded-xl border border-slate-800 bg-slate-900 p-5 shadow-lg shadow-slate-950/30">
              <p className="text-sm text-slate-400">{label}</p>
              <p className="mt-3 text-2xl font-semibold">{value}</p>
            </div>
          ))}
        </section>
      </div>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
